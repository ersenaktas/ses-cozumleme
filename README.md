# Ses Çözümleme Programı / Speech-to-Text Program

[English version below](#speech-to-text-program)

Bu program, ses dosyalarını metne çevirme ve çeviri yapma işlemlerini gerçekleştirir.

## Önemli Not

Bu repository'de FFmpeg dosyası boyut sınırlaması nedeniyle bulunmamaktadır. Lütfen FFmpeg'i şu adımları izleyerek manuel olarak ekleyin:

1. [FFmpeg'in resmi sitesinden](https://ffmpeg.org/download.html) Windows için olan son sürümü indirin
2. İndirdiğiniz zip/7z dosyasından `ffmpeg.exe` dosyasını çıkarın
3. Dosyayı `ffmpeg/ffmpeg2.exe` olarak projenin içindeki `ffmpeg` klasörüne kopyalayın

## Kurulum Adımları

1. `install.bat` dosyasını yönetici olarak çalıştırın. Bu işlem:
   - Python'u kontrol edecek ve gerekirse kuracak
   - Sanal ortam oluşturacak
   - Gerekli paketleri yükleyecek
   - Whisper modelini ve FFmpeg'i indirecek (eğer yoksa)

2. İlk kurulumdan sonra programı başlatmak için `start.bat` dosyasını kullanın.

## Gereksinimler

- Windows 10 veya 11
- İnternet bağlantısı (ilk kurulum için)
- En az 2GB boş disk alanı

## Sorun Giderme

Eğer program çalışmazsa:
1. Python'un doğru kurulduğundan emin olun
2. İnternet bağlantınızı kontrol edin
3. Antivirüs programınızın kurulumu engellemediğinden emin olun

## İletişim

Herhangi bir sorun yaşarsanız destek için iletişime geçin.

---

# Speech-to-Text Program

This program performs speech-to-text conversion and translation operations.

## Important Note

The FFmpeg file is not included in this repository due to size limitations. Please manually add FFmpeg by following these steps:

1. Download the latest version for Windows from [FFmpeg's official website](https://ffmpeg.org/download.html)
2. Extract the `ffmpeg.exe` file from the downloaded zip/7z file
3. Copy the file to the `ffmpeg` folder in the project as `ffmpeg/ffmpeg2.exe`

## Installation Steps

1. Run the `install.bat` file. This process will:
   - Check for Python and install if necessary
   - Create a virtual environment
   - Install required packages
   - Download Whisper model and FFmpeg (if not present)

2. After initial setup, use `start.bat` to launch the program.

## Requirements

- Windows 10 or 11
- Internet connection (for initial setup)
- At least 2GB free disk space

## Troubleshooting

If the program doesn't work:
1. Make sure Python is installed correctly
2. Check your internet connection
3. Ensure your antivirus isn't blocking the installation

## Contact

If you experience any issues, please reach out for support.
