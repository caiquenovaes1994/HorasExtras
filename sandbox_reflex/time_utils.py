import dateutil.easter
import holidays
from datetime import datetime, date, timedelta

# Cache por ano para evitar recriação a cada linha
_feriados_cache = {}

def get_feriados(ano: int):
    """Retorna feriados nacionais + estaduais SP + municipais São Paulo/SP."""
    if ano in _feriados_cache:
        return _feriados_cache[ano]

    f = holidays.country_holidays("BR", subdiv="SP", years=ano)

    # Municipais de São Paulo/SP (fixos)
    municipais = {
        date(ano, 1, 25): "Aniversário de São Paulo",
        date(ano, 7, 9):  "Revolução Constitucionalista",
        date(ano, 11, 20): "Dia da Consciência Negra",
    }

    # Feriados móveis (Carnaval e Corpus Christi)
    try:
        pascoa = dateutil.easter.easter(ano)
        carnaval = pascoa - timedelta(days=47)
        corpus_christi = pascoa + timedelta(days=60)
        municipais[carnaval] = "Carnaval"
        municipais[corpus_christi] = "Corpus Christi"
    except Exception as e:
        print(f"Erro ao calcular feriados móveis para o ano {ano}: {e}")

    for d, name in municipais.items():
        f[d] = name

    _feriados_cache[ano] = f
    return f

def get_dia_semana(data_obj) -> str:
    """Retorna o dia da semana em caixa alta ou FERIADO (incluindo SP municipal)."""
    dias = ["SEGUNDA-FEIRA", "TERÇA-FEIRA", "QUARTA-FEIRA", "QUINTA-FEIRA", "SEXTA-FEIRA", "SÁBADO", "DOMINGO"]
    data_date = data_obj.date() if isinstance(data_obj, datetime) else data_obj
    feriados = get_feriados(data_date.year)
    if data_date in feriados:
        return "FERIADO"
    return dias[data_date.weekday()]

def processar_input_horario(s: str) -> str:
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
            if int(h) > 23: h = "23"
            if int(m) > 59: m = "59"
            return f"{h}:{m}"
    return s if ":" in s else "08:00"

def calcular_duracao(inicio_str: str, termino_str: str) -> timedelta:
    if not inicio_str or not termino_str: 
        return timedelta(0)
    
    inicio_str = processar_input_horario(inicio_str)
    termino_str = processar_input_horario(termino_str)
    
    fmt = "%H:%M"
    try:
        t1 = datetime.strptime(inicio_str, fmt)
        t2 = datetime.strptime(termino_str, fmt)
        if t2 < t1:
            t2 += timedelta(days=1)
        return t2 - t1
    except:
        return timedelta(0)

def formatar_timedelta(td: timedelta) -> str:
    if not td or td.total_seconds() <= 0: 
        return "00:00"
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}"

def obter_faixa_periodo(mes_ref_extenso: str, ano_ref: int) -> tuple[datetime, datetime]:
    meses_pt = ["JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO", 
                "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO"]
    try:
        mes_index = meses_pt.index(mes_ref_extenso.upper()) + 1
    except ValueError:
        mes_index = datetime.now().month
    
    fim = datetime(int(ano_ref), mes_index, 25, 23, 59, 59)
    if mes_index == 1:
        inicio = datetime(int(ano_ref) - 1, 12, 26, 0, 0, 0)
    else:
        inicio = datetime(int(ano_ref), mes_index - 1, 26, 0, 0, 0)
    return inicio, fim
