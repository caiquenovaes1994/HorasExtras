import reflex as rx
from sqlmodel import select
from typing import List, Dict, Any
import bcrypt

from .state import AuthState
from .models import Usuario
from .backup_utils import backup_tabela

class UsuarioState(rx.State):
    usuarios: List[Dict[str, Any]] = []
    
    # Modal state
    is_modal_open: bool = False
    
    # Form fields
    u_id: int = -1 # -1 means new user
    u_username: str = ""
    u_nome: str = ""
    u_perfil: str = "USER" # USER or ADMIN
    
    async def _is_admin(self) -> bool:
        auth_state = await self.get_state(AuthState)
        return auth_state.user_info.get("perfil") == "ADMIN"
        
    async def load_usuarios(self):
        # Somente admins devem carregar a lista de usuários para evitar vazamento
        if not (await self._is_admin()):
            self.usuarios = []
            return
            
        with rx.session() as session:
            users_db = session.exec(select(Usuario).order_by(Usuario.nome_completo)).all()
            self.usuarios = []
            for u in users_db:
                self.usuarios.append({
                    "id": u.id,
                    "username": u.username,
                    "nome_completo": u.nome_completo or "",
                    "perfil": u.perfil,
                    "is_admin": u.is_admin
                })

    async def open_new_user(self):
        if not (await self._is_admin()): return
        self.u_id = -1
        self.u_username = ""
        self.u_nome = ""
        self.u_perfil = "USER"
        self.is_modal_open = True
        
    async def open_edit_user(self, user_dict: Dict[str, Any]):
        if not (await self._is_admin()): return
        self.u_id = user_dict["id"]
        self.u_username = user_dict["username"]
        self.u_nome = user_dict["nome_completo"]
        self.u_perfil = user_dict["perfil"]
        self.is_modal_open = True
        
    def close_modal(self):
        self.is_modal_open = False
        
    def set_u_username(self, val: str):
        self.u_username = val
        
    def set_u_nome(self, val: str):
        self.u_nome = val
        
    def set_u_perfil(self, val: str):
        self.u_perfil = val

    async def save_usuario(self):
        if not (await self._is_admin()): return
        
        if not self.u_username or not self.u_nome:
            return rx.window_alert("Preencha Username e Nome Completo.")
            
        with rx.session() as session:
            is_admin_flag = 1 if self.u_perfil == "ADMIN" else 0
            
            if self.u_id == -1:
                # Novo usuário
                existente = session.exec(select(Usuario).where(Usuario.username == self.u_username)).first()
                if existente:
                    return rx.window_alert("Este Username já está em uso!")
                    
                # Gera senha padrão
                senha_padrao = "mudar@123"
                hashed = bcrypt.hashpw(senha_padrao.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                
                novo = Usuario(
                    username=self.u_username,
                    password=hashed,
                    nome_completo=self.u_nome,
                    is_admin=is_admin_flag,
                    perfil=self.u_perfil,
                    must_change_password=1,
                    valor_base="0.0",
                    valor_base_secure="0.0",
                    aceitou_termos=0
                )
                session.add(novo)
                session.commit()
                backup_tabela(session, Usuario, "usuarios")
                self.is_modal_open = False
                await self.load_usuarios()
                return rx.toast.success(f"Usuário criado! Senha padrão: {senha_padrao}")
                
            else:
                # Edição
                user_db = session.exec(select(Usuario).where(Usuario.id == self.u_id)).first()
                if user_db:
                    # Checa colisão de username
                    if user_db.username != self.u_username:
                        existente = session.exec(select(Usuario).where(Usuario.username == self.u_username)).first()
                        if existente:
                            return rx.window_alert("Este Username já está em uso por outro usuário!")
                            
                    user_db.username = self.u_username
                    user_db.nome_completo = self.u_nome
                    user_db.perfil = self.u_perfil
                    user_db.is_admin = is_admin_flag
                    session.add(user_db)
                    session.commit()
                    backup_tabela(session, Usuario, "usuarios")
                    self.is_modal_open = False
                    await self.load_usuarios()
                    return rx.toast.success("Usuário atualizado com sucesso!")

    async def delete_usuario(self, user_id: int):
        if not (await self._is_admin()): return
        with rx.session() as session:
            user_db = session.exec(select(Usuario).where(Usuario.id == user_id)).first()
            if user_db:
                # Evita que o admin apague a si mesmo
                auth_state = await self.get_state(AuthState)
                current_user_id = auth_state.user_info.get("id")
                if current_user_id == user_id:
                    return rx.window_alert("Você não pode excluir seu próprio usuário!")
                    
                session.delete(user_db)
                session.commit()
                backup_tabela(session, Usuario, "usuarios")
                await self.load_usuarios()
                return rx.toast.success("Usuário removido!")

    async def reset_password(self, user_id: int):
        if not (await self._is_admin()): return
        with rx.session() as session:
            user_db = session.exec(select(Usuario).where(Usuario.id == user_id)).first()
            if user_db:
                senha_padrao = "mudar@123"
                hashed = bcrypt.hashpw(senha_padrao.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                
                user_db.password = hashed
                user_db.must_change_password = 1
                session.add(user_db)
                session.commit()
                backup_tabela(session, Usuario, "usuarios")
                return rx.toast.info("Senha redefinida para a padrão: mudar@123")
