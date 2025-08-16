# Ses Çözümleme Programı

Bu program, ses dosyalarını metne çevirme ve çeviri yapma işlemlerini gerçekleştirir.

## Önemli Not

Bu repository'de FFmpeg dosyası boyut sınırlaması nedeniyle bulunmamaktadır. Lütfen FFmpeg'i şu adımları izleyerek manuel olarak ekleyin:

1. [FFmpeg'in resmi sitesinden](https://ffmpeg.org/download.html) Windows için olan son sürümü indirin
2. İndirdiğiniz zip/7z dosyasından `ffmpeg.exe` dosyasını çıkarın
3. Dosyayı `ffmpeg/ffmpeg2.exe` olarak projenin içindeki `ffmpeg` klasörüne kopyalayın

## Kurulum Adımları

1. `install.bat` dosyasını çalıştırın. Bu işlem:
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
