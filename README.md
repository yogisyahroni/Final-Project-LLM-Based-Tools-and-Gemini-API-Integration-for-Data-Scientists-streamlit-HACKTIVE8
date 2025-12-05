# AI Chatbot - Final Project HACKTIV8

![Banner](https://img.shields.io/badge/HACKTIV8-Final%20Project-orange)
![Theme](https://img.shields.io/badge/Tema-MAJU%20BARENG%20AI-blue)

Aplikasi Chatbot AI berbasis Streamlit yang dibangun sebagai **Final Project** untuk course **HACKTIV8** dengan tema **"MAJU BARENG AI"**.

Aplikasi ini mengintegrasikan berbagai model LLM (Large Language Models) melalui **OpenRouter** dan **Groq**, dengan antarmuka modern bergaya "Linear" dan fitur penyimpanan riwayat chat lokal menggunakan SQLite.

## 🌟 Fitur Utama

- **Multi-Provider AI**: Mendukung OpenRouter dan Groq.
- **Model Gratis & Berbayar**: Akses ke ribuan model termasuk Llama 3, Gemma, Mistral, dan lainnya.
- **Penyimpanan Lokal**: Riwayat chat tersimpan aman di database SQLite lokal (`chat.db`).
- **UI Modern**: Antarmuka gelap (Dark Mode) dengan gaya *glassmorphism* dan animasi halus.
- **Validasi API Key**: Indikator visual (Hijau/Merah) untuk validitas API Key secara real-time.
- **Parameter Kustom**: Kontrol penuh atas `Temperature` dan `Max Tokens`.
- **Pencarian Model**: Fitur pencarian cepat di dalam dropdown model.

## 🛠️ Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama.
- **Streamlit**: Framework untuk antarmuka web.
- **SQLite**: Database ringan untuk penyimpanan sesi chat.
- **OpenAI SDK**: Wrapper untuk komunikasi dengan API LLM.
- **CSS3**: Kustomisasi tampilan antarmuka.

## 🚀 Cara Menjalankan

1. **Clone Repository**

    ```bash
    git clone https://github.com/yogisyahroni/Final-Project-LLM-Based-Tools-and-Gemini-API-Integration-for-Data-Scientists-streamlit-HACKTIVE8.git
    cd Final-Project-LLM-Based-Tools-and-Gemini-API-Integration-for-Data-Scientists-streamlit-HACKTIVE8
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Jalankan Aplikasi**

    ```bash
    streamlit run app.py
    ```

4. **Konfigurasi**
    - Buka sidebar di sebelah kiri.
    - Pilih Provider (OpenRouter/Groq).
    - Masukkan API Key Anda.
    - Pilih Model dan mulai chatting!

## 📝 Catatan Pengembang

Project ini dibuat untuk mendemonstrasikan integrasi LLM ke dalam aplikasi web interaktif yang ramah pengguna, mendukung visi **MAJU BARENG AI** untuk mendemokratisasi akses ke kecerdasan buatan.

---
**Created by Yogi Syahroni**
