Ses Çözümleme Programı / Speech-to-Text Program

English version below

Bu program, ses dosyalarını metne dönüştürür ve istenirse Türkçeye çevirir.
Whisper modeli otomatik olarak indirilir; sadece FFmpeg dosyasını manuel eklemeniz gerekir.

⚙️ FFmpeg Kurulumu

FFmpeg lisans ve boyut kısıtlamaları nedeniyle depoda bulunmuyor.
Manuel olarak eklemek için:

FFmpeg'in resmi sitesinden
 Windows sürümünü indirin.

ffmpeg.exe dosyasını çıkarın.

Bu dosyayı projenin içindeki ffmpeg klasörüne kopyalayın:

ffmpeg/ffmpeg.exe

🚀 Kurulum ve Çalıştırma

install.bat dosyasını çalıştırın.
Bu işlem:

Python 3.10–3.12 sürümünü arar,

Sanal ortam (venv/) oluşturur,

Gerekli paketleri (openai-whisper, torch, deep-translator vb.) yükler,

Whisper modelini (small.pt) otomatik indirir,

Kurulum tamamlandıktan sonra start.bat dosyasını otomatik olarak başlatır.

Sonraki çalıştırmalarda yalnızca start.bat dosyasını kullanın.

💻 Gereksinimler

Windows 10 veya 11

Python 3.10–3.12 (otomatik kontrol edilir)

En az 2 GB boş disk alanı

İnternet bağlantısı (ilk kurulum için)

❗ Sorun Giderme

Program açılmıyor: install.bat dosyasını tekrar çalıştırın.

Python bulunamadı: Python 3.12+ yükleyin ve yeniden deneyin.

FFmpeg hatası: ffmpeg/ffmpeg.exe dosyasının mevcut olduğundan emin olun.

Model eksik: install.bat modeli otomatik indirir; internet bağlantınızı kontrol edin.

📧 İletişim

Herhangi bir hata veya öneri için:
ersenaktas@gmail.com

Speech-to-Text Program

This program converts audio files into text and optionally translates them into Turkish.
The Whisper model downloads automatically; only FFmpeg must be added manually.

⚙️ FFmpeg Setup

Due to size and licensing limitations, FFmpeg is not included.
To add it manually:

Download the latest Windows version from FFmpeg's official website

Extract the ffmpeg.exe file.

Copy it into the project folder as:

ffmpeg/ffmpeg.exe

🚀 Installation and Usage

Run install.bat. This will:

Check for Python 3.10–3.12,

Create a virtual environment (venv/),

Install required packages,

Automatically download the Whisper model (small.pt),

Launch start.bat automatically after setup.

For later use, just run start.bat.

💻 Requirements

Windows 10 or 11

Python 3.10–3.12

At least 2 GB of free disk space

Internet connection (required for first setup)

❗ Troubleshooting

Program not launching: rerun install.bat.

Python not found: install Python 3.12+.

FFmpeg error: ensure ffmpeg/ffmpeg.exe exists.

Missing model: install.bat downloads it automatically; check your connection.

📧 Contact

For support or feedback:
ersenaktas@gmail.com
