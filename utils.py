import pandas as pd
from datetime import datetime, date, time, timedelta
import holidays

# Cache por ano para evitar recriação a cada linha
_feriados_cache = {}

def get_feriados(ano: int):
    """Retorna feriados nacionais + estaduais SP + municipais São Paulo/SP."""
    if ano in _feriados_cache:
        return _feriados_cache[ano]

    # Nacionais
    f = holidays.Brazil(state="SP", years=ano)

    # Municipais de São Paulo/SP (fixos que a lib pode não incluir)
    municipais = {
        date(ano, 1, 25): "Aniversário de São Paulo",
        date(ano, 7, 9):  "Revolução Constitucionalista",
        date(ano, 11, 20): "Dia da Consciência Negra",
    }
    f.update(municipais)

    _feriados_cache[ano] = f
    return f

def get_dia_semana(data):
    """Retorna o dia da semana em caixa alta ou FERIADO (incluindo SP municipal)."""
    dias = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
    data_date = data.date() if hasattr(data, 'date') else data
    feriados = get_feriados(data_date.year)
    if data_date in feriados:
        return "FERIADO"
    return dias[data_date.weekday()]

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
    if not td or td.total_seconds() <= 0: return ""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    # Excel usually doesn't show seconds in these sheets unless specific
    return f"{hours:02}:{minutes:02}"

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
        for col in ['inicio', 'termino', 'caso', 'observacoes', 'valor_base_snapshot']: df_agrupado[col] = ""
    else:
        df['data'] = pd.to_datetime(df['data'])
        df = df[(df['data'] >= inicio_p) & (df['data'] <= fim_p)]
        
        df['valor_base_snapshot'] = pd.to_numeric(df['valor_base_snapshot'], errors='coerce').fillna(0.0)
        
        def process_day(g):
            g = g.sort_values("inicio")
            horarios = []
            duracao_total = timedelta(0)
            obs = []
            casos = set()
            vbs = 0.0
            
            for _, row in g.iterrows():
                ti = str(row.get('inicio', ''))
                tf = str(row.get('termino', ''))
                if ti and tf and ti != 'nan' and tf != 'nan':
                    horarios.append(f"{ti} - {tf}")
                    duracao_total += calcular_duracao(ti, tf)
                
                c = str(row.get('caso', ''))
                if c and c.strip() and c.lower() != 'nan' and c.lower() != 'none':
                    casos.add(c.strip())
                
                o = str(row.get('observacoes', ''))
                if o and o.strip() and o.lower() != 'nan' and o.lower() != 'none':
                    obs.append(o.strip())
                
                v = float(row.get('valor_base_snapshot', 0.0))
                if v > vbs:
                    vbs = v
            
            p1 = horarios[0] if len(horarios) > 0 else ""
            p2 = horarios[1] if len(horarios) > 1 else ""
            p3 = horarios[2] if len(horarios) > 2 else ""
            
            overflow = horarios[3:]
            if overflow:
                overflow_str = "Extras: " + "; ".join(overflow)
                obs.insert(0, overflow_str)
            
            return pd.Series({
                'p1': p1,
                'p2': p2,
                'p3': p3,
                'caso': ', '.join(sorted(list(casos))),
                'observacoes': ' | '.join(obs),
                'valor_base_snapshot': vbs,
                'duracao_td': duracao_total
            })

        grouped = df.groupby('data').apply(process_day, include_groups=False).reset_index()
        df_agrupado = pd.merge(df_base, grouped, on='data', how='left').fillna("")
        df_agrupado['duracao_td'] = df_agrupado['duracao_td'].apply(lambda x: x if pd.notnull(x) and x != "" else timedelta(0))
    
    df_agrupado['semana'] = df_agrupado['data'].apply(get_dia_semana)
    df_agrupado['horas_trabalhadas'] = df_agrupado['duracao_td'].apply(formatar_timedelta)
    
    def calc_percentual(row):
        if not row['horas_trabalhadas']: return pd.Series(["", ""])
        # SÁBADOS agora são 50%. Apenas Domingos e Feriados são 100%.
        is_100 = row['semana'] in ["DOMINGO", "FERIADO"]
        if is_100: return pd.Series(["", row['horas_trabalhadas']])
        return pd.Series([row['horas_trabalhadas'], ""])
            
    df_agrupado[['50%', '100%']] = df_agrupado.apply(calc_percentual, axis=1)
    return df_agrupado.sort_values('data')
