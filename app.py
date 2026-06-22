import streamlit as st
import numpy as np
import joblib # Jika model disimpan sebagai file .pkl
import os
import matplotlib.pyplot as plt

# Konfigurasi Halaman (Kekhasan)
st.set_page_config(page_title="Simulasi Bisnis Pro", page_icon="🚀", layout="wide")

# --- KEKHASAN APLIKASI (IDENTITAS & STYLING) ---
st.markdown("""
    <div style='text-align: center; background: linear-gradient(to right, #2b5876, #4e4376); padding: 20px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);'>
        <h1 style='color: white; margin: 0; font-family: sans-serif;'>📈 Aplikasi Simulasi Bisnis Interaktif</h1>
        <h4 style='color: #e0e0e0; margin: 5px 0 0 0; font-style: italic;'>Karya Spesial: [sigit] - [2313020027]</h4>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 👑 Identitas Kreator")
st.sidebar.success(
    "**Dibuat Oleh:**\n\n"
    "👤 [sigit]\n\n"
    "🎓 [2313020027]\n\n"
)
st.sidebar.markdown("---")
# ----------------------------------------------
# 1. Load Model (Contoh model regresi minggu ke-4)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'model_bisnis.pkl')
model = joblib.load(model_path)

# 2. Setup Layout Utama
hasil_container = st.container()

# Buat dua kolom: Kiri untuk grafik (1 bagian), Kanan untuk input (1.2 bagian)
col_kiri, col_kanan = st.columns([1, 1.2])

# Tempatkan Input Simulasi di Kolom Kanan
with col_kanan:
    st.subheader("🎛️ Input Kebijakan (Simulasi)")
    st.markdown("Atur nilai di bawah ini untuk melihat perubahannya pada grafik di samping:")
    iklan = st.slider("Budget Iklan", 0, 50, 10)
    diskon = st.slider("Persentase Diskon", 0, 20, 5)

# 3. Prediksi (Logika What-If)
input_data = np.array([[iklan, diskon]])
prediksi = model.predict(input_data)[0]

# 4. Tampilkan Hasil Prediksi Teks di atas (dalam hasil_container)
with hasil_container:
    st.subheader("📊 Hasil Simulasi")
    st.success(f"Keuntungan yang diprediksi: **Rp {prediksi:.2f} Juta**")

# 5. Visualisasi Perbandingan (di letakkan di Kolom Kiri)
with col_kiri:
    fig, ax = plt.subplots(figsize=(4, 3)) # Ukuran grafik tetap kecil
    ax.bar(['Baseline', 'Skenario Baru'], [100, prediksi], color=['#95a5a6', '#2ecc71'])
    ax.set_ylabel("Keuntungan")
    st.pyplot(fig, use_container_width=True)