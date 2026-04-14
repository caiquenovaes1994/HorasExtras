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
# CONFIGURAÇÃO DE FONTES (INTER)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_BOLD = "Helvetica-Bold"

def _registrar_fontes():
    global DEFAULT_FONT, DEFAULT_FONT_BOLD
    
    # Caminhos Sistema (Usuário caiqu)
    user_fonts_dir = r"C:\Users\caiqu\AppData\Local\Microsoft\Windows\Fonts"
    inter_reg_sys = os.path.join(user_fonts_dir, "InterVariable.ttf")
    
    calibri_path = r"C:\Windows\Fonts\calibri.ttf"
    calibri_bold_path = r"C:\Windows\Fonts\calibrib.ttf"
    
    try:
        # 1. Registrar Regular (Inter)
        if os.path.exists(inter_reg_sys):
            pdfmetrics.registerFont(TTFont('Inter', inter_reg_sys))
            DEFAULT_FONT = 'Inter'
        elif os.path.exists(calibri_path):
            pdfmetrics.registerFont(TTFont('Inter', calibri_path))
            DEFAULT_FONT = 'Inter'
            
        # 2. Registrar Bold (Inter-Bold)
        if os.path.exists(inter_reg_sys):
            pdfmetrics.registerFont(TTFont('Inter-Bold', inter_reg_sys))
            DEFAULT_FONT_BOLD = 'Inter-Bold'
        elif os.path.exists(calibri_bold_path):
            pdfmetrics.registerFont(TTFont('Inter-Bold', calibri_bold_path))
            DEFAULT_FONT_BOLD = 'Inter-Bold'
            
    except Exception as e:
        print(f"Erro ao registrar fontes: {e}")

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
from reportlab.platypus import PageBreak

# ─────────────────────────────────────────────────────────────────────────────
# GERADOR PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def _criar_elementos_usuario(styles, dados_consolidados, plantonista, mes, ano, valor_base):
    """Gera a lista de elementos Platypus para um único colaborador."""
    elems = []
    
    # ── Título (Inter 9 Bold) ─────────────────────────────────────────────
    title_style = ParagraphStyle(
        "TitleMain",
        parent=styles["Normal"],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=9,
        textColor=BLACK,
        alignment=1, # CENTER
        spaceAfter=10,
    )
    elems.append(Paragraph("<b>FOLHA DE HORA EXTRA</b>", title_style))

    # ── Cabeçalho (Inter 7) ───────────────────────────────────────────────
    hdr_data = [
        ["PLANTONISTA:", plantonista.upper(), "MÊS:", mes.upper(), "ANO:", ano]
    ]
    hdr_widths = [2.5*cm, 10.0*cm, 1.2*cm, 4.0*cm, 1.2*cm, 7.2*cm]
    hdr_table  = Table(hdr_data, colWidths=hdr_widths)
    hdr_table.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (0, 0), DEFAULT_FONT_BOLD),
        ("FONTNAME",   (2, 0), (2, 0), DEFAULT_FONT_BOLD),
        ("FONTNAME",   (4, 0), (4, 0), DEFAULT_FONT_BOLD),
        ("FONTNAME",   (1, 0), (1, 0), DEFAULT_FONT),
        ("FONTNAME",   (3, 0), (3, 0), DEFAULT_FONT),
        ("FONTNAME",   (5, 0), (5, 0), DEFAULT_FONT),
        ("BOX",        (0, 0), (-1, -1), 0.5, BLACK),
        ("FONTSIZE",   (0, 0), (-1, -1), 7),
        ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, -1), WINE),
        ("TEXTCOLOR",  (0, 0), (-1, -1), WHITE),
    ]))
    elems.append(hdr_table)
    elems.append(Spacer(1, 0.4*cm))

    # ── Tabela de Dados ──────────────────────────────────────────────────────
    COL_HDR = [
        "DIA", "SEMANA", "DATA",
        "PLANTÃO1", "PLANTÃO2", "PLANTÃO3",
        "HORAS", "50 %", "100 %", "OBSERVAÇÕES"
    ]

    total_worked = timedelta(0)
    total_50     = timedelta(0)
    total_100    = timedelta(0)
    
    val_tot_50   = 0.0
    val_tot_100  = 0.0
    
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
            _clean(row.get("p1")),
            _clean(row.get("p2")),
            _clean(row.get("p3")),
            _clean(row["horas_trabalhadas"]),
            _clean(row["50%"]),
            _clean(row["100%"]),
            _clean(row["observacoes"]),
        ]
        data_rows.append(r)

        total_worked += row.get("duracao_td", timedelta(0))
        t50 = _to_td(row.get("50%", "00:00"))
        t100 = _to_td(row.get("100%", "00:00"))
        
        total_50     += t50
        total_100    += t100
        
        # Financial logic per row (Fallback to user's valor_base if snapshot is 0)
        try:
            row_vbase = float(row.get("valor_base_snapshot", 0.0))
        except:
            row_vbase = 0.0
            
        if row_vbase <= 0.0:
            row_vbase = valor_base
            
        row_vhora = row_vbase / 200.0
        
        if t50.total_seconds() > 0:
            val_tot_50 += (t50.total_seconds() / 3600.0) * row_vhora * 1.5
            
        if t100.total_seconds() > 0:
            val_tot_100 += (t100.total_seconds() / 3600.0) * row_vhora * 2.0

    footer = [
        "", "", "", "", "", "TOTAL:",
        formatar_timedelta(total_worked),
        formatar_timedelta(total_50),
        formatar_timedelta(total_100),
        ""
    ]

    full_data = [COL_HDR] + data_rows + [footer]

    n_lines = len(full_data)
    max_total_h  = 15.5 * cm
    target_row_h = 0.45 * cm
    row_h        = min(target_row_h, max_total_h / n_lines)
    
    col_w = [1.2*cm, 3.4*cm, 2.6*cm, 2.2*cm, 2.2*cm, 2.2*cm, 2.0*cm, 1.5*cm, 1.5*cm, 7.3*cm]
    main_table = Table(full_data, colWidths=col_w, rowHeights=[row_h]*n_lines)

    ts = [
        ("GRID",       (0, 0), (-1, -1), 0.5, BLACK),
        ("FONTNAME",   (0, 0), (-1, -1), DEFAULT_FONT),
        ("FONTSIZE",   (0, 0), (-1, -1), 7),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND", (0, 0), (-1, 0),  WINE),
        ("TEXTCOLOR",  (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",   (0, 0), (-1, 0),  DEFAULT_FONT_BOLD),
    ]

    for idx in destaque_idx:
        ts.append(("BACKGROUND", (0, idx), (-1, idx), GRAY_ROW))

    ts.append(("FONTNAME", (5, -1), (8, -1), DEFAULT_FONT_BOLD))
    ts.append(("BACKGROUND", (5, -1), (8, -1), WINE))
    ts.append(("TEXTCOLOR",  (5, -1), (8, -1), WHITE))
    ts.append(("ALIGN", (0, 1), (-1, -1), "CENTER"))

    main_table.setStyle(TableStyle(ts))
    elems.append(main_table)

    # ── Seção Financeira ──────────────────────────────────
    elems.append(Spacer(1, 0.5*cm))
    val_tot = val_tot_50 + val_tot_100
    
    def f_real(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    fin_data = [
        [f"Total Extra 50%: {f_real(val_tot_50)}", f"Total Extra 100%: {f_real(val_tot_100)}"],
        [f"Total Geral a Receber: {f_real(val_tot)}", ""]
    ]
    
    # Largura total de 13.8 cm para alinhar até a coluna PLANTÃO 3
    fin_table = Table(fin_data, colWidths=[6.9*cm, 6.9*cm])
    fin_table.setStyle(TableStyle([
        # Bordas e Alinhamento
        ("GRID",       (0, 0), (-1, -1), 0.5, BLACK),
        ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        
        # Fontes e Cores
        ("FONTNAME",   (0, 0), (-1, -1), DEFAULT_FONT),
        ("FONTSIZE",   (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",  (0, 0), (-1, -1), BLACK),
        
        # Linha 2: Total Geral (Mesclada e Negrito)
        ("SPAN",       (0, 1), (1, 1)),
        ("FONTNAME",   (0, 1), (1, 1), DEFAULT_FONT_BOLD),
        
        # Ajustes Internos
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(fin_table)
    return elems

def gerar_pdf(dados_consolidados, plantonista: str, mes: str,
              ano: str, valor_base: float, output_path: str = "folha_horas.pdf") -> str:
    
    pts_cm = 28.35
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4), 
        rightMargin=1.8*pts_cm, leftMargin=1.8*pts_cm,
        topMargin=1.0*pts_cm,   bottomMargin=1.0*pts_cm,
    )
    styles = getSampleStyleSheet()
    elems = _criar_elementos_usuario(styles, dados_consolidados, plantonista, mes, ano, valor_base)
    doc.build(elems)
    return output_path

def gerar_pdf_massa(lista_consolidados, mes: str, ano: str, output_path: str) -> str:
    """
    lista_consolidados: List[Tuple(df_agrupado, nome_completo, valor_base)]
    """
    pts_cm = 28.35
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4), 
        rightMargin=1.8*pts_cm, leftMargin=1.8*pts_cm,
        topMargin=1.0*pts_cm,   bottomMargin=1.0*pts_cm,
    )
    styles = getSampleStyleSheet()
    all_elems = []
    
    for i, (df_ag, nome, vbase) in enumerate(lista_consolidados):
        if i > 0:
            all_elems.append(PageBreak())
        all_elems.extend(_criar_elementos_usuario(styles, df_ag, nome, mes, ano, vbase))
        
    doc.build(all_elems)
    return output_path
