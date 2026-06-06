import reflex as rx
from sqlmodel import select, or_
from typing import List, Dict, Any, Optional

from .state import AuthState
from .models import Hotel, SolicitacaoHotel
from .backup_utils import backup_tabela

class HotelState(rx.State):
    hoteis: List[Dict[str, Any]] = []
    solicitacoes: List[Dict[str, Any]] = []
    
    # Controle do Modal
    is_modal_open: bool = False
    
    # Formulário
    h_original_rid: str = "" # Usado para saber se é edição
    h_rid: str = ""
    h_nome: str = ""
    
    def set_h_rid(self, val: str):
        self.h_rid = val
        
    def set_h_nome(self, val: str):
        self.h_nome = val
        
    # Pesquisa
    search_query: str = ""
    
    @rx.var
    def filtered_hoteis(self) -> List[Dict[str, Any]]:
        if not self.search_query:
            return self.hoteis
        sq = self.search_query.lower()
        return [h for h in self.hoteis if sq in h["rid"].lower() or sq in h["nome"].lower()]

    def set_search_query(self, query: str):
        self.search_query = query
        
    def load_hoteis(self):
        with rx.session() as session:
            hoteis_db = session.exec(select(Hotel).order_by(Hotel.rid)).all()
            
            # Carregar solicitações PENDING para marcar quais hotéis têm pendência
            sols_db = session.exec(select(SolicitacaoHotel).where(SolicitacaoHotel.status == "PENDING")).all()
            
            # Mapeia os rids que tem pendência
            # Pode haver mudança de rid na edição (então o rid da solicitação é o NOVO rid, precisamos do original,
            # mas na modelagem de SolicitacaoHotel nós só temos `rid` e `nome`.
            # Assumiremos que o `rid` na SolicitacaoHotel de EDIT ou DELETE é o rid alvo.
            pendentes_rids = [s.rid for s in sols_db]
            
            self.hoteis = []
            for h in hoteis_db:
                has_pendency = h.rid in pendentes_rids
                # Procura a ação específica para o tooltip
                pendencia_tipo = ""
                if has_pendency:
                    for s in sols_db:
                        if s.rid == h.rid:
                            pendencia_tipo = "Exclusão" if s.tipo == "DELETE" else "Edição"
                            break

                self.hoteis.append({
                    "id": h.id,
                    "rid": h.rid,
                    "nome": h.nome,
                    "has_pendency": has_pendency,
                    "pendencia_tipo": pendencia_tipo
                })
            
            # Carrega solicitações pendentes completas para o painel do Admin
            self.solicitacoes = []
            for s in sols_db:
                self.solicitacoes.append({
                    "id": s.id,
                    "rid": s.rid,
                    "nome": s.nome,
                    "tipo": s.tipo,
                    "user_id": s.user_id
                })

    def open_new_hotel(self):
        self.h_original_rid = ""
        self.h_rid = ""
        self.h_nome = ""
        self.is_modal_open = True
        
    def open_edit_hotel(self, rid: str, nome: str):
        self.h_original_rid = rid
        self.h_rid = rid
        self.h_nome = nome
        self.is_modal_open = True
        
    def close_modal(self):
        self.is_modal_open = False
        
    async def save_hotel(self):
        if not self.h_rid or not self.h_nome:
            return rx.window_alert("Preencha RID e Nome.")
            
        with rx.session() as session:
            auth_state = await self.get_state(AuthState)
            if auth_state.user_info.get("perfil") == "GESTOR":
                return rx.window_alert("Gestores não podem adicionar hotéis.")
                
            # Novo Hotel (Insert direto liberado para todos)
            if not self.h_original_rid:
                # Verifica se já existe
                existente = session.exec(select(Hotel).where(Hotel.rid == self.h_rid)).first()
                if existente:
                    return rx.window_alert("Já existe um Hotel com este RID!")
                    
                novo = Hotel(rid=self.h_rid, nome=self.h_nome)
                session.add(novo)
                session.commit()
                backup_tabela(session, Hotel, "hoteis")
                self.is_modal_open = False
                self.load_hoteis()
                return rx.toast.success("Hotel inserido com sucesso!")
                
            # Edição
            else:
                auth_state = await self.get_state(AuthState)
                user_info = auth_state.user_info
                is_admin = user_info.get("perfil") == "ADMIN"
                
                if is_admin:
                    # Admin atualiza direto
                    hotel_db = session.exec(select(Hotel).where(Hotel.rid == self.h_original_rid)).first()
                    if hotel_db:
                        hotel_db.rid = self.h_rid
                        hotel_db.nome = self.h_nome
                        session.add(hotel_db)
                        session.commit()
                        backup_tabela(session, Hotel, "hoteis")
                        self.is_modal_open = False
                        self.load_hoteis()
                        return rx.toast.success("Hotel atualizado com sucesso!")
                else:
                    # Usuário comum gera solicitação
                    # Verifica se já existe solicitação pendente para este RID
                    s_existente = session.exec(select(SolicitacaoHotel).where(
                        SolicitacaoHotel.rid == self.h_original_rid,
                        SolicitacaoHotel.status == "PENDING"
                    )).first()
                    
                    if s_existente:
                        return rx.window_alert("Já existe uma solicitação pendente para este hotel.")
                        
                    s = SolicitacaoHotel(
                        rid=self.h_original_rid, # Na solicitação salvamos o RID original como alvo
                        nome=self.h_nome, # O novo nome proposto
                        tipo="EDIT",
                        user_id=user_info.get("id"),
                        status="PENDING"
                    )
                    session.add(s)
                    session.commit()
                    self.is_modal_open = False
                    self.load_hoteis()
                    return rx.toast.info("Sua edição foi enviada para aprovação do Administrador.")

    async def delete_hotel(self, rid: str, nome: str):
        with rx.session() as session:
            auth_state = await self.get_state(AuthState)
            user_info = auth_state.user_info
            if user_info.get("perfil") == "GESTOR":
                return rx.window_alert("Gestores não podem excluir hotéis.")
                
            is_admin = user_info.get("perfil") == "ADMIN"
            
            if is_admin:
                hotel_db = session.exec(select(Hotel).where(Hotel.rid == rid)).first()
                if hotel_db:
                    session.delete(hotel_db)
                    session.commit()
                    backup_tabela(session, Hotel, "hoteis")
                    self.load_hoteis()
                    return rx.toast.success(f"Hotel {rid} removido!")
            else:
                s_existente = session.exec(select(SolicitacaoHotel).where(
                    SolicitacaoHotel.rid == rid,
                    SolicitacaoHotel.status == "PENDING"
                )).first()
                
                if s_existente:
                    return rx.window_alert("Já existe uma solicitação pendente para este hotel.")
                    
                s = SolicitacaoHotel(
                    rid=rid,
                    nome=nome,
                    tipo="DELETE",
                    user_id=user_info.get("id"),
                    status="PENDING"
                )
                session.add(s)
                session.commit()
                self.load_hoteis()
                return rx.toast.info("Sua exclusão foi enviada para aprovação do Administrador.")

    def approve_solicitacao(self, req_id: int):
        with rx.session() as session:
            req = session.exec(select(SolicitacaoHotel).where(SolicitacaoHotel.id == req_id)).first()
            if not req: return
            
            if req.tipo == "EDIT":
                hotel_db = session.exec(select(Hotel).where(Hotel.rid == req.rid)).first()
                if hotel_db:
                    hotel_db.nome = req.nome # Atualiza apenas o nome baseado na solicitação
                    # Se fosse para alterar o RID precisariamos de um campo 'new_rid' na SolicitacaoHotel.
                    # Simplificaremos assumindo que usuários editam apenas o Nome ou geram erro se tentarem mudar o RID.
                    session.add(hotel_db)
            
            elif req.tipo == "DELETE":
                hotel_db = session.exec(select(Hotel).where(Hotel.rid == req.rid)).first()
                if hotel_db:
                    session.delete(hotel_db)
            
            req.status = "APPROVED"
            session.add(req)
            session.commit()
            if req.tipo in ["EDIT", "DELETE"]:
                backup_tabela(session, Hotel, "hoteis")
            self.load_hoteis()
            return rx.toast.success("Solicitação aprovada e aplicada.")

    def reject_solicitacao(self, req_id: int):
        with rx.session() as session:
            req = session.exec(select(SolicitacaoHotel).where(SolicitacaoHotel.id == req_id)).first()
            if not req: return
            
            req.status = "REJECTED"
            session.add(req)
            session.commit()
            self.load_hoteis()
            return rx.toast.info("Solicitação rejeitada.")
