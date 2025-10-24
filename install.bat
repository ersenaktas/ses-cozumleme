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
    echo Python bulunamadı! Lütfen Python 3.12 veya üstü sürümünü kurun.
    pause
    exit /b 1
)

:found_python
echo Python bulundu: %PYTHON_PATH%

echo Sanal ortam oluşturuluyor...
"%PYTHON_PATH%" -m venv "%PROJECT_DIR%venv"
if errorlevel 1 (
    echo Sanal ortam oluşturulamadı!
    pause
    exit /b 1
)

echo Sanal ortam aktifleştiriliyor...
call "%PROJECT_DIR%venv\Scripts\activate.bat"

echo Pip guncelleniyor...
python -m pip install --upgrade pip

echo Gerekli paketler yukleniyor...
pip install openai-whisper deep-translator torch ffmpeg-python gdown tqdm

echo Whisper modeli ve FFmpeg dosyaları kontrol ediliyor...
if not exist "%PROJECT_DIR%whisper_models\small.pt" (
    echo Whisper modeli indiriliyor...
    python "%PROJECT_DIR%download_dependencies.py"
)

echo Kurulum tamamlandi!
pause
exit /b 0
