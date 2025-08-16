import gdown
import requests
import os
import zipfile
from tqdm import tqdm
import urllib.request

# Whisper model'ini indir
if not os.path.exists("whisper_models/small.pt"):
    print("Whisper modeli indiriliyor...")
    os.makedirs("whisper_models", exist_ok=True)
    # OpenAI'nin resmi model dosyasını indir
    url = "https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt"
    print(f"Whisper modeli indiriliyor: {url}")
    
    import requests
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open("whisper_models/small.pt", 'wb') as file, tqdm(
        desc="small.pt",
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

# FFmpeg'i indir
if not os.path.exists("ffmpeg/ffmpeg.exe"):
    print("\nFFmpeg indiriliyor...")
    os.makedirs("ffmpeg", exist_ok=True)
    
    # FFmpeg'i doğrudan exe olarak indir
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    print(f"FFmpeg indiriliyor: {ffmpeg_url}")
    
    urllib.request.urlretrieve(
        ffmpeg_url,
        "ffmpeg_latest.zip"
    )
    
    # Zip'i aç
    print("\nFFmpeg çıkartılıyor...")
    with zipfile.ZipFile("ffmpeg_latest.zip", 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.endswith('ffmpeg.exe'):
                zip_ref.extract(file, 'ffmpeg_temp')
                # Dosyayı final konumuna taşı
                import shutil
                shutil.move(os.path.join('ffmpeg_temp', file), 'ffmpeg/ffmpeg.exe')
                break
    
    # Geçici dosyaları temizle
    import shutil
    if os.path.exists("ffmpeg_temp"):
        shutil.rmtree("ffmpeg_temp")
    os.remove("ffmpeg_latest.zip")

print("\nDosyalar başarıyla indirildi!")
