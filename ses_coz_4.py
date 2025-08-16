from tkinter import Tk, filedialog, messagebox, Label, Entry, Button, StringVar, OptionMenu, Checkbutton, BooleanVar, \
    ttk, Frame
import whisper
import os
from deep_translator import GoogleTranslator
import threading
import os, sys

import torch

def safe_load_model(model_path):
    try:
        # Önce weights_only=True ile deneyelim
        return whisper.load_model(model_path)
    except Exception as e:
        # Hata durumunda weights_only=False ile deneyelim
        if "weights_only" in str(e):
            print("Model yükleme yöntemi değiştiriliyor...")
            return whisper.load_model(model_path, device="cpu")
        else:
            raise e

model = safe_load_model(r"whisper_models\small.pt")
def resource_path(relative_path: str) -> str:
    """PyInstaller ile .exe içinde çalışırken doğru yol döndürür."""
    if hasattr(sys, "_MEIPASS"):          # exe içinde çalışıyorsa
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

# ffmpeg'i PATH'e ekle
FFMPEG_EXE = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))
os.environ["PATH"] = os.pathsep.join([os.path.dirname(FFMPEG_EXE), os.environ["PATH"]])


def transcribe_or_translate():
    audio_paths = file_path_var.get().split(";")
    model_size = model_var.get()
    use_translate = translate_var.get()
    output_dir = output_dir_var.get()

    if not audio_paths or audio_paths == [""]:
        messagebox.showerror("Hata", "Geçerli bir ses dosyası seçilmedi.")
        return
    if not output_dir:
        messagebox.showerror("Hata", "Çıktı klasörü seçilmedi.")
        return

    thread = threading.Thread(target=process_audios, args=(audio_paths, model_size, use_translate, output_dir))
    thread.start()


def process_audios(audio_paths, model_size, use_translate, output_dir):
    try:
        total_files = len(audio_paths)
        status_label.config(text="Model yükleniyor...")
        progress_bar['value'] = 0
        root.update_idletasks()
        model = whisper.load_model("small")
        for idx, audio_path in enumerate(audio_paths, start=1):
            if not os.path.exists(audio_path):
                continue
            status_label.config(text=f"{os.path.basename(audio_path)} işleniyor ({idx}/{total_files})...")
            overall_progress = int(((idx-1)/total_files)*100)
            progress_bar['value'] = overall_progress
            root.update_idletasks()
            process_audio(audio_path, model, use_translate, output_dir, idx, total_files)
        status_label.config(text="Tüm dosyalar işlendi!")
        progress_bar['value'] = 100
    except Exception as e:
        status_label.config(text="Hata oluştu!")
        messagebox.showerror("Hata", f"Hata oluştu:\n{str(e)}")
        progress_bar['value'] = 0


def process_audio(audio_path, model, use_translate, output_dir, file_idx, total_files):
    try:
        status_label.config(text=f"Ses çözümlemesi yapılıyor... ({file_idx}/{total_files})")
        progress_bar['value'] += 5
        root.update_idletasks()

        result = model.transcribe(audio_path)
        segments = result["segments"]
        total_segments = len(segments)
        srt_content = ""

        status_label.config(text=f"Altyazı oluşturuluyor... ({file_idx}/{total_files})")
        progress_bar['value'] += 5
        root.update_idletasks()

        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()

            if use_translate:
                try:
                    source = source_lang_var.get()
                    if source == "auto":
                        detected_lang = result.get("language", "en")
                        source = detected_lang
                    text = GoogleTranslator(source=source, target='tr').translate(text)
                except Exception as e:
                    print(f"Çeviri hatası: {e}")
                    text = segment["text"].strip()

            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

            file_progress = 10 + int((i / total_segments) * 70)
            overall_progress = int(((file_idx-1)/total_files)*100 + (file_progress/100)*(100/total_files))
            progress_bar['value'] = overall_progress
            status_label.config(text=f"{os.path.basename(audio_path)}: {i}/{total_segments} satır (%{overall_progress})")
            root.update_idletasks()

        status_label.config(text=f"Dosya kaydediliyor... ({file_idx}/{total_files})")
        progress_bar['value'] = int((file_idx/total_files)*100)
        root.update_idletasks()

        if not os.path.isdir(output_dir):
            status_label.config(text="Geçersiz çıktı klasörü!")
            messagebox.showerror("Klasör Hatası", f"Çıktı klasörü bulunamadı:\n{output_dir}")
            return
        if not os.access(output_dir, os.W_OK):
            status_label.config(text="Klasöre yazılamıyor!")
            messagebox.showerror("İzin Hatası", f"Çıktı klasörüne yazma izni yok:\n{output_dir}")
            return

        srt_path = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_path))[0] + ".srt")
        try:
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt_content)
        except Exception as file_err:
            status_label.config(text="Dosya yazma hatası!")
            messagebox.showerror("Dosya Yazma Hatası", f"SRT dosyası kaydedilemedi:\n{srt_path}\nHata: {file_err}")
            return

        status_label.config(text=f"{os.path.basename(audio_path)} tamamlandı! ({file_idx}/{total_files})")
        root.update_idletasks()

    except Exception as e:
        status_label.config(text="Hata oluştu!")
        messagebox.showerror("Hata", f"Hata oluştu:\n{str(e)}")
        progress_bar['value'] = 0


def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def select_file():
    paths = filedialog.askopenfilenames(filetypes=[("Ses Dosyaları", "*.mp3 *.wav *.m4a *.mp4")])
    if paths:
        file_path_var.set(";".join(paths))


def select_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_dir_var.set(dir_path)


# GUI kısmında değişiklik
root = Tk()
root.title("Altyazı Oluşturucu")
root.geometry("550x450")

file_path_var = StringVar()
model_var = StringVar(value="small") # Sabit small model
translate_var = BooleanVar(value=True)
source_lang_var = StringVar(value="auto") # Kaynak dil için değişken
output_dir_var = StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))

Label(root, text="Ses Dosyası/Dosyaları:").pack()
Entry(root, textvariable=file_path_var, width=60).pack()
Button(root, text="Dosya(lar) Seç", command=select_file).pack(pady=5)

# Model seçimi kaldırıldı, sadece small model kullanılacak
# Label(root, text="Model Boyutu:").pack()
# OptionMenu(root, model_var, "tiny", "base", "small", "medium", "large").pack()

# Dil seçimi için yeni bölüm
Frame(root, height=1, bg="gray").pack(fill="x", pady=10)
Label(root, text="Çeviri Ayarları").pack()

Checkbutton(root, text="Türkçe'ye çevir", variable=translate_var).pack()

# Kaynak dil seçimi
Label(root, text="Kaynak Dil:").pack()
lang_options = ["auto", "en", "ru", "fr", "de", "es", "it", "zh-CN", "ja", "ko", "ar"]
OptionMenu(root, source_lang_var, *lang_options).pack()

Label(root, text="Çıktı Klasörü:").pack()
Entry(root, textvariable=output_dir_var, width=60).pack()
Button(root, text="Klasör Seç", command=select_output_dir).pack(pady=5)

Button(root, text="Altyazı Oluştur (.srt)", command=transcribe_or_translate).pack(pady=10)

# Progress bar ve status
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

status_label = Label(root, text="Hazır")
status_label.pack(pady=5)

Label(root, text="© 2025 ersenaktas@gmail.com", fg="gray").pack(side="bottom", pady=5)

root.mainloop()
