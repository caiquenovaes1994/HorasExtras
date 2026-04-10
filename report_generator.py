from reportlab.lib             import colors
from reportlab.lib.pagesizes   import A4, landscape
from reportlab.platypus        import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles      import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units        import cm
from datetime                  import datetime, timedelta

from utils import formatar_timedelta

# ─────────────────────────────────────────────────────────────────────────────
# PALETA DE CORES (padrão Accor / planilha de referência)
# ─────────────────────────────────────────────────────────────────────────────
WINE       = colors.Color(128/255,   0,     0)        # #800000 – cabeçalho
GRAY_ROW   = colors.Color(211/255, 211/255, 211/255)  # #D3D3D3 – fim de semana / feriado
WHITE      = colors.white
BLACK      = colors.black
LIGHT_BG   = colors.Color(245/255, 245/255, 245/255)  # linhas pares (levíssimo contraste)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def _to_td(s: str) -> timedelta:
    """Converte string HH:MM[:SS] em timedelta."""
    if not s or s in ("nan", "None", "00:00:00", "00:00"):
        return timedelta(0)
    try:
        parts = list(map(int, s.split(":")))
        return timedelta(hours=parts[0], minutes=parts[1],
                         seconds=parts[2] if len(parts) == 3 else 0)
    except Exception:
        return timedelta(0)


def _clean(val) -> str:
    """Retorna string limpa ou vazio para nulos/zeros."""
    s = str(val).strip() if val is not None else ""
    if s in ("nan", "None", "00:00:00", "00:00", ""):
        return ""
    return s


# ─────────────────────────────────────────────────────────────────────────────
# GERADOR PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def gerar_pdf(dados_consolidados, colaborador: str, mes: str,
              ano: str, output_path: str = "folha_horas.pdf") -> str:
    """
    Gera a Folha de Hora Extra em PDF A4 landscape em uma única página.

    Colunas: Dia | Semana | Data | Início | Intervalo | Volta | Término
             | Horas | 50% | 100% | Observação
    """
    # ── Margens mínimas para caber tudo em uma página ────────────────────────
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        rightMargin=0.6*cm, leftMargin=0.6*cm,
        topMargin=0.6*cm,   bottomMargin=0.6*cm,
    )

    styles  = getSampleStyleSheet()
    elems   = []

    # ── Título ───────────────────────────────────────────────────────────────
    title_style = ParagraphStyle(
        "TitleMain",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=WHITE,
        alignment=1,          # CENTER
        backColor=WINE,
        borderPadding=(4, 0, 4, 0),
    )
    elems.append(Paragraph("FOLHA DE HORA EXTRA", title_style))
    elems.append(Spacer(1, 0.2*cm))

    # ── Cabeçalho (colaborador / mês / ano) ──────────────────────────────────
    hdr_data = [[
        "COLABORADOR:", colaborador.upper(),
        "MÊS:", mes.upper(),
        "ANO:", ano,
    ]]
    hdr_widths = [3.2*cm, 8.5*cm, 1.8*cm, 3.5*cm, 1.4*cm, 1.8*cm]
    hdr_table  = Table(hdr_data, colWidths=hdr_widths)
    hdr_table.setStyle(TableStyle([
        ("FONTNAME",   (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 8),
        ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("BOX",        (1, 0), (1, 0),   0.5, BLACK),
        ("BOX",        (3, 0), (3, 0),   0.5, BLACK),
        ("BOX",        (5, 0), (5, 0),   0.5, BLACK),
    ]))
    elems.append(hdr_table)
    elems.append(Spacer(1, 0.2*cm))

    # ── Construir dados da tabela ─────────────────────────────────────────────
    COL_HDR = [
        "DIA", "SEMANA", "DATA",
        "INÍCIO", "INTERVALO", "VOLTA", "TÉRMINO",
        "HORAS", "50 %", "100 %", "OBSERVAÇÃO",
    ]

    total_worked = timedelta(0)
    total_50     = timedelta(0)
    total_100    = timedelta(0)
    destaque_idx = []   # índices (1-based, pois linha 0 é header) para destacar
    data_rows    = []

    for i, (_, row) in enumerate(dados_consolidados.iterrows()):
        semana = row["semana"]
        is_dest = semana in ("SÁBADO", "DOMINGO", "FERIADO")
        if is_dest:
            destaque_idx.append(i + 1)  # +1 = cabeçalho ocupa índice 0

        r = [
            _clean(row["data"].strftime("%d")),
            _clean(semana),
            _clean(row["data"].strftime("%d/%m/%Y")),
            _clean(row["inicio"]),
            "",                              # Intervalo – campo não rastreado
            "",                              # Volta     – campo não rastreado
            _clean(row["termino"]),
            _clean(row["horas_trabalhadas"]),
            _clean(row["50%"]),
            _clean(row["100%"]),
            _clean(row["caso"]),
        ]
        data_rows.append(r)

        total_worked += row["duracao_td"]
        total_50     += _to_td(row["50%"])
        total_100    += _to_td(row["100%"])

    footer = [
        "", "", "", "", "", "", "TOTAL:",
        formatar_timedelta(total_worked),
        formatar_timedelta(total_50),
        formatar_timedelta(total_100),
        "",
    ]

    full_data = [COL_HDR] + data_rows + [footer]

    # ── Larguras de coluna (soma ≈ 27.2 cm = A4L 29.7 – 2×0.6 margens) ──────
    col_w = [
        0.8*cm,   # Dia
        3.0*cm,   # Semana
        2.2*cm,   # Data
        1.5*cm,   # Início
        1.7*cm,   # Intervalo
        1.7*cm,   # Volta
        1.6*cm,   # Término
        1.8*cm,   # Horas
        1.4*cm,   # 50%
        1.4*cm,   # 100%
        8.6*cm,   # Observação
    ]

    # ── Altura das linhas: calc para 1 página ─────────────────────────────────
    # A4 landscape útil: 21.0cm – 0.6*2 margens – ~2.5 header = 17.3cm para tabela
    # Linhas: 1 header + N dias + 1 rodapé
    n_lines     = len(full_data)
    useful_h_mm = 173  # mm
    row_h_mm    = max(3.5, useful_h_mm / n_lines)
    row_h       = row_h_mm / 10 * cm
    font_size   = max(5.5, min(8.0, row_h_mm * 0.55))

    main_table  = Table(full_data, colWidths=col_w, rowHeights=[row_h] * n_lines)

    # ── Estilo base ───────────────────────────────────────────────────────────
    ts = [
        # Grid geral
        ("GRID",       (0, 0),  (-1, -1), 0.3, BLACK),
        # Fonte
        ("FONTNAME",   (0, 0),  (-1, -1), "Helvetica"),
        ("FONTSIZE",   (0, 0),  (-1, -1), font_size),
        ("ALIGN",      (0, 0),  (-1, -1), "CENTER"),
        ("VALIGN",     (0, 0),  (-1, -1), "MIDDLE"),
        # Cabeçalho Vinho
        ("BACKGROUND", (0, 0),  (-1, 0),  WINE),
        ("TEXTCOLOR",  (0, 0),  (-1, 0),  WHITE),
        ("FONTNAME",   (0, 0),  (-1, 0),  "Helvetica-Bold"),
        # Rodapé  "TOTAL" – células 6–10
        ("BACKGROUND", (6, -1), (9, -1),  WINE),
        ("TEXTCOLOR",  (6, -1), (9, -1),  WHITE),
        ("FONTNAME",   (6, -1), (9, -1),  "Helvetica-Bold"),
        # Coluna Observação alinhada à esquerda
        ("ALIGN",      (10, 1), (10, -1), "LEFT"),
    ]

    # Linhas cinza (fim de semana / feriado) – aplicar ANTES dos estilos de fundo do cabec.
    for idx in destaque_idx:
        ts.append(("BACKGROUND", (0, idx), (-1, idx), GRAY_ROW))

    main_table.setStyle(TableStyle(ts))
    elems.append(main_table)

    doc.build(elems)
    return output_path
