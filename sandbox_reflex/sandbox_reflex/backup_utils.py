import os
import glob
import csv
from datetime import datetime
from sqlmodel import select

EXPORT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "exports")

def backup_tabela(session, model, table_name: str):
    """
    Gera um backup CSV da tabela fornecida e mantém apenas os 10 mais recentes.
    Lê diretamente do banco via session.
    """
    try:
        records = session.exec(select(model)).all()
        if not records:
            return
            
        os.makedirs(EXPORT_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{table_name}_{timestamp}.csv"
        file_path = os.path.join(EXPORT_DIR, file_name)
        
        data = []
        for r in records:
            if hasattr(r, "dict"):
                data.append(r.dict())
            else:
                data.append(dict(r))
                
        if not data:
            return
            
        keys = data[0].keys()
        
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(data)
        
        # Rotação: manter no máximo 10 arquivos
        pattern = os.path.join(EXPORT_DIR, f"{table_name}_*.csv")
        files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
        
        for f in files[10:]:
            try:
                os.remove(f)
            except:
                pass
    except Exception as e:
        print(f"Erro ao gerar backup da tabela {table_name}: {e}")
