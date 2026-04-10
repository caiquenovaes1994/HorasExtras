from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from datetime import datetime, timedelta
import os

WINE_COLOR = colors.Color(128/255, 0, 0) # Vinho/Marrom (#800000)
LIGHT_GRAY = colors.Color(211/255, 211/255, 211/255) # #D3D3D3

def gerar_pdf(dados_consolidados, colaborador, mes, ano, output_path="folha_horas.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4), 
                            rightMargin=1*cm, leftMargin=1*cm, 
                            topMargin=0.8*cm, bottomMargin=0.8*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=12,
                               textColor=colors.white, alignment=1, backColor=WINE_COLOR, borderPadding=3)
    elements.append(Paragraph("FOLHA DE HORA EXTRA", title_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # Cabeçalho
    header_data = [["COLABORADOR:", colaborador.upper(), "MÊS REFERENTE:", mes.upper(), "ANO:", ano]]
    header_table = Table(header_data, colWidths=[3.5*cm, 7*cm, 3.5*cm, 4*cm, 2*cm, 2*cm])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (1,0), (1,0), 0.5, colors.black), ('GRID', (3,0), (3,0), 0.5, colors.black),
        ('GRID', (5,0), (5,0), 0.5, colors.black),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.3*cm))
    
    # Tabela
    table_header = [["DIA", "SEMANA", "DATA", "INÍCIO", "INTERVALO", "VOLTA", "TÉRMINO", "HORAS", "50%", "100%", "OBSERVAÇÃO"]]
    rows = []
    total_50 = timedelta(0)
    total_100 = timedelta(0)
    total_worked = timedelta(0)
    
    def to_td(s):
        if not s or s == "00:00:00": return timedelta(0)
        try:
            parts = list(map(int, s.split(':')))
            return timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2] if len(parts)==3 else 0)
        except: return timedelta(0)

    # Identificar linhas para destacar (Fim de semana / Feriado)
    destaque_rows = []
    
    for i, (_, row) in enumerate(dados_consolidados.iterrows()):
        dia = row['data'].strftime('%d')
        data_str = row['data'].strftime('%d/%m/%Y')
        semana = row['semana']
        
        # Verificar destaque
        if semana in ["SÁBADO", "DOMINGO", "FERIADO"]:
            destaque_rows.append(i + 1) # +1 por causa do header
        
        row_data = [
            dia, semana, data_str, row['inicio'], "", "", row['termino'], 
            row['horas_trabalhadas'], row['50%'], row['100%'], row['caso']
        ]
        # Limpar nulos/zeros
        row_data = [str(x) if (x and str(x) not in ["nan", "None", "00:00:00"]) else "" for x in row_data]
        rows.append(row_data)
        
        total_worked += row['duracao_td']
        if row['50%']: total_50 += to_td(row['50%'])
        if row['100%']: total_100 += to_td(row['100%'])
        
    from utils import formatar_timedelta
    footer_row = ["", "", "", "", "", "", "TOTAL:", formatar_timedelta(total_worked), 
                  formatar_timedelta(total_50), formatar_timedelta(total_100), ""]
    
    full_table_data = table_header + rows + [footer_row]
    col_widths = [0.8*cm, 3.2*cm, 2.3*cm, 1.6*cm, 1.8*cm, 1.8*cm, 1.7*cm, 2*cm, 1.4*cm, 1.4*cm, 9.7*cm]
    
    # Cálculo de altura para caber em uma página
    # A4 landscape útil ~19cm (21cm - margens). Header/Títulos ~3cm. Sobram 16cm.
    # ~32 linhas (31 dias + footer). 16 / 32 = 0.5cm por linha.
    row_height = 0.45*cm
    
    main_table = Table(full_table_data, colWidths=col_widths, rowHeights=[row_height]*len(full_table_data))
    
    main_style = [
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.black),
        ('BACKGROUND', (0,0), (-1,0), WINE_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (6,-1), (9,-1), WINE_COLOR),
        ('TEXTCOLOR', (6,-1), (9,-1), colors.white),
        ('FONTNAME', (6,-1), (9,-1), 'Helvetica-Bold'),
    ]
    
    # Adicionar destaques (cinza #D3D3D3)
    for row_idx in destaque_rows:
        main_style.append(('BACKGROUND', (0, row_idx), (-1, row_idx), LIGHT_GRAY))
            
    main_table.setStyle(TableStyle(main_style))
    elements.append(main_table)
    
    doc.build(elements)
    return output_path
