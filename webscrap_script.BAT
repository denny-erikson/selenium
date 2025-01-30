@echo off
SETLOCAL

:: Caminho para o diretório onde o ambiente virtual será criado
set VENV_DIR=%~dp0venv

:: Caminho para o script Python
set PYTHON_SCRIPT=%~dp0webscrap.py

:: Caminho para o arquivo zip do ChromeDriver
set CHROMEDRIVER_ZIP=%~dp0chromedriver-win32.zip

:: Caminho para o diretório onde o ChromeDriver será instalado
set CHROMEDRIVER_DIR=%ProgramFiles%\ChromeDriver

:: Verifique se o Python 3 está instalado
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3 não encontrado. Instalando Python 3...
    powershell -Command "Start-Process 'https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe' -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait"
    if %errorlevel% neq 0 (
        echo Falha ao instalar o Python 3. Por favor, instale o Python 3 manualmente.
        pause
        exit /b 1
    )
)

:: Verifique se o pip está instalado
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo pip não encontrado. Instalando pip...
    python -m ensurepip --upgrade
)

:: Verifique se o virtualenv está instalado
where virtualenv >nul 2>&1
if %errorlevel% neq 0 (
    echo virtualenv não encontrado. Instalando virtualenv...
    pip install virtualenv
)

:: Crie o ambiente virtual se não existir
if not exist "%VENV_DIR%" (
    echo Criando o ambiente virtual...
    python -m venv "%VENV_DIR%"
)

:: Ative o ambiente virtual
call "%VENV_DIR%\Scripts\activate"

:: Instalar as dependências
echo Instalando dependências...
pip install selenium
pip install pandas
python.exe -m pip install --upgrade pip


:: Verifique se o ChromeDriver está instalado e instale a partir do arquivo local
if not exist "%CHROMEDRIVER_DIR%\chromedriver.exe" (
    echo ChromeDriver não encontrado. Instalando o ChromeDriver a partir do arquivo local...

    :: Verifique se o arquivo zip do ChromeDriver existe
    if exist "%CHROMEDRIVER_ZIP%" (
        echo Descompactando o ChromeDriver...
        powershell -Command "Expand-Archive -Path '%CHROMEDRIVER_ZIP%' -DestinationPath '%CHROMEDRIVER_DIR%' -Force"
    ) else (
        echo O arquivo %CHROMEDRIVER_ZIP% não foi encontrado. Verifique o arquivo e tente novamente.
        pause
        exit /b 1
    )
)

:: Defina a variável de ambiente para o ChromeDriver
set PATH=%PATH%;%CHROMEDRIVER_DIR%

:: Execute o script Python
echo Executando o script Python...
python "%PYTHON_SCRIPT%"
pause

:: Desative o ambiente virtual
deactivate

:: Manter o Prompt de Comando aberto após a execução
pause

ENDLOCAL
