import os
import reflex as rx
from dotenv import load_dotenv

load_dotenv()

# Monta a URL do banco: usa PostgreSQL (Supabase) se as variáveis existirem,
# senão cai no SQLite local para desenvolvimento.
_db_host = os.getenv("DB_HOST", "")
_db_name = os.getenv("DB_NAME", "")
_db_user = os.getenv("DB_USER", "")
_db_pass = os.getenv("DB_PASS", "")
_db_port = os.getenv("DB_PORT", "5432")
_db_sslmode = os.getenv("DB_SSLMODE", "require")

if _db_host and _db_host != "localhost":
    _db_url = f"postgresql+psycopg2://{_db_user}:{_db_pass}@{_db_host}:{_db_port}/{_db_name}?sslmode={_db_sslmode}"
else:
    _db_url = "sqlite:///horas_extras.db"

# Porta definida pelo Render (ou default)
_port = os.getenv("PORT", "3000")

config = rx.Config(
    app_name="sandbox_reflex",
    db_url=_db_url,
    backend_host="0.0.0.0",
    frontend_port=int(_port),
    backend_port=int(_port),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)