@echo off
setlocal
cd /d "%~dp0"

if not exist "venv" (
    echo Sanal ortam bulunamadi! Lütfen once install.bat dosyasini calistirin.
    pause
    exit /b 1
)

call "%~dp0venv\Scripts\activate.bat"

:: Whisper modülünü kontrol et
python -m pip show openai-whisper >nul 2>&1
if errorlevel 1 (
    echo openai-whisper modülü eksik! Şimdi kuruluyor...
    python -m pip install openai-whisper
)

echo Program baslatiliyor...
python "%~dp0ses_coz_4.py"
if errorlevel 1 (
    echo Program calistirilirken bir hata olustu!
    pause
    exit /b 1
)

endlocal
pause
