from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from datetime import datetime, timedelta
import os

WINE_COLOR = colors.Color(128/255, 0, 0) # Vinho/Marrom (#800000)
LIGHT_GRAY = colors.Color(240/255, 240/255, 240/255)

def gerar_pdf(dados_consolidados, colaborador, mes, ano, output_path="folha_horas.pdf"):
    doc = SimpleDocTemplate(output_path, pagesize=landscape(A4), 
                            rightMargin=1*cm, leftMargin=1*cm, 
                            topMargin=1*cm, bottomMargin=1*cm)
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo do Título Principal
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.white,
        alignment=1, # Center
        backColor=WINE_COLOR,
        borderPadding=5
    )
    
    elements.append(Paragraph("FOLHA DE HORA EXTRA", title_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Cabeçalho de Informações: COLABORADOR, MÊS REFERENTE, ANO
    header_data = [
        ["COLABORADOR:", colaborador.upper(), "MÊS REFERENTE:", mes.upper(), "ANO:", ano]
    ]
    header_table = Table(header_data, colWidths=[4*cm, 8*cm, 4*cm, 4*cm, 2*cm, 2*cm])
    header_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (1,0), (1,0), 1, colors.black),
        ('GRID', (3,0), (3,0), 1, colors.black),
        ('GRID', (5,0), (5,0), 1, colors.black),
        ('BACKGROUND', (1,0), (1,0), LIGHT_GRAY),
        ('BACKGROUND', (3,0), (3,0), LIGHT_GRAY),
        ('BACKGROUND', (5,0), (5,0), LIGHT_GRAY),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))
    
    # Tabela Principal
    # Colunas: DIA, SEMANA, DATA, INÍCIO, INTERVALO, VOLTA, TÉRMINO, HORAS TRABALHADAS, 50%, 100%, OBSERVAÇÃO
    table_header = [
        ["DIA", "SEMANA", "DATA", "INÍCIO", "INTERVALO", "VOLTA", "TÉRMINO", "HORAS\nTRABALHADAS", "Horas a Receber", "", "OBSERVAÇÃO"],
        ["", "", "", "", "", "", "", "", "50%", "100%", ""]
    ]
    
    rows = []
    total_50 = timedelta(0)
    total_100 = timedelta(0)
    total_worked = timedelta(0)
    
    # Helper to convert HH:MM:SS string to timedelta
    def to_td(s):
        if not s or s == "None" or s == "": return timedelta(0)
        try:
            parts = list(map(int, s.split(':')))
            if len(parts) == 3:
                h, m, sec = parts
                return timedelta(hours=h, minutes=m, seconds=sec)
            elif len(parts) == 2:
                h, m = parts
                return timedelta(hours=h, minutes=m)
        except:
            return timedelta(0)
        return timedelta(0)

    for _, row in dados_consolidados.iterrows():
        dia = row['data'].strftime('%d')
        data_str = row['data'].strftime('%d/%m/%Y')
        
        row_data = [
            dia, row['semana'], data_str, row['inicio'], "", "", row['termino'], 
            row['horas_trabalhadas'], row['50%'] or "", row['100%'] or "", row['caso']
        ]
        rows.append(row_data)
        
        # Somar totais utilizando duracao_td (que já deve ser timedelta do utils)
        # E somar 50% e 100% convertendo as strings de volta para timedelta
        total_worked += row['duracao_td']
        if row['50%']: total_50 += to_td(row['50%'])
        if row['100%']: total_100 += to_td(row['100%'])
        
    # Importar helper de formatação
    from utils import formatar_timedelta
    
    footer_row = ["", "", "", "", "", "", "TOTAL:", formatar_timedelta(total_worked), 
                  formatar_timedelta(total_50), formatar_timedelta(total_100), ""]
    
    full_table_data = table_header + rows + [footer_row]
    
    # Larguras das colunas
    col_widths = [1*cm, 3.5*cm, 2.5*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 2.2*cm, 1.8*cm, 1.8*cm, 7.5*cm]
    
    main_table = Table(full_table_data, colWidths=col_widths, repeatRows=2)
    
    # Estilo da Tabela
    main_style = TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        
        # Header primário (Vinho)
        ('BACKGROUND', (0,0), (-1,0), WINE_COLOR),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        
        # Header secundário (Subcolunas 50/100)
        ('BACKGROUND', (8,1), (9,1), WINE_COLOR),
        ('TEXTCOLOR', (8,1), (9,1), colors.white),
        ('FONTNAME', (8,1), (9,1), 'Helvetica-Bold'),
        
        # Mesclagens de Header
        ('SPAN', (8,0), (9,0)), # Horas a Receber
        ('SPAN', (0,0), (0,1)), # Dia
        ('SPAN', (1,0), (1,1)), # Semana
        ('SPAN', (2,0), (2,1)), # Data
        ('SPAN', (3,0), (3,1)), # Início
        ('SPAN', (4,0), (4,1)), # Intervalo
        ('SPAN', (5,0), (5,1)), # Volta
        ('SPAN', (6,0), (6,1)), # Término
        ('SPAN', (7,0), (7,1)), # Horas Trabalhadas
        ('SPAN', (10,0), (10,1)), # Observação
        
        # Rodapé (Totais)
        ('BACKGROUND', (6,-1), (9,-1), WINE_COLOR),
        ('TEXTCOLOR', (6,-1), (9,-1), colors.white),
        ('FONTNAME', (6,-1), (9,-1), 'Helvetica-Bold'),
    ])
    
    # Listras Zebra (alternando entre cinza claro e branco)
    for i in range(2, len(full_table_data) - 1):
        if i % 2 == 0:
            main_style.add('BACKGROUND', (0, i), (-1, i), LIGHT_GRAY)
            
    main_table.setStyle(main_style)
    elements.append(main_table)
    
    # Rodapé do Documento (opcional)
    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph(f"Documento gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Italic']))
    
    # Construir PDF
    doc.build(elements)
    return output_path
