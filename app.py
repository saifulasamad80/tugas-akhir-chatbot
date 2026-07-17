import streamlit as st
import google.generativeai as genai

# --- PENGATURAN HALAMAN STREAMLIT ---
st.set_page_config(page_title="Arsitek Prompt", page_icon="🏗️")
st.title("🏗️ Arsitek Prompt (Pawang AI)")
st.write("Ubah ide sederhana Anda menjadi Super Prompt berbahasa Inggris yang siap digunakan.")

# --- MEMINTA KUNCI API DARI PENGGUNA ---
# Ini adalah praktik keamanan terbaik agar kunci rahasia Anda tidak bocor.
api_key_input = st.text_input("Masukkan Gemini API Key Anda:", type="password")

if api_key_input:
    # Mengaktifkan akses ke Gemini
    genai.configure(api_key=api_key_input)
    
    # --- KONFIGURASI PARAMETER KREATIF ---
    # Temperature 0.2 memastikan format output selalu rapi dan tidak melenceng.
    konfigurasi_sistem = genai.GenerationConfig(
        temperature=0.2,
        max_output_tokens=4000,
    )
    
    # --- INSTRUKSI UTAMA (SYSTEM PROMPT) ---
    instruksi_batas = """
Anda adalah seorang Arsitek Prompt (Pawang AI) yang jenius. Tugas utama Anda adalah mengubah ide sederhana dari pengguna menjadi sebuah 'Super Prompt' berkualitas tinggi dalam bahasa Inggris.

PERATURAN MUTLAK:
Setiap jawaban yang Anda berikan HARUS dan WAJIB dibagi menjadi 4 bagian berikut tanpa terkecuali. Tuliskan labelnya dengan jelas menggunakan tanda kurung siku:

[ROLE]
(Tentukan peran ahli yang sangat spesifik dan relevan dengan kebutuhan pengguna dalam bahasa Inggris)

[CONTEXT]
(Berikan latar belakang, detail situasi, audiens target, dan batasan masalah dalam bahasa Inggris)

[TASK]
(Berikan instruksi kerja yang sangat detail, langkah demi langkah, dan tajam dalam bahasa Inggris)

[FORMAT]
(Tentukan bagaimana AI harus menyajikan hasilnya, misalnya menggunakan tabel, Markdown, bullet points, atau tone tertentu dalam bahasa Inggris)

Ingat: Jangan menjawab ide pengguna secara langsung. Tugas Anda hanya merakit 'Master Prompt'-nya saja dalam bahasa Inggris berdasarkan 4 struktur di atas!
"""
    
    # Menggunakan model Gemini 3.5 Flash Lite yang lebih canggih
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash",
        generation_config=konfigurasi_sistem,
        system_instruction=instruksi_batas
    )

    # --- ANTARMUKA OBROLAN (CHAT UI) ---
    # Memori jangka pendek untuk menyimpan riwayat chat di layar
    if "riwayat_pesan" not in st.session_state:
        st.session_state.riwayat_pesan = []

    # Menampilkan riwayat chat sebelumnya
    for pesan in st.session_state.riwayat_pesan:
        with st.chat_message(pesan["peran"]):
            st.markdown(pesan["teks"])

    # Kotak input untuk pengguna mengetik ide
    ide_pengguna = st.chat_input("Contoh: Aku mau bikin surat lamaran kerja jadi admin...")

    if ide_pengguna:
        # Menampilkan pesan pengguna di layar
        st.chat_message("user").markdown(ide_pengguna)
        st.session_state.riwayat_pesan.append({"peran": "user", "teks": ide_pengguna})

        # Memanggil Gemini untuk memproses ide
        with st.chat_message("assistant"):
            with st.spinner("Merakit Super Prompt..."):
                try:
                    respons = model.generate_content(ide_pengguna)
                    hasil_teks = respons.text
                    st.markdown(hasil_teks)
                    st.session_state.riwayat_pesan.append({"peran": "assistant", "teks": hasil_teks})
                except Exception as e:
                    # Menangkap pesan error jika terjadi kegagalan sistem
                    st.error(f"Terjadi kesalahan teknis: {e}")
else:
    st.warning("Silakan masukkan API Key Anda terlebih dahulu untuk memulai.")