from sqlmodel import select
import asyncio
import os
from datetime import datetime, timedelta
import reflex as rx
from .state import AuthState
from .models import Chamado
from . import time_utils
from . import report_generator

MESES_PT = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
ANOS = ["2023", "2024", "2025", "2026", "2027", "2028"]

class DataState(AuthState):
    """Estado responsável pela consulta e agrupamento dos dados da aplicação."""
    
    mes_ref: str = "JANEIRO"
    ano_ref: str = "2024"
    
    filtro_plantonista: str = "TODOS"
    opcoes_plantonistas: list[str] = ["TODOS"]
    
    # Lista de chamados processados e agrupados
    registros_agrupados: list[dict] = []
    
    # Totais calculados na hora de rodar load_registros()
    total_horas_50_td: timedelta = timedelta(0)
    total_horas_100_td: timedelta = timedelta(0)
    total_chamados: int = 0
    
    # Seleção de registros para deleção em massa
    selected_records: list[str] = []
    
    # Aba ativa
    active_tab: str = "historico"
    
    def set_active_tab(self, tab: str):
        if tab == "novo":
            from .state_form import FormState
            return FormState.open_new_record()
        self.active_tab = tab
    
    # Flag de carregamento do PDF
    is_generating_pdf: bool = False
    show_plantonista_alert: bool = False
    show_empty_equipe_alert: bool = False
    
    def close_plantonista_alert(self):
        self.show_plantonista_alert = False
        
    def close_empty_equipe_alert(self):
        self.show_empty_equipe_alert = False

    def set_mes_ref(self, mes: str):
        self.mes_ref = mes
        self.load_registros()
        
    def set_ano_ref(self, ano: str):
        self.ano_ref = ano
        self.load_registros()

    def set_filtro_plantonista(self, val: str):
        self.filtro_plantonista = val
        self.load_registros()

    def load_defaults(self):
        mes_idx = datetime.now().month - 1
        self.mes_ref = MESES_PT[mes_idx]
        self.ano_ref = str(datetime.now().year)
        self.load_registros()

    def load_registros(self):
        """Busca os chamados no banco e processa as regras de horários (nativo Python)."""
        if not self.is_authenticated:
            return
            
        # Reseta seleção sempre que os filtros mudarem
        self.selected_records = []
            
        inicio_p, fim_p = time_utils.obter_faixa_periodo(self.mes_ref, int(self.ano_ref))
        
        username_filter = self.user_info.get("username")
        perfil = self.user_info.get("perfil", "USER")
        
        with rx.session() as session:
            # Query do banco
            query = select(Chamado).where(
                Chamado.data >= inicio_p.date(),
                Chamado.data <= fim_p.date()
            )
            
            # Trava de Segurança
            if perfil == "USER":
                query = query.where(Chamado.username == username_filter)
            else:
                # Prepara opcoes_plantonistas
                from .models import Usuario
                usuarios = session.exec(
                    select(Usuario).where(Usuario.perfil != "GESTOR").order_by(Usuario.nome_completo)
                ).all()
                self.opcoes_plantonistas = ["TODOS"] + [u.nome_completo for u in usuarios]
                
                # Aplica filtro se não for TODOS
                if self.filtro_plantonista != "TODOS":
                    selected_u = session.exec(select(Usuario).where(Usuario.nome_completo == self.filtro_plantonista)).first()
                    if selected_u:
                        query = query.where(Chamado.username == selected_u.username)
                
            chamados_bd = session.exec(query).all()
            
        # Processa cada chamado retornado do banco
        registros_temp = []
        t50 = timedelta(0)
        t100 = timedelta(0)
        
        for c in chamados_bd:
            duracao = time_utils.calcular_duracao(c.inicio, c.termino)
            
            semana = time_utils.get_dia_semana(c.data)
            is_100 = semana in ["DOMINGO", "FERIADO"]
            if is_100:
                t100 += duracao
            else:
                t50 += duracao
                
            registros_temp.append({
                "id": str(c.id),
                "data": c.data.strftime("%d/%m/%Y"),
                "caso": c.caso or "—",
                "hotel": f"{c.pms} - {c.hotel}",
                "motivo": c.motivo or "—",
                "inicio": c.inicio or "—",
                "termino": c.termino or "—",
                "observacoes": c.observacoes or "—",
            })

        self.registros_agrupados = registros_temp
        self.total_horas_50_td = t50
        self.total_horas_100_td = t100
        self.total_chamados = len(chamados_bd)

    def toggle_record(self, record_id: str, is_checked: bool):
        if is_checked and record_id not in self.selected_records:
            self.selected_records.append(record_id)
        elif not is_checked and record_id in self.selected_records:
            self.selected_records.remove(record_id)
            
    @rx.var
    def is_all_selected(self) -> bool:
        if not self.registros_agrupados:
            return False
        return len(self.selected_records) == len(self.registros_agrupados)
        
    def toggle_select_all(self, checked: bool):
        if checked:
            self.selected_records = [r["id"] for r in self.registros_agrupados]
        else:
            self.selected_records = []
            
    def bulk_delete(self):
        if not self.selected_records:
            return
            
        try:
            with rx.session() as session:
                for rid in self.selected_records:
                    chamado = session.get(Chamado, int(rid))
                    if chamado:
                        session.delete(chamado)
                session.commit()
                
                try:
                    from .backup_utils import backup_tabela
                    backup_tabela(session, Chamado, "chamados")
                except Exception:
                    pass
                
            self.selected_records = []
            self.load_registros()
        except Exception as e:
            return rx.window_alert(f"Erro ao deletar: {str(e)}")
        
    def view_record(self, record_id: str):
        # Stub para a Fase futura (modal de visualizar)
        print(f"Viewing record {record_id}")
        
    def edit_record(self, record_id: str):
        # Stub para a Fase futura (modal de editar)
        print(f"Editing record {record_id}")

    @rx.var
    def total_horas_50(self) -> str:
        return time_utils.formatar_timedelta(self.total_horas_50_td)
        
    @rx.var
    def total_horas_100(self) -> str:
        return time_utils.formatar_timedelta(self.total_horas_100_td)
        
    @rx.var
    def ganhos_estimados(self) -> str:
        h50_secs = self.total_horas_50_td.total_seconds()
        h100_secs = self.total_horas_100_td.total_seconds()
        
        if h50_secs <= 0 and h100_secs <= 0:
            return "R$ 0,00"
            
        vbase = float(self.user_info.get("valor_base", 0.0))
        if vbase <= 0:
            return "R$ 0,00"
            
        valor_hora = vbase / 220
        ganho_50 = (h50_secs / 3600) * 1.5 * valor_hora
        ganho_100 = (h100_secs / 3600) * 2.0 * valor_hora
        
        total = ganho_50 + ganho_100
        return f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
    @rx.var
    def media_por_chamado(self) -> str:
        if self.total_chamados == 0:
            return "0h 00m"
            
        total_secs = self.total_horas_50_td.total_seconds() + self.total_horas_100_td.total_seconds()
        avg_secs = int(total_secs / self.total_chamados)
        
        hours, remainder = divmod(avg_secs, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if hours > 0:
            return f"{hours}h {minutes:02d}m"
        return f"{minutes}m"

    async def baixar_pdf_individual(self):
        """Gera e faz o download do PDF individual."""
        self.is_generating_pdf = True
        yield
        
        try:
            inicio_p, fim_p = time_utils.obter_faixa_periodo(self.mes_ref, int(self.ano_ref))
            perfil = self.user_info.get("perfil", "USER")
            
            with rx.session() as session:
                from .models import Usuario
                
                if perfil in ["ADMIN", "GESTOR"]:
                    if self.filtro_plantonista == "TODOS":
                        self.is_generating_pdf = False
                        self.show_plantonista_alert = True
                        yield
                        return
                    
                    target_user = session.exec(select(Usuario).where(Usuario.nome_completo == self.filtro_plantonista)).first()
                    if target_user:
                        target_username = target_user.username
                    else:
                        target_username = ""
                else:
                    target_username = self.user_info["username"]
                    target_user = None
                    
                query = select(Chamado).where(
                    Chamado.data >= inicio_p.date(),
                    Chamado.data <= fim_p.date(),
                    Chamado.username == target_username
                )
                chamados_bd = session.exec(query).all()
                
                if target_username == self.user_info["username"]:
                    vbase = float(self.user_info.get("valor_base", 0.0))
                    nome = self.user_info.get("nome", "PLANTONISTA")
                else:
                    if target_user:
                        nome = target_user.nome_completo
                        from . import database
                        try:
                            vbase = float(database._decrypt(target_user.valor_base))
                        except:
                            vbase = 0.0
                    else:
                        nome = self.filtro_plantonista
                        vbase = 0.0
                
            raw_dicts = []
            for c in chamados_bd:
                raw_dicts.append({
                    "data": c.data,
                    "inicio": c.inicio,
                    "termino": c.termino,
                    "observacoes": c.observacoes,
                    "valor_base_snapshot": c.valor_base_snapshot,
                    "valor_base_fallback": vbase,
                })
            
            # Executa a geração pesada em thread separada para não bloquear
            out_path = await asyncio.to_thread(
                report_generator.gerar_pdf,
                raw_dicts,
                nome,
                self.mes_ref,
                self.ano_ref,
                vbase,
                "folha_individual.pdf"
            )
            
            with open(out_path, "rb") as f:
                pdf_data = f.read()
            
            # Exclui o arquivo físico do servidor após ler para memória
            if os.path.exists(out_path):
                os.remove(out_path)
                
            nome_arquivo = f"{nome}_HorasExtras_{self.mes_ref}.pdf"
            yield rx.download(data=pdf_data, filename=nome_arquivo)
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
        finally:
            self.is_generating_pdf = False
            yield
            
    async def baixar_pdf_equipe(self):
        """Gera e faz o download do PDF de toda a equipe (Apenas GESTOR)."""
        self.is_generating_pdf = True
        yield
        
        try:
            inicio_p, fim_p = time_utils.obter_faixa_periodo(self.mes_ref, int(self.ano_ref))
            
            with rx.session() as session:
                query = select(Chamado).where(
                    Chamado.data >= inicio_p.date(),
                    Chamado.data <= fim_p.date()
                )
                chamados_bd = session.exec(query).all()
                
            # Agrupa os chamados brutos por Username
            agrupado_por_user = {}
            for c in chamados_bd:
                user = c.username
                if user not in agrupado_por_user:
                    agrupado_por_user[user] = {
                        "nome": c.nome_completo or user,
                        "vbase": float(c.valor_base) if c.valor_base else 0.0,
                        "registros": []
                    }
                agrupado_por_user[user]["registros"].append({
                    "data": c.data,
                    "inicio": c.inicio,
                    "termino": c.termino,
                    "observacoes": c.observacoes
                })
                
            lista_consolidados = []
            for u_data in agrupado_por_user.values():
                lista_consolidados.append((
                    u_data["registros"],
                    u_data["nome"],
                    u_data["vbase"]
                ))
                
            if not lista_consolidados:
                self.is_generating_pdf = False
                self.show_empty_equipe_alert = True
                yield
                return
                
            out_path = await asyncio.to_thread(
                report_generator.gerar_pdf_massa,
                lista_consolidados,
                self.mes_ref,
                self.ano_ref,
                "folha_equipe.pdf"
            )
            
            with open(out_path, "rb") as f:
                pdf_data = f.read()
                
            # Exclui o arquivo físico do servidor após ler para memória
            if os.path.exists(out_path):
                os.remove(out_path)
                
            nome_arquivo_equipe = f"EQUIPE_HorasExtras_{self.mes_ref}.pdf"
            yield rx.download(data=pdf_data, filename=nome_arquivo_equipe)
            
        except Exception as e:
            print(f"Erro ao gerar PDF Consolidado: {e}")
        finally:
            self.is_generating_pdf = False
            yield
