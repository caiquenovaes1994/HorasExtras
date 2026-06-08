import reflex as rx
from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    username: str = Field(unique=True, index=True)
    password: str
    nome_completo: Optional[str] = None
    is_admin: bool = Field(default=False)
    perfil: str = Field(default="USER")
    must_change_password: bool = Field(default=True)
    valor_base: str = Field(default="0.0")
    valor_base_secure: str = Field(default="0.0")
    aceitou_termos: bool = Field(default=False)
    data_aceite: Optional[str] = None

class Chamado(SQLModel, table=True):
    __tablename__ = "chamados"
    id: Optional[int] = Field(default=None, primary_key=True)
    
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

class Hotel(SQLModel, table=True):
    __tablename__ = "hoteis"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    rid: str = Field(unique=True, index=True)
    nome: str

class SolicitacaoHotel(SQLModel, table=True):
    __tablename__ = "solicitacoes_hoteis"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    rid: str
    nome: str
    tipo: str
    user_id: Optional[int] = None
    status: str = Field(default="PENDING")
