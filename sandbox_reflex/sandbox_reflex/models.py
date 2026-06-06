import reflex as rx
from typing import Optional
from datetime import date
from sqlmodel import Field

class Usuario(rx.Model, table=True):
    __tablename__ = "usuarios"
    
    username: str = Field(unique=True, index=True)
    password: str
    nome_completo: Optional[str] = None
    is_admin: int = Field(default=0)
    perfil: str = Field(default="USER")
    must_change_password: int = Field(default=1)
    valor_base: str = Field(default="0.0")
    valor_base_secure: str = Field(default="0.0")
    aceitou_termos: int = Field(default=0)
    data_aceite: Optional[str] = None

class Chamado(rx.Model, table=True):
    __tablename__ = "chamados"
    
    data: date
    caso: Optional[str] = None
    pms: Optional[str] = None
    hotel: Optional[str] = None
    inicio: str
    termino: str
    observacoes: Optional[str] = None
    motivo: Optional[str] = None
    username: Optional[str] = None
    valor_base_snapshot: str = Field(default="0.0")

class Hotel(rx.Model, table=True):
    __tablename__ = "hoteis"
    
    rid: str = Field(unique=True, index=True)
    nome: str

class SolicitacaoHotel(rx.Model, table=True):
    __tablename__ = "solicitacoes_hoteis"
    
    rid: str
    nome: str
    tipo: str
    user_id: Optional[int] = None
    status: str = Field(default="PENDING")
