import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import joblib # Jika model disimpan sebagai file .pkl
import os
# Konfigurasi Halaman (Kekhasan)
st.set_page_config(
    page_title="Simulasi Bisnis Pro", 
    page_icon="🚀", 
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# --- KEKHASAN APLIKASI (IDENTITAS & STYLING) ---
st.markdown("""
    <style>
        /* MENGHILANGKAN SEMUA MENU DAN HEADER SEPENUHNYA */
        header {display: none !important;}
        footer {display: none !important;}
        
        /* Menyembunyikan tombol merah dan avatar di pojok kanan bawah */
        .viewerBadge-container {display: none !important;}
        [data-testid="stDecoration"] {display: none !important;}
    </style>
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
st.write("") # Spasi kosong sedikit

# Buat dua kolom: Kiri untuk grafik, Kanan untuk input simulasi
col_kiri, col_kanan = st.columns([1.2, 1])

# Tempatkan Input Simulasi di Kolom Kanan
with col_kanan:
    st.markdown("### 🎛️ Input Simulasi")
    iklan = st.slider("💰 Budget Iklan", 0, 100, 10, format="Rp %d Juta")
    diskon = st.slider("🏷️ Persentase Diskon", 0, 100, 5, format="%d%%")

# 3. Prediksi (Logika What-If)
input_data = np.array([[iklan, diskon]])
prediksi = float(model.predict(input_data)[0])
baseline = 100.0

# 4. Tampilkan Hasil Prediksi dengan st.metric (Tampilan Dashboard Dinamis)
with hasil_container:
    selisih = prediksi - baseline
    st.metric(
        label="Prediksi Keuntungan Skenario Baru", 
        value=f"Rp {prediksi:.2f} Juta", 
        delta=f"{selisih:.2f} Juta (vs Baseline)"
    )

# 5. Visualisasi Perbandingan Interaktif dengan Altair
with col_kiri:
    st.markdown("### 📈 Grafik Perbandingan")
    # Membuat dataframe sederhana untuk grafik
    df_chart = pd.DataFrame({
        "Skenario": ["Baseline", "Skenario Baru"],
        "Keuntungan (Juta)": [baseline, prediksi]
    })
    
    # Menggunakan Altair agar kita bisa mengatur ukuran lebar batang (size)
    chart = alt.Chart(df_chart).mark_bar(size=60, cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
        x=alt.X('Skenario', title=None, axis=alt.Axis(labelAngle=0, labelFontSize=12)),
        y=alt.Y('Keuntungan (Juta)', title='Keuntungan (Juta)'),
        color=alt.Color('Skenario', legend=None, scale=alt.Scale(range=['#5DADE2', '#48C9B0']))
    ).properties(height=320)
    
    # Menampilkan chart
    st.altair_chart(chart, use_container_width=True)