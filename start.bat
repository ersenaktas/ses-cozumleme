@echo off
setlocal
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

if not exist "%PROJECT_DIR%venv" (
    echo Sanal ortam bulunamadi! Lutfen once install.bat'i calistirin.
    pause
    exit /b 1
)

call "%PROJECT_DIR%venv\Scripts\activate.bat"

:: whisper yüklü mü kontrol et
python -m pip show openai-whisper >nul 2>&1
if errorlevel 1 (
    echo openai-whisper eksik, kuruluyor...
    python -m pip install openai-whisper --quiet
)

echo Program baslatiliyor...
python "%PROJECT_DIR%ses_coz_4.py"
if errorlevel 1 (
    echo Program calistirilirken bir hata olustu!
    pause
    exit /b 1
)

endlocal
pause
