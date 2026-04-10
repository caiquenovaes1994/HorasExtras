import pandas as pd
from datetime import datetime, time, timedelta
import holidays

def get_dia_semana(data_str):
    dias = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
    data = pd.to_datetime(data_str)
    
    # Verificar feriado (Brasil)
    br_holidays = holidays.Brazil()
    if data in br_holidays:
        return "FERIADO"
    
    return dias[data.weekday()]

def calcular_duracao(inicio_str, termino_str):
    fmt = "%H:%M"
    try:
        t1 = datetime.strptime(inicio_str, fmt)
        t2 = datetime.strptime(termino_str, fmt)
        
        # Lidar com virada de dia (se término < início)
        if t2 < t1:
            t2 += timedelta(days=1)
            
        duracao = t2 - t1
        return duracao
    except Exception:
        return timedelta(0)

def formatar_timedelta(td):
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def agrupar_por_data(df):
    if df.empty:
        return df
    
    # Garantir que as colunas estão no formato correto
    df['data'] = pd.to_datetime(df['data'])
    
    # Agrupar: Menor início e maior término por dia
    grouped = df.groupby('data').agg({
        'inicio': 'min',
        'termino': 'max',
        'caso': lambda x: ', '.join(sorted(list(set([str(i) for i in x if i])))),
        'observacoes': lambda x: ' | '.join([str(i) for i in x if i])
    }).reset_index()
    
    # Adicionar colunas calculadas
    grouped['semana'] = grouped['data'].apply(lambda x: get_dia_semana(x))
    grouped['duracao_td'] = grouped.apply(lambda x: calcular_duracao(x['inicio'], x['termino']), axis=1)
    grouped['horas_trabalhadas'] = grouped['duracao_td'].apply(formatar_timedelta)
    
    # Lógica de 50% vs 100%
    # 100% em Sábados, Domingos e Feriados. 50% em dias úteis.
    def calc_percentual(row):
        is_100 = row['semana'] in ["SÁBADO", "DOMINGO", "FERIADO"]
        if is_100:
            return pd.Series([None, row['horas_trabalhadas']])
        else:
            return pd.Series([row['horas_trabalhadas'], None])
            
    grouped[['50%', '100%']] = grouped.apply(calc_percentual, axis=1)
    
    return grouped.sort_values('data')

def get_periodo_atual():
    """
    Retorna o período de 26 do mês anterior a 25 do mês atual (ou conforme o dia de hoje).
    """
    hoje = datetime.now()
    if hoje.day >= 26:
        inicio = datetime(hoje.year, hoje.month, 26)
        if hoje.month == 12:
            fim = datetime(hoje.year + 1, 1, 25)
        else:
            fim = datetime(hoje.year, hoje.month + 1, 25)
    else:
        if hoje.month == 1:
            inicio = datetime(hoje.year - 1, 12, 26)
        else:
            inicio = datetime(hoje.year, hoje.month - 1, 26)
        fim = datetime(hoje.year, hoje.month, 25)
    return inicio, fim
