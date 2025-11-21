# ====================================================
# SASTRO BUDI - Multi Kategori Kreatif Gemini AI
# Cerpen • Cerpan • Puisi • Pentigraf • Pantun • Naskah Drama
# API KEY BARU ANDA SUDAH SAYA MASUKKAN LANGSUNG!
# ====================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from google import genai
from google.genai.errors import APIError, ClientError

# API KEY BARU ANDA (SUDAH DIGANTI SESUAI PERMINTAAN)
API_KEY = "AIzaSyAGNls_VBvYUPJp5ZeYd8NGecqtaTiUUyA" 

# MODEL YANG PASTI JALAN HARI INI (November 2025)
MODEL_NAME = "gemini-2.5-flash"   # <--- INI YANG BARU & PASTI JALAN HARI INI!

print("🔄 SASTRO BUDI sedang menginisialisasi koneksi Gemini AI...")

# Inisialisasi Klien Gemini (kode lama tetap utuh)
try:
    client = genai.Client(api_key=API_KEY)
    
    # Uji koneksi API dengan permintaan sederhana
    test_response = client.models.generate_content(
        model=MODEL_NAME,
        contents="Sebutkan satu kata kunci saja."
    )
    
    if test_response.text:
        AI_CONNECTED = True
        print("✅ Koneksi Gemini AI berhasil diinisialisasi dan diuji.")
    else:
        AI_CONNECTED = False
        print("❌ Uji koneksi gagal: Respon kosong dari model. Cek Kunci API dan batasan akun Anda.")

except ClientError as e:
    AI_CONNECTED = False
    error_message = str(e).split('\n')[0] 
    print(f"❌ Gagal inisialisasi/koneksi API: {error_message}")
    print("💡 **MASALAH UTAMA:** Kunci API kemungkinan tidak valid.")

except Exception as e:
    AI_CONNECTED = False
    print(f"❌ Kesalahan umum saat inisialisasi: {e}")


class StoryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SASTRO BUDI - Generator Kreatif Gemini AI")
        self.root.geometry("900x750") 
        self.root.configure(bg="#0d1117")

        # Header
        header = tk.Label(root, text="🧠 SASTRO BUDI", font=("Consolas", 30, "bold"),
                          bg="#0d1117", fg="#58a6ff")
        header.pack(pady=20)

        sub = tk.Label(root, text="Pilih kategori + 2 kata kunci → Gemini buatkan karya masterpiece!",
                        font=("Segoe UI", 13), bg="#0d1117", fg="#8b949e")
        sub.pack(pady=5)

        # === TAMBAHAN BARU: Dropdown Kategori ===
        frame_kategori = tk.Frame(root, bg="#0d1117")
        frame_kategori.pack(pady=20)

        tk.Label(frame_kategori, text="Pilih Kategori :", bg="#0d1117", fg="white", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)
        self.kategori = ttk.Combobox(frame_kategori, values=[
            "Cerpen",
            "Cerpan",
            "Puisi",
            "Pentigraf",
            "Pantun",
            "Naskah Drama"
        ], state="readonly", width=25, font=("Segoe UI", 11))
        self.kategori.pack(side="left", padx=15)
        self.kategori.set("Cerpen")  # default

        # Input Frame (kode lama tetap utuh)
        frame_kata = tk.Frame(root, bg="#0d1117")
        frame_kata.pack(pady=20)
        
        tk.Label(frame_kata, text="Kata 1:", bg="#0d1117", fg="white", font=("Segoe UI", 11)).grid(row=0, column=0, padx=15)
        self.kata1 = tk.Entry(frame_kata, width=20, font=("Segoe UI", 11))
        self.kata1.grid(row=0, column=1, padx=10)
        
        tk.Label(frame_kata, text="Kata 2:", bg="#0d1117", fg="white", font=("Segoe UI", 11)).grid(row=0, column=2, padx=15)
        self.kata2 = tk.Entry(frame_kata, width=20, font=("Segoe UI", 11))
        self.kata2.grid(row=0, column=3, padx=10)
        
        # Tombol
        tk.Button(root, text="Buat Karya Epik! ✨", bg="#ff7b72", fg="white", font=("Segoe UI", 13, "bold"),
                  command=self.mulai_cerita).pack(pady=20)
        
        # Status Label
        self.status_cerita = tk.Label(root, text="", bg="#0d1117", fg="#ffa657", font=("Segoe UI", 11))
        self.status_cerita.pack(pady=5)
        
        # Hasil Output
        self.hasil_cerita = scrolledtext.ScrolledText(root, height=22, font=("Georgia", 12),
                                                     bg="#161b22", fg="#f0f6fc", wrap=tk.WORD)
        self.hasil_cerita.pack(fill="both", expand=True, padx=40, pady=20)
        
    def generate(self, prompt):
        """Fungsi untuk memanggil Gemini API (kode lama tetap utuh)"""
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.9,
                    max_output_tokens=8192  # PANJANG BANGET!
                )
            )
            return response.text if response.text else "❌ Respons kosong dari Gemini."

        except ClientError as e:
            error_message = str(e).split('\n')[0]
            return f"❌ ERROR API GEMINI: {error_message}. Cek Kunci API dan koneksi internet Anda."
        except Exception as e:
            return f"❌ ERROR: Terjadi kesalahan yang tidak terduga: {e}"

    def mulai_cerita(self):
        if not globals().get('AI_CONNECTED', False):
             self.hasil_cerita.delete(1.0, tk.END)
             self.hasil_cerita.insert(tk.END, "❌ Koneksi AI GAGAL. Harap periksa Kunci API Anda dan pastikan koneksi internet stabil.")
             self.status_cerita.config(text="Gagal terhubung ke Gemini API.")
             return
             
        threading.Thread(target=self.proses_cerita, daemon=True).start()

    def proses_cerita(self):
        k1 = self.kata1.get().strip()
        k2 = self.kata2.get().strip()
        kategori = self.kategori.get()
        
        if not k1 or not k2:
            self.status_cerita.config(text="Isi dua kata dulu dong 😊")
            return
            
        self.status_cerita.config(text=f"Sedang membuat {kategori} dengan kata '{k1}' & '{k2}'...")
        self.root.update()
        
        # PROMPT BERDASARKAN KATEGORI (SUDAH DIPERBAIKI!)
        base = f"Buat karya kreatif dalam Bahasa Indonesia yang sangat bagus dan orisinal. Wajib menggunakan kata '{k1}' dan '{k2}' secara alami.\n\n"
        
        if kategori == "Cerpen":
            prompt = base + "Buat cerpen lengkap 600-900 kata dengan awal, konflik, klimaks, dan ending memuaskan. Gaya santai remaja."
        elif kategori == "Cerpan":
            prompt = base + "Buat cerpan 3-5 bab singkat. Tiap bab beri judul menarik."
        elif kategori == "Puisi":
            prompt = base + "Buat puisi indah 16-24 baris, penuh makna dan emosi, boleh berima atau bebas."
        elif kategori == "Pentigraf":
            prompt = base + "Buat PENTIGRAF: Baris 1 = 1 kata, Baris 2 = 2 kata, Baris 3 = 3 kata, Baris 4 = 4 kata, Baris 5 = 5 kata. Tema mendalam."
        elif kategori == "Pantun":
            prompt = base + "Buat 4 bait pantun jenaka atau romantis (sampiran + isi)."
        elif kategori == "Naskah Drama":
            prompt = base + "Buat naskah drama pendek 2-4 tokoh. Nama tokoh kapital, dialog hidup, ada konflik kecil, ending lucu/menyentuh."
        else:
            prompt = base + "Buat cerita pendek kreatif 600-800 kata."  # fallback kalau ada bug

        cerita = self.generate(prompt)
        
        self.hasil_cerita.delete(1.0, tk.END)
        self.hasil_cerita.insert(tk.END, cerita)
        self.status_cerita.config(text=f"{kategori} selesai dibuat oleh Gemini AI! ✨")

# Jalankan Aplikasi!
if __name__ == "__main__":
    root = tk.Tk()
    app = StoryGeneratorApp(root)
    root.mainloop()