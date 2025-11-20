# ====================================================
# StoryBuddy v6.2 - Integrasi Gemini API (Fokus Cerita)
# ====================================================

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from google import genai
from google.genai.errors import APIError, ClientError

# ⚠️ GANTI BARIS INI DENGAN KUNCI API GEMINI BARU ANDA
API_KEY = "AIzaSyBaw54RwMQQ8l4KPN2nwpoB81M2ud_k1NA" 
MODEL_NAME = "gemini-2.5-flash" 

print("🔄 StoryBuddy sedang menginisialisasi koneksi Gemini AI...")

# Inisialisasi Klien Gemini
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

# Penanganan Error 
except ClientError as e:
    AI_CONNECTED = False
    # ClientError memiliki format yang berbeda. Kita ambil pesannya langsung.
    error_message = str(e).split('\n')[0] 
    print(f"❌ Gagal inisialisasi/koneksi API: {error_message}")
    print("💡 **MASALAH UTAMA:** Kunci API kemungkinan tidak valid.")

except Exception as e:
    AI_CONNECTED = False
    print(f"❌ Kesalahan umum saat inisialisasi: {e}")


class StoryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StoryBuddy v6.2 - Generator Cerita Gemini AI")
        self.root.geometry("800x600") 
        self.root.configure(bg="#0d1117")
        self.root.iconbitmap(default=None) 

        # Header
        header = tk.Label(root, text="🧠 StoryBuddy AI ", font=("Consolas", 28, "bold"),
                          bg="#0d1117", fg="#58a6ff")
        header.pack(pady=20)

        sub = tk.Label(root, text="Masukkan dua kata kunci, biarkan Gemini AI membuat cerita!",
                        font=("Segoe UI", 12), bg="#0d1117", fg="#8b949e")
        sub.pack(pady=5)

        # === Konten Utama: Buat Cerita ===
        
        # Input Frame
        frame_kata = tk.Frame(root, bg="#0d1117")
        frame_kata.pack(pady=20)
        
        tk.Label(frame_kata, text="Kata 1:", bg="#0d1117", fg="white", font=("Segoe UI", 11)).grid(row=0, column=0, padx=15)
        self.kata1 = tk.Entry(frame_kata, width=20, font=("Segoe UI", 11))
        self.kata1.grid(row=0, column=1, padx=10)
        
        tk.Label(frame_kata, text="Kata 2:", bg="#0d1117", fg="white", font=("Segoe UI", 11)).grid(row=0, column=2, padx=15)
        self.kata2 = tk.Entry(frame_kata, width=20, font=("Segoe UI", 11))
        self.kata2.grid(row=0, column=3, padx=10)
        
        # Tombol
        tk.Button(root, text="Buat Cerita Epik! ✨", bg="#ff7b72", fg="white", font=("Segoe UI", 12, "bold"),
                  command=self.mulai_cerita).pack(pady=15)
        
        # Status Label
        self.status_cerita = tk.Label(root, text="", bg="#0d1117", fg="#ffa657", font=("Segoe UI", 10))
        self.status_cerita.pack(pady=5)
        
        # Hasil Output
        self.hasil_cerita = scrolledtext.ScrolledText(root, height=20, font=("Georgia", 11),
                                                     bg="#161b22", fg="#f0f6fc", wrap=tk.WORD)
        self.hasil_cerita.pack(fill="both", expand=True, padx=30, pady=10)
        
    def generate(self, prompt):
        """Fungsi untuk memanggil Gemini API."""
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.9
                )
            )
            # Pastikan respons bukan None (misalnya jika diblokir oleh safety settings)
            return response.text if response.text else "❌ Respons kosong. Cerita mungkin diblokir oleh Safety Settings Gemini."

        except ClientError as e:
            error_message = str(e).split('\n')[0]
            return f"❌ ERROR API GEMINI: {error_message}. Cek Kunci API dan koneksi internet Anda."
        except Exception as e:
            return f"❌ ERROR: Terjadi kesalahan yang tidak terduga: {e}"


    def mulai_cerita(self):
        # Cek status koneksi AI
        if not globals().get('AI_CONNECTED', False):
             self.hasil_cerita.delete(1.0, tk.END)
             self.hasil_cerita.insert(tk.END, "❌ Koneksi AI GAGAL. Harap periksa Kunci API Anda dan pastikan koneksi internet stabil.")
             self.status_cerita.config(text="Gagal terhubung ke Gemini API.")
             return
             
        # Jalankan proses generator di thread terpisah agar UI tidak macet
        threading.Thread(target=self.proses_cerita, daemon=True).start()

    def proses_cerita(self):
        k1 = self.kata1.get().strip()
        k2 = self.kata2.get().strip()
        
        if not k1 or not k2:
            self.status_cerita.config(text="Isi dua kata dulu dong 😊")
            return
            
        self.status_cerita.config(text="StoryBuddy sedang bertanya ke Gemini AI... Tunggu beberapa detik")
        self.root.update()
        
        # PROMPT untuk Gemini
        prompt = (
            f"Buat cerita pendek yang sangat kreatif dan unik dalam Bahasa Indonesia, dengan gaya santai remaja. "
            f"Cerita ini wajib menggunakan kata '{k1}' dan '{k2}'. "
            f"Panjang cerita sekitar 5-7 paragraf."
        )
        
        cerita = self.generate(prompt)
        
        self.hasil_cerita.delete(1.0, tk.END)
        self.hasil_cerita.insert(tk.END, cerita)
        self.status_cerita.config(text="Cerita selesai! Dibuat oleh Gemini AI. 🚀")


# Jalankan Aplikasi!
if __name__ == "__main__":
    root = tk.Tk()
    app = StoryGeneratorApp(root)
    root.mainloop()