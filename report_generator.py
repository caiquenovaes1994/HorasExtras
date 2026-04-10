from reportlab.lib             import colors
from reportlab.lib.pagesizes   import A4, landscape
from reportlab.platypus        import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles      import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units        import cm
from reportlab.pdfbase         import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime                  import datetime, timedelta

from utils import formatar_timedelta

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DE FONTES (CALIBRI)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_BOLD = "Helvetica-Bold"

def _registrar_fontes():
    global DEFAULT_FONT, DEFAULT_FONT_BOLD
    calibri_path = "C:\\Windows\\Fonts\\calibri.ttf"
    calibri_bold_path = "C:\\Windows\\Fonts\\calibrib.ttf"
    
    try:
        if os.path.exists(calibri_path):
            pdfmetrics.registerFont(TTFont('Calibri', calibri_path))
            DEFAULT_FONT = 'Calibri'
        if os.path.exists(calibri_bold_path):
            pdfmetrics.registerFont(TTFont('Calibri-Bold', calibri_bold_path))
            DEFAULT_FONT_BOLD = 'Calibri-Bold'
    except Exception as e:
        print(f"Erro ao registrar Calibri: {e}")

_registrar_fontes()

# ─────────────────────────────────────────────────────────────────────────────
# PALETA DE CORES (Referência)
# ─────────────────────────────────────────────────────────────────────────────
WINE       = colors.Color(128/255,   0,     0)        # #800000
GRAY_ROW   = colors.Color(211/255, 211/255, 211/255)  # #D3D3D3
WHITE      = colors.white
BLACK      = colors.black

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _clean(val) -> str:
    if val is None: return ""
    s = str(val).strip()
    if s.lower() in ("nan", "none", "00:00:00", "00:00", "0:00", "0"):
        return ""
    return s

def _to_td(s: str) -> timedelta:
    if not s or s.lower() in ("nan", "none", "00:00", "00:00:00", ""):
        return timedelta(0)
    try:
        parts = list(map(int, s.split(":")))
        return timedelta(hours=parts[0], minutes=parts[1],
                         seconds=parts[2] if len(parts) == 3 else 0)
    except:
        return timedelta(0)

# ─────────────────────────────────────────────────────────────────────────────
# GERADOR PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def gerar_pdf(dados_consolidados, colaborador: str, mes: str,
              ano: str, output_path: str = "folha_horas.pdf") -> str:
    
    pts_cm = 28.35
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4), 
        rightMargin=1.8*pts_cm, leftMargin=1.8*pts_cm,
        topMargin=1.9*pts_cm,   bottomMargin=1.9*pts_cm,
    )

    styles = getSampleStyleSheet()
    elems  = []

    # ── Título (Calibri 14 Bold) ─────────────────────────────────────────────
    title_style = ParagraphStyle(
        "TitleMain",
        parent=styles["Normal"],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=14,
        textColor=BLACK,
        alignment=1, # CENTER
        spaceAfter=10,
    )
    elems.append(Paragraph("FOLHA DE HORA EXTRA", title_style))

    # ── Cabeçalho (Calibri 11) ───────────────────────────────────────────────
    hdr_data = [
        ["COLABORADOR:", colaborador.upper(), "MÊS:", mes.upper(), "ANO:", ano]
    ]
    # Útil A4L: 29.7 - 1.8*2 = 26.1 cm
    hdr_widths = [4.0*cm, 10.0*cm, 2.0*cm, 6.0*cm, 2.0*cm, 2.1*cm]
    hdr_table  = Table(hdr_data, colWidths=hdr_widths)
    hdr_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), DEFAULT_FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("ALIGN",    (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",   (0, 0), (-1, -1), "BOTTOM"),
        ("LINEBELOW", (1, 0), (1, 0), 0.5, BLACK),
        ("LINEBELOW", (3, 0), (3, 0), 0.5, BLACK),
        ("LINEBELOW", (5, 0), (5, 0), 0.5, BLACK),
    ]))
    elems.append(hdr_table)
    elems.append(Spacer(1, 0.4*cm))

    # ── Tabela de Dados ──────────────────────────────────────────────────────
    COL_HDR = [
        "DIA", "SEMANA", "DATA",
        "INÍCIO", "INTERVALO", "VOLTA", "TÉRMINO",
        "HORAS", "50 %", "100 %", "OBSERVAÇÃO"
    ]

    total_worked = timedelta(0)
    total_50     = timedelta(0)
    total_100    = timedelta(0)
    destaque_idx = []
    data_rows    = []

    for i, (_, row) in enumerate(dados_consolidados.iterrows()):
        semana = row["semana"]
        is_dest = semana in ("SÁBADO", "DOMINGO", "FERIADO")
        if is_dest:
            destaque_idx.append(i + 1)

        r = [
            _clean(row["data"].strftime("%d")),
            _clean(semana),
            _clean(row["data"].strftime("%d/%m/%Y")),
            _clean(row["inicio"]),
            "", # Intervalo
            "", # Volta
            _clean(row["termino"]),
            _clean(row["horas_trabalhadas"]),
            _clean(row["50%"]),
            _clean(row["100%"]),
            _clean(row["caso"]),
        ]
        data_rows.append(r)

        total_worked += row.get("duracao_td", timedelta(0))
        total_50     += _to_td(row.get("50%", "00:00"))
        total_100    += _to_td(row.get("100%", "00:00"))

    footer = [
        "", "", "", "", "", "", "TOTAL:",
        formatar_timedelta(total_worked),
        formatar_timedelta(total_50),
        formatar_timedelta(total_100),
        ""
    ]

    full_data = [COL_HDR] + data_rows + [footer]

    # Alturas para caber em uma página:
    # Útil A4L: 21.0 - 1.9*2 - ~2.0 (título/hdr) = ~15.2cm
    n_lines = len(full_data)
    row_h   = (15.2 / n_lines) * cm
    
    # Larguras colunas (Soma = 26.1cm)
    col_w = [
        1.0*cm, # Dia
        3.5*cm, # Semana
        2.5*cm, # Data
        1.5*cm, # Início
        1.5*cm, # Int
        1.5*cm, # Vol
        1.5*cm, # Tér
        2.0*cm, # Horas
        1.5*cm, # 50
        1.5*cm, # 100
        8.1*cm  # Obs
    ]

    main_table = Table(full_data, colWidths=col_w, rowHeights=[row_h]*n_lines)

    ts = [
        ("GRID",       (0, 0), (-1, -1), 0.5, BLACK),
        ("FONTNAME",   (0, 0), (-1, -1), DEFAULT_FONT),
        ("FONTSIZE",   (0, 0), (-1, -1), 11),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        # Cabeçalho Vinho com Texto Branco
        ("BACKGROUND", (0, 0), (-1, 0),  WINE),
        ("TEXTCOLOR",  (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",   (0, 0), (-1, 0),  DEFAULT_FONT_BOLD),
    ]

    # Aplicar Gray Row para fins de semana/feriado
    for idx in destaque_idx:
        ts.append(("BACKGROUND", (0, idx), (-1, idx), GRAY_ROW))

    # Estilo Rodapé Total
    ts.append(("FONTNAME", (6, -1), (9, -1), DEFAULT_FONT_BOLD))
    ts.append(("BACKGROUND", (6, -1), (9, -1), WINE))
    ts.append(("TEXTCOLOR",  (6, -1), (9, -1), WHITE))

    # Coluna Observação alinhada à esquerda
    ts.append(("ALIGN", (10, 1), (10, -1), "LEFT"))

    main_table.setStyle(TableStyle(ts))
    elems.append(main_table)

    # Assinaturas
    elems.append(Spacer(1, 0.6*cm))
    sign_data = [["_________________________________", "_________________________________"],
                 ["COLABORADOR", "GESTOR"]]
    sign_table = Table(sign_data, colWidths=[13.0*cm, 13.1*cm])
    sign_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), DEFAULT_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))
    elems.append(sign_table)

    doc.build(elems)
    return output_path
