import reflex as rx
from sqlmodel import select
from datetime import date, datetime
from typing import List, Dict, Any, Optional

from .state import AuthState
from .data_state import DataState
from .models import Chamado, Hotel
from .backup_utils import backup_tabela

class FormState(rx.State):
    is_modal_open: bool = False
    is_view_only: bool = False
    
    # Form fields
    record_id: int = -1
    f_data: str = ""
    f_caso: str = ""
    f_hotel: str = ""
    f_motivo: str = ""
    f_inicio: str = ""
    f_termino: str = ""
    f_obs: str = ""
    
    # Validation errors
    error_message: str = ""
    
    hoteis_opts: List[str] = []
    
    def set_f_data(self, val: str): self.f_data = val
    def set_f_caso(self, val: str): self.f_caso = val
    def set_f_hotel(self, val: str): self.f_hotel = val
    def set_f_motivo(self, val: str): self.f_motivo = val
    def set_f_inicio(self, val: str): self.f_inicio = val
    def set_f_termino(self, val: str): self.f_termino = val
    def set_f_obs(self, val: str): self.f_obs = val
    
    def load_hoteis(self):
        with rx.session() as session:
            hoteis = session.exec(select(Hotel).order_by(Hotel.rid)).all()
            self.hoteis_opts = [f"{h.rid} - {h.nome}" for h in hoteis]
            
    def open_new_record(self):
        self.record_id = -1
        self.f_data = datetime.now().strftime("%Y-%m-%d")
        self.f_caso = ""
        self.f_hotel = ""
        self.f_motivo = ""
        self.f_inicio = ""
        self.f_termino = ""
        self.f_obs = ""
        self.is_view_only = False
        self.error_message = ""
        self.load_hoteis()
        self.is_modal_open = True
        
    def open_edit_record(self, record_id: int):
        self.load_record(record_id)
        self.is_view_only = False
        self.error_message = ""
        self.load_hoteis()
        self.is_modal_open = True
        
    def open_view_record(self, record_id: int):
        self.load_record(record_id)
        self.is_view_only = True
        self.error_message = ""
        self.load_hoteis()
        self.is_modal_open = True
        
    def load_record(self, record_id: int):
        with rx.session() as session:
            record = session.get(Chamado, record_id)
            if record:
                self.record_id = record.id
                self.f_data = record.data.strftime("%Y-%m-%d")
                self.f_caso = record.caso or ""
                self.f_hotel = f"{record.pms} - {record.hotel}" if record.pms else (record.hotel or "")
                self.f_motivo = record.motivo or ""
                self.f_inicio = record.inicio or ""
                self.f_termino = record.termino or ""
                self.f_obs = record.observacoes or ""
                
    def close_modal(self):
        self.is_modal_open = False
        
    async def save_record(self):
        self.error_message = ""
        if not self.f_inicio or not self.f_termino or not self.f_motivo.strip():
            self.error_message = "Campos obrigatórios: Início, Término e Motivo."
            return
            
        try:
            from . import time_utils
            ti = time_utils.processar_input_horario(self.f_inicio)
            tf = time_utils.processar_input_horario(self.f_termino)
            
            pms_, hnome_ = ("", "")
            if self.f_hotel:
                if " - " in self.f_hotel:
                    pms_, hnome_ = self.f_hotel.split(" - ", 1)
                else:
                    hnome_ = self.f_hotel
                    
            user_info = await self.get_state(AuthState)
            data_state = await self.get_state(DataState)
            
            if user_info.user_info.get("perfil") == "GESTOR":
                self.error_message = "Gestores não podem alterar registros."
                return
            
            vbase_atual = user_info.user_info.get("valor_base", "0.0")
            
            with rx.session() as session:
                if self.record_id == -1:
                    novo = Chamado(
                        data=datetime.strptime(self.f_data, "%Y-%m-%d").date(),
                        caso=self.f_caso.strip() or None,
                        pms=pms_ or None,
                        hotel=hnome_ or None,
                        inicio=ti,
                        termino=tf,
                        observacoes=self.f_obs.strip() or None,
                        motivo=self.f_motivo.strip(),
                        username=user_info.user_info["username"],
                        valor_base_snapshot=str(vbase_atual)
                    )
                    session.add(novo)
                else:
                    record = session.get(Chamado, self.record_id)
                    if record:
                        record.data = datetime.strptime(self.f_data, "%Y-%m-%d").date()
                        record.caso = self.f_caso.strip() or None
                        record.pms = pms_ or None
                        record.hotel = hnome_ or None
                        record.inicio = ti
                        record.termino = tf
                        record.observacoes = self.f_obs.strip() or None
                        record.motivo = self.f_motivo.strip()
                        session.add(record)
                session.commit()
                backup_tabela(session, Chamado, "chamados")
            self.is_modal_open = False
            # Recarregar
            return DataState.load_registros()
        except Exception as e:
            self.error_message = f"Erro ao salvar: {str(e)}"
