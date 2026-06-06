import reflex as rx

config = rx.Config(
    app_name="sandbox_reflex",
    show_reflex_badge=False,
    db_url="sqlite:///horas_extras.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)