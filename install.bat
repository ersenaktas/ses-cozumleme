@echo off
setlocal enabledelayedexpansion

:: Python yollarını kontrol et
set PYTHON_PATHS=^
C:\Python312\python.exe;^
C:\Python311\python.exe;^
C:\Python310\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe

echo Python kurulumu kontrol ediliyor...

for %%p in (%PYTHON_PATHS%) do (
    if exist %%p (
        set PYTHON_PATH=%%p
        goto :found_python
    )
)

:: Python bulunamadı, indir ve kur
echo Python bulunamadı! Python indiriliyor...
powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python_installer.exe'}"
if not exist "python_installer.exe" (
    echo Python indirilemedi! İnternet bağlantınızı kontrol edin.
    pause
    exit /b 1
)

echo Python kurulumu başlatılıyor...
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if errorlevel 1 (
    echo Python kurulumu başarısız oldu!
    del python_installer.exe
    pause
    exit /b 1
)
del python_installer.exe

:: Sistem PATH'ini yenile
echo Sistem değişkenleri güncelleniyor...
setx PATH "%PATH%" /M
set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe

:found_python
echo Python bulundu: %PYTHON_PATH%

echo Sanal ortam oluşturuluyor...
"%PYTHON_PATH%" -m venv venv
if errorlevel 1 (
    echo Sanal ortam oluşturulamadı!
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Sanal ortam aktifleştirilemedi!
    pause
    exit /b 1
)

echo Pip güncelleniyor...
python -m pip install --upgrade pip

echo Gerekli paketler yükleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo Paket kurulumu başarısız!
    pause
    exit /b 1
)

echo Whisper modeli ve FFmpeg dosyaları kontrol ediliyor...
if not exist "whisper_models\small.pt" (
    echo Whisper modeli indiriliyor...
    python download_dependencies.py
)

echo Kurulum tamamlandı!
echo Program başlatılıyor...
python ses_coz_4.py
pause
