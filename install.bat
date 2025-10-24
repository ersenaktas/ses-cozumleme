@echo off
setlocal enabledelayedexpansion

:: Bu betik Python'ın bulunamaması durumunda 3.12 sürümünü kurmaya çalışır.

:: Python yollarını kontrol et
set PYTHON_PATHS=^
C:\Python312\python.exe;^
C:\Python311\python.exe;^
C:\Python310\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe;^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\python.exe

echo Python kurulumu kontrol ediliyor...
set PYTHON_FOUND=
set PYTHON_PATH=

for %%p in (%PYTHON_PATHS%) do (
    if exist "%%p" (
        set PYTHON_PATH=%%p
        set PYTHON_FOUND=1
        goto :found_python
    )
)

:: Python bulunamadı, indir ve kur
if not defined PYTHON_FOUND (
    echo Python bulunamadı! Python indiriliyor...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python_installer.exe'}"
    if errorlevel 1 (
        echo Python indirilemedi! İnternet bağlantınızı kontrol edin.
        pause
        exit /b 1
    )
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

    set PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe
    set PYTHON_FOUND=1
    
    echo Sistem değişkenleri güncelleniyor (Yeni oturumlarda geçerli olacak)...
    setx PATH "%PATH%" /M >nul
)


:found_python
if not defined PYTHON_FOUND (
    echo Python kurulumu ve yol tespiti başarısız oldu! Lütfen manuel kontrol edin.
    pause
    exit /b 1
)

echo Python bulundu: %PYTHON_PATH%

echo Sanal ortam oluşturuluyor...
"%PYTHON_PATH%" -m venv venv
if errorlevel 1 (
    echo Sanal ortam oluşturulamadı!
    echo PYTHON_PATH: "%PYTHON_PATH%" yolu kontrol ediniz.
    pause
    exit /b 1
)

echo Sanal ortam aktifleştiriliyor...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Sanal ortam aktifleştirilemedi!
    pause
    exit /b 1
)

echo Pip güncelleniyor...
python -m pip install --upgrade pip

echo Gerekli paketler yükleniyor...
:: requirements.txt içeriği doğrudan kuruluyor, dosya arama sorunu çözüldü.
pip install openai-whisper deep-translator torch ffmpeg-python gdown tqdm
if errorlevel 1 (
    echo Paket kurulumu başarısız!
    pause
    exit /b 1
)

echo Whisper modeli ve FFmpeg dosyaları kontrol ediliyor...
if not exist "whisper_models\small.pt" (
    echo Whisper modeli indiriliyor...
    python download_dependencies.py
    if errorlevel 1 (
        echo Bağımlılık indirme betiği başarısız oldu!
        pause
        exit /b 1
    )
)

echo Kurulum tamamlandı!
echo Program başlatılıyor...
python ses_coz_4.py
pause
