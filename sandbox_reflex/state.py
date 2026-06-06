import reflex as rx
import json
from sqlmodel import select
from . import database
from .models import Usuario

class AuthState(rx.State):
    """Estado global de autenticação do usuário."""
    auth_token: str = rx.Cookie("", max_age=86400) # 24 horas de validade
    
    # Propriedades do usuário em sessão
    user_info: dict = {"nome": "", "username": "", "perfil": "", "aceitou_termos": True}
    is_authenticated: bool = False
    
    # Controle de formulário e fluxo
    login_error: str = ""
    must_change_password: bool = False
    show_policy: bool = False
    
    # Perfil
    is_profile_modal_open: bool = False
    p_nome: str = ""
    p_new_password: str = ""
    p_valor_base: str = ""
    
    def toggle_policy(self):
        self.show_policy = not self.show_policy
    
    @rx.var
    def needs_lgpd_acceptance(self) -> bool:
        if not self.is_authenticated:
            return False
        return not self.user_info.get("aceitou_termos", True)
        
    def login(self, form_data: dict):
        """Processa o formulário de login via ORM."""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "")
        
        self.login_error = ""
        
        with rx.session() as session:
            user_model = session.exec(
                select(Usuario).where(Usuario.username == username)
            ).first()
            
            if user_model and database._check_pw(password, user_model.password):
                user_dict = {
                    "id": user_model.id,
                    "username": user_model.username,
                    "nome": user_model.nome_completo,
                    "admin": bool(user_model.is_admin),
                    "must_change": bool(user_model.must_change_password),
                    "valor_base": database._decrypt(user_model.valor_base),
                    "perfil": user_model.perfil or "USER",
                    "aceitou_termos": bool(user_model.aceitou_termos)
                }
                
                if user_dict["must_change"]:
                    self.must_change_password = True
                    self.user_info = {"id": user_dict["id"], "username": user_dict["username"]}
                else:
                    self.must_change_password = False
                    self._create_session(user_dict)
                    return rx.redirect("/")
            else:
                self.login_error = "Credenciais inválidas."
            
    def _create_session(self, user: dict):
        """Cria o cookie cifrado de sessão."""
        self.user_info = user
        self.is_authenticated = True
        
        payload = json.dumps({"username": user["username"]})
        self.auth_token = database.encrypt_str(payload)
        
    def check_session(self):
        """Verifica cookie via ORM. Roda no evento on_load."""
        if self.is_authenticated:
            return
            
        if self.auth_token:
            payload_str = database.decrypt_str(self.auth_token)
            if payload_str:
                try:
                    payload = json.loads(payload_str)
                    username = payload.get("username")
                    if username:
                        with rx.session() as session:
                            user_model = session.exec(
                                select(Usuario).where(Usuario.username == username)
                            ).first()
                            
                            if user_model and not user_model.must_change_password:
                                self.user_info = {
                                    "id": user_model.id,
                                    "username": user_model.username,
                                    "nome": user_model.nome_completo,
                                    "admin": bool(user_model.is_admin),
                                    "must_change": bool(user_model.must_change_password),
                                    "valor_base": database._decrypt(user_model.valor_base),
                                    "perfil": user_model.perfil or "USER",
                                    "aceitou_termos": bool(user_model.aceitou_termos)
                                }
                                self.is_authenticated = True
                                return
                except Exception as e:
                    print(f"Erro na verificação de sessão: {e}")
                    pass
                    
        self.logout()
        return rx.redirect("/login")
        
    def logout(self):
        """Encerra a sessão limpando o cookie e os dados."""
        self.auth_token = ""
        self.is_authenticated = False
        self.user_info = {}
        self.must_change_password = False
        return rx.redirect("/login")
        
    def reset_password(self, form_data: dict):
        """Processa a troca de senha via ORM."""
        new_password = form_data.get("new_password", "")
        confirm_password = form_data.get("confirm_password", "")
        
        if not new_password or new_password != confirm_password:
            self.login_error = "As senhas não coincidem ou estão vazias."
            return
            
        with rx.session() as session:
            user_model = session.exec(
                select(Usuario).where(Usuario.id == self.user_info["id"])
            ).first()
            
            if user_model:
                user_model.password = database._hash_pw(new_password)
                user_model.must_change_password = False
                session.add(user_model)
                session.commit()
                
                # Atualiza info e cria cookie
                user_dict = {
                    "id": user_model.id,
                    "username": user_model.username,
                    "nome": user_model.nome_completo,
                    "admin": bool(user_model.is_admin),
                    "must_change": bool(user_model.must_change_password),
                    "valor_base": database._decrypt(user_model.valor_base),
                    "perfil": user_model.perfil or "USER",
                    "aceitou_termos": bool(user_model.aceitou_termos)
                }
                
                self.must_change_password = False
                self.login_error = ""
                self._create_session(user_dict)
                return rx.redirect("/")
            
    def aceitar_termos_lgpd(self):
        """Atualiza a flag LGPD via ORM."""
        if not self.is_authenticated:
            return
            
        from datetime import datetime
        data_atual_sp = datetime.now().isoformat()
        
        data_atual_sp = datetime.now()
        
        with rx.session() as session:
            user_model = session.exec(
                select(Usuario).where(Usuario.id == self.user_info["id"])
            ).first()
            
            if user_model:
                user_model.aceitou_termos = True
                user_model.data_aceite = data_atual_sp.strftime("%Y-%m-%d %H:%M:%S")
                session.add(user_model)
                session.commit()
                
                # Atualiza state local
                self.user_info["aceitou_termos"] = True

    def open_profile(self):
        self.p_nome = self.user_info.get("nome", "")
        self.p_new_password = ""
        self.p_valor_base = self.user_info.get("valor_base", "0.0")
        self.is_profile_modal_open = True
        
    def close_profile(self):
        self.is_profile_modal_open = False
        
    def set_p_new_password(self, val: str):
        self.p_new_password = val
        
    def set_p_nome(self, val: str):
        self.p_nome = val
        
    def set_p_valor_base(self, val: str):
        self.p_valor_base = val
        
    def save_profile(self):
        if not self.is_authenticated: return
        
        with rx.session() as session:
            user_model = session.exec(
                select(Usuario).where(Usuario.id == self.user_info["id"])
            ).first()
            
            if user_model:
                # Atualiza Nome
                if self.p_nome.strip():
                    user_model.nome_completo = self.p_nome.strip()
                    self.user_info["nome"] = self.p_nome.strip()
                    
                # Se preencheu nova senha, atualiza
                if self.p_new_password.strip():
                    user_model.password = database._hash_pw(self.p_new_password)
                
                # Atualiza valor base seguro (Apenas se não for GESTOR ou se o GESTOR preencher, mas a UI não vai mostrar pro GESTOR)
                try:
                    # Permite trocar vírgula por ponto
                    vb_str = self.p_valor_base.replace(",", ".")
                    vb = float(vb_str)
                except ValueError:
                    return rx.window_alert("Valor base inválido. Use formato numérico (ex: 15.50 ou 15,50)")
                    
                user_model.valor_base = database._encrypt(str(vb))
                
                session.add(user_model)
                session.commit()
                
                # Update no estado local
                self.user_info["valor_base"] = str(vb)
                
                self.is_profile_modal_open = False
                return rx.toast.success("Perfil atualizado com sucesso!")
