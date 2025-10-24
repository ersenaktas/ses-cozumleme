from tkinter import Tk, filedialog, messagebox, Label, Entry, Button, StringVar, OptionMenu, Checkbutton, BooleanVar, ttk, Frame
import whisper
import os
import sys
import threading
import torch
from deep_translator import GoogleTranslator


def resource_path(relative_path: str) -> str:
    """PyInstaller ile .exe içinde çalışırken doğru yol döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)


# FFmpeg'i PATH'e ekle
FFMPEG_EXE = resource_path(os.path.join("ffmpeg", "ffmpeg.exe"))
os.environ["PATH"] = os.pathsep.join([os.path.dirname(FFMPEG_EXE), os.environ["PATH"]])

# Cihaz seçimi (GPU varsa otomatik kullanılır)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Whisper modelini sadece bir kez yükle
print(f"Whisper modeli yükleniyor ({DEVICE})...")
try:
    model = whisper.load_model("small", device=DEVICE)
except Exception as e:
    print(f"Model yüklenemedi, CPU ile tekrar deneniyor: {e}")
    model = whisper.load_model("small", device="cpu")


def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"


def process_audio(audio_path, use_translate, output_dir, file_idx, total_files):
    try:
        status_label.config(text=f"Ses çözümlemesi yapılıyor... ({file_idx}/{total_files})")
        root.update_idletasks()

        result = model.transcribe(audio_path)
        segments = result["segments"]
        srt_content = ""

        texts = [seg["text"].strip() for seg in segments]
        translated_texts = []

        if use_translate:
            try:
                source = source_lang_var.get()
                if source == "auto":
                    source = result.get("language", "en")
                translated_texts = GoogleTranslator(source=source, target="tr").translate_batch(texts)
            except Exception as e:
                print(f"Çeviri hatası ({audio_path}): {e}")
                translated_texts = texts
        else:
            translated_texts = texts

        for i, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = translated_texts[i - 1]
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"

        os.makedirs(output_dir, exist_ok=True)
        srt_path = os.path.join(output_dir, os.path.splitext(os.path.basename(audio_path))[0] + ".srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)

        status_label.config(text=f"{os.path.basename(audio_path)} tamamlandı! ({file_idx}/{total_files})")
        root.update_idletasks()

    except Exception as e:
        status_label.config(text=f"Hata: {os.path.basename(audio_path)}")
        messagebox.showerror("İşlem Hatası", f"{audio_path} işlenirken hata oluştu:\n{e}")


def process_audios(audio_paths, use_translate, output_dir):
    try:
        total_files = len(audio_paths)
        progress_bar["value"] = 0
        for idx, audio_path in enumerate(audio_paths, start=1):
            if not os.path.exists(audio_path):
                print(f"Dosya bulunamadı: {audio_path}")
                continue
            process_audio(audio_path, use_translate, output_dir, idx, total_files)
            progress_bar["value"] = int((idx / total_files) * 100)
            root.update_idletasks()

        status_label.config(text="Tüm dosyalar işlendi!")
        progress_bar["value"] = 100
        messagebox.showinfo("Tamamlandı", "Tüm dosyalar başarıyla işlendi.")
    except Exception as e:
        status_label.config(text="Hata oluştu!")
        messagebox.showerror("Hata", str(e))


def transcribe_or_translate():
    audio_paths = file_path_var.get().split(";")
    use_translate = translate_var.get()
    output_dir = output_dir_var.get()

    if not audio_paths or audio_paths == [""]:
        messagebox.showerror("Hata", "Geçerli bir ses dosyası seçilmedi.")
        return
    if not output_dir:
        messagebox.showerror("Hata", "Çıktı klasörü seçilmedi.")
        return

    thread = threading.Thread(target=process_audios, args=(audio_paths, use_translate, output_dir), daemon=True)
    thread.start()


def select_file():
    paths = filedialog.askopenfilenames(filetypes=[("Ses Dosyaları", "*.mp3 *.wav *.m4a *.mp4")])
    if paths:
        file_path_var.set(";".join(paths))


def select_output_dir():
    dir_path = filedialog.askdirectory()
    if dir_path:
        output_dir_var.set(dir_path)


# --- GUI ---
root = Tk()
root.title("Altyazı Oluşturucu")
root.geometry("550x450")

file_path_var = StringVar()
translate_var = BooleanVar(value=True)
source_lang_var = StringVar(value="auto")
output_dir_var = StringVar(value=os.path.join(os.path.expanduser("~"), "Desktop"))

Label(root, text="Ses Dosyası/Dosyaları:").pack()
Entry(root, textvariable=file_path_var, width=60).pack()
Button(root, text="Dosya(lar) Seç", command=select_file).pack(pady=5)

Frame(root, height=1, bg="gray").pack(fill="x", pady=10)
Label(root, text="Çeviri Ayarları").pack()

Checkbutton(root, text="Türkçe'ye çevir", variable=translate_var).pack()

Label(root, text="Kaynak Dil:").pack()
lang_options = ["auto", "en", "fr", "de", "es", "ru", "it", "zh", "ja", "ko", "ar", "tr", "pt", "nl", "sv"]
OptionMenu(root, source_lang_var, *lang_options).pack()

Label(root, text="Çıktı Klasörü:").pack()
Entry(root, textvariable=output_dir_var, width=60).pack()
Button(root, text="Klasör Seç", command=select_output_dir).pack(pady=5)

Button(root, text="Altyazı Oluştur (.srt)", command=transcribe_or_translate).pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

status_label = Label(root, text="Hazır")
status_label.pack(pady=5)

Label(root, text="© 2025 ersenaktas@gmail.com", fg="gray").pack(side="bottom", pady=5)

if __name__ == "__main__":
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
