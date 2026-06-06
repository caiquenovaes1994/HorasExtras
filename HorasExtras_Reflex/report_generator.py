import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from . import time_utils

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO DE FONTES (HELVETICA)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_BOLD = "Helvetica-Bold"

def _registrar_fontes():
    # Passamos a utilizar Helvetica nativo do PDF que garante Bold perfeito 
    # nos cabeçalhos e Total a Receber, sem precisar carregar TTFs variáveis.
    pass

_registrar_fontes()

# ─────────────────────────────────────────────────────────────────────────────
# PALETA DE CORES
# ─────────────────────────────────────────────────────────────────────────────
WINE       = colors.Color(128/255,   0,     0)        # #800000
GRAY_ROW   = colors.Color(211/255, 211/255, 211/255)  # #D3D3D3
WHITE      = colors.white
BLACK      = colors.black

def _clean(val) -> str:
    if val is None: return ""
    s = str(val).strip()
    if s.lower() in ("nan", "none", "00:00:00", "00:00", "0:00", "0"):
        return ""
    return s

def format_td(td: timedelta) -> str:
    if not td or td.total_seconds() <= 0: return ""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"

def agrupar_para_pdf(registros: list[dict], mes: str, ano: str) -> list[dict]:
    """
    Recebe os chamados brutos do BD e agrupa por dia, gerando P1, P2, P3 e as horas.
    Esperado que 'registros' tenha: 'data' (datetime object), 'inicio', 'termino', 'observacoes'.
    """
    agrupado = {}
    
    inicio_p, fim_p = time_utils.obter_faixa_periodo(mes, int(ano))
    curr = inicio_p.date()
    end = fim_p.date()
    
    # Preenche todos os dias do período (mesmo sem plantão)
    while curr <= end:
        dt_str = curr.strftime("%Y-%m-%d")
        dt_obj = datetime(curr.year, curr.month, curr.day)
        agrupado[dt_str] = {
            "data": dt_obj,
            "semana": time_utils.get_dia_semana(dt_obj),
            "plantonistas": [],
            "duracao_td": timedelta(0),
            "obs": [],
            "100%": timedelta(0),
            "50%": timedelta(0),
            "val_100": 0.0,
            "val_50": 0.0,
        }
        curr += timedelta(days=1)
    
    # Preenche com os dados reais
    for c in registros:
        d = c["data"]
        dt_str = d.strftime("%Y-%m-%d")
        
        # Ignora se for fora do período (safety check)
        if dt_str not in agrupado:
            continue
        
        inicio = time_utils.processar_input_horario(c["inicio"])
        termino = time_utils.processar_input_horario(c["termino"])
        agrupado[dt_str]["plantonistas"].append(f"{inicio}-{termino}")
        
        duracao = time_utils.calcular_duracao(c["inicio"], c["termino"])
        agrupado[dt_str]["duracao_td"] += duracao
        
        semana = agrupado[dt_str]["semana"]
        
        # Recupera o snapshot ou usa o fallback
        snapshot = c.get("valor_base_snapshot")
        if snapshot is None or snapshot == "" or snapshot == "0.0":
            snapshot = str(c.get("valor_base_fallback", "0.0"))
        try:
            vbase = float(snapshot)
        except:
            vbase = 0.0
            
        dur_secs = duracao.total_seconds()
        val_hora = vbase / 200.0
        
        if semana in ["DOMINGO", "FERIADO"]:
            agrupado[dt_str]["100%"] += duracao
            agrupado[dt_str]["val_100"] += (dur_secs / 3600.0) * val_hora * 2.0
        else:
            agrupado[dt_str]["50%"] += duracao
            agrupado[dt_str]["val_50"] += (dur_secs / 3600.0) * val_hora * 1.5
            
        if c["observacoes"]:
            agrupado[dt_str]["obs"].append(c["observacoes"])
            
    # Formata a lista para o PDF
    lista_final = []
    for dt_str in sorted(agrupado.keys()):
        item = agrupado[dt_str]
        
        p = item["plantonistas"]
        p1 = p[0] if len(p) > 0 else ""
        p2 = p[1] if len(p) > 1 else ""
        p3 = " / ".join(p[2:]) if len(p) > 2 else ""
        
        lista_final.append({
            "data": item["data"],
            "semana": item["semana"],
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "duracao_td": item["duracao_td"],
            "horas_trabalhadas": format_td(item["duracao_td"]),
            "50_td": item["50%"],
            "100_td": item["100%"],
            "50%": format_td(item["50%"]),
            "100%": format_td(item["100%"]),
            "observacoes": " | ".join(item["obs"])
        })
        
    return lista_final

def _criar_elementos_usuario(styles, registros_raw: list[dict], plantonista: str, mes: str, ano: str, valor_base: float):
    elems = []
    
    title_style = ParagraphStyle(
        "TitleMain",
        parent=styles["Normal"],
        fontName=DEFAULT_FONT_BOLD,
        fontSize=9,
        textColor=BLACK,
        alignment=1,
        spaceAfter=10,
    )
    elems.append(Paragraph("<b>FOLHA DE HORA EXTRA</b>", title_style))

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
    
    # Executa o agrupamento de chamados para o layout de impressão preenchendo todos os dias
    dados_agrupados = agrupar_para_pdf(registros_raw, mes, ano)

    for i, row in enumerate(dados_agrupados):
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
            _clean(row.get("horas_trabalhadas")),
            _clean(row.get("50%")),
            _clean(row.get("100%")),
            _clean(row.get("observacoes")),
        ]
        data_rows.append(r)

        total_worked += row.get("duracao_td", timedelta(0))
        t50 = row.get("50_td", timedelta(0))
        t100 = row.get("100_td", timedelta(0))
        
        total_50  += t50
        total_100 += t100
        
        val_tot_50 += row.get("val_50", 0.0)
        val_tot_100 += row.get("val_100", 0.0)

    footer = [
        "", "", "", "", "", "TOTAL:",
        format_td(total_worked),
        format_td(total_50),
        format_td(total_100),
        ""
    ]

    full_data = [COL_HDR] + data_rows + [footer]

    n_lines = len(full_data)
    max_total_h  = 15.5 * cm
    target_row_h = 0.45 * cm
    row_h        = min(target_row_h, max_total_h / max(1, n_lines))
    
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

    elems.append(Spacer(1, 0.5*cm))
    val_tot = val_tot_50 + val_tot_100
    
    def f_real(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    fin_data = [
        [f"Total Extra 50%: {f_real(val_tot_50)}", f"Total Extra 100%: {f_real(val_tot_100)}"],
        [f"Total Geral a Receber: {f_real(val_tot)}", ""]
    ]
    
    fin_table = Table(fin_data, colWidths=[6.9*cm, 6.9*cm])
    fin_table.setStyle(TableStyle([
        ("GRID",       (0, 0), (-1, -1), 0.5, BLACK),
        ("ALIGN",      (0, 0), (-1, -1), "LEFT"),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("FONTNAME",   (0, 0), (-1, -1), DEFAULT_FONT),
        ("FONTSIZE",   (0, 0), (-1, -1), 8),
        ("TEXTCOLOR",  (0, 0), (-1, -1), BLACK),
        ("SPAN",       (0, 1), (1, 1)),
        ("FONTNAME",   (0, 1), (1, 1), DEFAULT_FONT_BOLD),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(fin_table)
    return elems

def gerar_pdf(registros_raw: list[dict], plantonista: str, mes: str, ano: str, valor_base: float, output_path: str = "folha_horas.pdf") -> str:
    pts_cm = 28.35
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4), 
        rightMargin=1.8*pts_cm, leftMargin=1.8*pts_cm,
        topMargin=1.0*pts_cm,   bottomMargin=1.0*pts_cm,
    )
    styles = getSampleStyleSheet()
    elems = _criar_elementos_usuario(styles, registros_raw, plantonista, mes, ano, valor_base)
    doc.build(elems)
    return output_path

def gerar_pdf_massa(lista_consolidados: list[tuple[list[dict], str, float]], mes: str, ano: str, output_path: str) -> str:
    """
    lista_consolidados: lista de tuplas contendo: (registros_raw, nome_completo, valor_base)
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
    
    for i, (regs_raw, nome, vbase) in enumerate(lista_consolidados):
        if i > 0:
            all_elems.append(PageBreak())
        all_elems.extend(_criar_elementos_usuario(styles, regs_raw, nome, mes, ano, vbase))
        
    doc.build(all_elems)
    return output_path
