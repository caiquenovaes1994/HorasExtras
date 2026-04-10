import pandas as pd
from datetime import datetime, time, timedelta
import holidays

def get_dia_semana(data):
    """Retorna o dia da semana em caixa alta ou FERIADO."""
    dias = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
    br_holidays = holidays.Brazil()
    if data in br_holidays:
        return "FERIADO"
    return dias[data.weekday()]

def processar_input_horario(s):
    """Converte '0730' em '07:30', ou mantém o formato se já estiver correto."""
    if not s: return "08:00"
    s = str(s).strip().replace(":", "")
    if s.isdigit():
        if len(s) == 1: s = f"0{s}00"
        elif len(s) == 2: s = f"{s}00"
        elif len(s) == 3: s = f"0{s}"
        elif len(s) > 4: s = s[:4]
        
        if len(s) == 4:
            h, m = s[:2], s[2:]
            # Validar limites
            if int(h) > 23: h = "23"
            if int(m) > 59: m = "59"
            return f"{h}:{m}"
    return s if ":" in s else "08:00"

def calcular_duracao(inicio_str, termino_str):
    if not inicio_str or not termino_str: return timedelta(0)
    fmt = "%H:%M"
    try:
        t1 = datetime.strptime(inicio_str, fmt)
        t2 = datetime.strptime(termino_str, fmt)
        if t2 < t1:
            t2 += timedelta(days=1)
        return t2 - t1
    except: return timedelta(0)

def formatar_timedelta(td):
    if not td or td.total_seconds() == 0: return ""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def obter_faixa_periodo(mes_ref_extenso, ano_ref):
    meses_pt = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    try:
        mes_index = meses_pt.index(mes_ref_extenso.upper()) + 1
    except:
        mes_index = datetime.now().month
    
    fim = datetime(int(ano_ref), mes_index, 25)
    if mes_index == 1:
        inicio = datetime(int(ano_ref) - 1, 12, 26)
    else:
        inicio = datetime(int(ano_ref), mes_index - 1, 26)
    return inicio, fim

def agrupar_por_data(df, mes_ref, ano_ref):
    inicio_p, fim_p = obter_faixa_periodo(mes_ref, ano_ref)
    datas_periodo = pd.date_range(start=inicio_p, end=fim_p)
    df_base = pd.DataFrame({'data': datas_periodo})
    
    if df.empty:
        df_agrupado = df_base
        for col in ['inicio', 'termino', 'caso', 'observacoes']: df_agrupado[col] = ""
    else:
        df['data'] = pd.to_datetime(df['data'])
        df = df[(df['data'] >= inicio_p) & (df['data'] <= fim_p)]
        grouped = df.groupby('data').agg({
            'inicio': 'min', 'termino': 'max',
            'caso': lambda x: ', '.join(sorted(list(set([str(i) for i in x if i])))),
            'observacoes': lambda x: ' | '.join([str(i) for i in x if i])
        }).reset_index()
        df_agrupado = pd.merge(df_base, grouped, on='data', how='left').fillna("")
    
    df_agrupado['semana'] = df_agrupado['data'].apply(get_dia_semana)
    df_agrupado['duracao_td'] = df_agrupado.apply(lambda x: calcular_duracao(x['inicio'], x['termino']), axis=1)
    df_agrupado['horas_trabalhadas'] = df_agrupado['duracao_td'].apply(formatar_timedelta)
    
    def calc_percentual(row):
        if row['horas_trabalhadas'] == "": return pd.Series(["", ""])
        is_100 = row['semana'] in ["SÁBADO", "DOMINGO", "FERIADO"]
        if is_100: return pd.Series(["", row['horas_trabalhadas']])
        return pd.Series([row['horas_trabalhadas'], ""])
            
    df_agrupado[['50%', '100%']] = df_agrupado.apply(calc_percentual, axis=1)
    return df_agrupado.sort_values('data')
