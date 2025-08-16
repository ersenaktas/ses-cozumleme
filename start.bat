@echo off
setlocal

:: Sanal ortamın varlığını kontrol et
if not exist "venv" (
    echo Sanal ortam bulunamadı! Lütfen önce install.bat dosyasını çalıştırın.
    pause
    exit /b 1
)

:: Sanal ortamı aktifleştir
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Sanal ortam aktifleştirilemedi!
    pause
    exit /b 1
)

:: Programı başlat
python ses_coz_4.py
if errorlevel 1 (
    echo Program çalıştırılırken bir hata oluştu!
    pause
    exit /b 1
)

endlocal
