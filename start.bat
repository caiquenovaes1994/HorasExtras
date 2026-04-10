@echo off
setlocal

:: Nome do ambiente virtual
set VENV_NAME=venv

echo [1/3] Verificando ambiente virtual...
if not exist %VENV_NAME% (
    echo Criando ambiente virtual...
    python -m venv %VENV_NAME%
)

echo [2/3] Instalando/Atualizando dependencias...
call %VENV_NAME%\Scripts\activate
pip install -r requirements.txt

echo [3/3] Iniciando aplicacao na porta 3003...
streamlit run app.py --server.port 3003

echo Aplicacao encerrada.
pause
