import reflex as rx
from .state import AuthState

def login_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.cond(
                AuthState.login_error != "",
                rx.callout(
                    AuthState.login_error,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    width="100%",
                ),
            ),
            
            rx.form.root(
                rx.vstack(
                    rx.vstack(
                        rx.text("Usuário", size="2", color="#fafafa", font_weight="500"),
                        rx.input(
                            name="username",
                            required=True,
                            width="100%",
                            style={"background_color": "#202128", "border": "none", "color": "#fafafa", "height": "40px", "border_radius": "6px"}
                        ),
                        width="100%",
                        align_items="flex-start",
                        spacing="1",
                    ),
                    rx.vstack(
                        rx.text("Senha", size="2", color="#fafafa", font_weight="500"),
                        rx.input(
                            type="password",
                            name="password",
                            required=True,
                            width="100%",
                            style={"background_color": "#202128", "border": "none", "color": "#fafafa", "height": "40px", "border_radius": "6px"}
                        ),
                        width="100%",
                        align_items="flex-start",
                        spacing="1",
                    ),
                    rx.button(
                        "ENTRAR", 
                        type="submit", 
                        width="100%", 
                        size="3",
                        background_color="transparent",
                        color="white",
                        border="1px solid #333",
                        border_radius="6px",
                        cursor="pointer",
                        _hover={"background_color": "#202128"},
                        margin_top="10px"
                    ),
                    spacing="4",
                ),
                on_submit=AuthState.login,
                reset_on_submit=True,
                width="100%",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        width="100%",
        max_width="500px",
        margin="auto",
        padding="2em",
        border_radius="8px",
        background_color="#12141A",
        border="1px solid #333",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.3)",
    )

def reset_password_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Atualização de Segurança", size="6", color="#fafafa", text_align="center", width="100%"),
            rx.text("Você precisa alterar sua senha para continuar.", color="#b0b0b8", text_align="center", width="100%", margin_bottom="1em"),
            
            rx.cond(
                AuthState.login_error != "",
                rx.callout(
                    AuthState.login_error,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    width="100%",
                ),
            ),
            
            rx.form.root(
                rx.vstack(
                    rx.input(
                        placeholder="Nova Senha",
                        type="password",
                        name="new_password",
                        required=True,
                        width="100%",
                        color_scheme="ruby",
                        variant="surface",
                    ),
                    rx.input(
                        placeholder="Confirme a Nova Senha",
                        type="password",
                        name="confirm_password",
                        required=True,
                        width="100%",
                        color_scheme="ruby",
                        variant="surface",
                    ),
                    rx.button(
                        "Salvar Nova Senha", 
                        type="submit", 
                        width="100%", 
                        size="3",
                        background_color="#800000",
                        color="white",
                        cursor="pointer",
                        _hover={"background_color": "#A30000"},
                    ),
                    spacing="4",
                ),
                on_submit=AuthState.reset_password,
                reset_on_submit=True,
                width="100%",
            ),
            spacing="5",
            align="center",
            width="100%",
        ),
        width="100%",
        max_width="400px",
        margin="auto",
        padding="2em",
        border_radius="10px",
        background_color="#1E1E1E",
        border="1px solid #333",
        box_shadow="0 4px 6px rgba(0, 0, 0, 0.3)",
    )

@rx.page(route="/login", title="Login | Horas Extras")
def login_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.box(
                rx.heading("CONTROLE DE HORAS EXTRAS", size="5", color="#B22222", text_transform="uppercase", text_align="center", padding_bottom="0.5em"),
                border_bottom="1px solid #4a1c1c",
                width="100vw",
                margin_bottom="1.5em",
            ),
            rx.cond(
                AuthState.must_change_password,
                reset_password_form(),
                login_form(),
            ),
            rx.vstack(
                rx.text(
                    "Desenvolvido por ",
                    rx.text("Caique Novaes", as_="span", weight="bold"),
                    font_family="'Inter', sans-serif"
                ),
                rx.text("Desenvolvido com ☕ e Python · 2026", white_space="nowrap", font_family="'Inter', sans-serif"),
                rx.text("v2.0", color="#2ecc71", weight="bold", font_family="'Inter', sans-serif"),
                font_size="10px",
                color="#b0b0b8",
                align="center",
                spacing="1",
                width="100%",
                line_height="1.2",
                margin_top="1.5em",
            ),
            align_items="center",
            width="100%",
        ),
        width="100%",
        height="100vh",
        background_color="#0e1117",
    )
