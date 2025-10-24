@echo off
setlocal enabledelayedexpansion

:: === Proje dizinini belirle ===
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo -----------------------------------------
echo  SES COZUMLEME KURULUMU BASLIYOR
echo -----------------------------------------

:: === Python kontrolü ===
set PYTHON_PATH=
for %%p in (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
) do (
    if exist %%p (
        set PYTHON_PATH=%%p
        goto :found_python
    )
)

if not defined PYTHON_PATH (
    echo [HATA] Python bulunamadi! Lutfen Python 3.12+ kurun.
    pause
    exit /b 1
)

:found_python
echo Python bulundu: %PYTHON_PATH%
echo.

:: === Sanal ortam olustur ===
if not exist "%PROJECT_DIR%venv" (
    echo Sanal ortam olusturuluyor...
    "%PYTHON_PATH%" -m venv "%PROJECT_DIR%venv"
)

if not exist "%PROJECT_DIR%venv\Scripts\activate.bat" (
    echo [HATA] Sanal ortam olusmadi!
    pause
    exit /b 1
)

:: === Sanal ortam aktiflesiyor ===
call "%PROJECT_DIR%venv\Scripts\activate.bat"
echo Pip guncelleniyor...
python -m pip install --upgrade pip

:: === Gerekli kutuphaneler ===
echo Gerekli paketler yukleniyor...
pip install openai-whisper deep-translator torch ffmpeg-python gdown tqdm --quiet

:: === Model kontrolu ve indirme ===
echo Whisper modeli kontrol ediliyor...
if not exist "%PROJECT_DIR%whisper_models" mkdir "%PROJECT_DIR%whisper_models"

if not exist "%PROJECT_DIR%whisper_models\small.pt" (
    echo Model indiriliyor (small.pt)...
    python - <<PYCODE
import whisper, shutil, os
path = whisper._download("small")
os.makedirs("whisper_models", exist_ok=True)
shutil.copy(path, "whisper_models/small.pt")
print("Model indirildi -> whisper_models/small.pt")
PYCODE
)

echo.
echo -----------------------------------------
echo  Kurulum tamamlandi!
echo  Program baslatiliyor...
echo -----------------------------------------
echo.

call "%PROJECT_DIR%start.bat"
endlocal
exit /b 0
