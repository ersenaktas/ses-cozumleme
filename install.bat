@echo off
setlocal enabledelayedexpansion
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo Python kurulumu kontrol ediliyor...
set PYTHON_FOUND=
set PYTHON_PATH=

for %%p in (
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
) do (
    if exist %%p (
        set PYTHON_PATH=%%p
        set PYTHON_FOUND=1
        goto :found_python
    )
)

if not defined PYTHON_FOUND (
    echo Python bulunamadi! Lütfen Python 3.12 veya ustu bir surumu kurun.
    pause
    exit /b 1
)

:found_python
echo Python bulundu: %PYTHON_PATH%

echo Sanal ortam olusturuluyor...
"%PYTHON_PATH%" -m venv "%PROJECT_DIR%venv"
if errorlevel 1 (
    echo Sanal ortam olusturulamadi!
    pause
    exit /b 1
)

echo Sanal ortam aktiflestiriliyor...
call "%PROJECT_DIR%venv\Scripts\activate.bat"

echo Pip guncelleniyor...
python -m pip install --upgrade pip

echo Gerekli paketler yukleniyor...
pip install openai-whisper deep-translator torch ffmpeg-python gdown tqdm

echo Whisper modeli ve FFmpeg dosyalari kontrol ediliyor...
if not exist "%PROJECT_DIR%whisper_models\small.pt" (
    echo Whisper modeli indiriliyor...
    python "%PROJECT_DIR%download_dependencies.py"
)

echo.
echo ================================
echo  Kurulum tamamlandi!
echo  Program baslatiliyor...
echo ================================
echo.

:: start.bat'i ayni dizinden calistir
call "%PROJECT_DIR%start.bat"

endlocal
exit /b 0
