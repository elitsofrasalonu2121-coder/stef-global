import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import matplotlib.pyplot as plt
import time

# --- SAYFA AYARLARI ---
st.set_page_config(layout="wide", page_title="STEF Global v9.0", page_icon="🌍")

# --- CSS TASARIM ---
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    section[data-testid="stSidebar"] { background-color: #0b1120; border-right: 1px solid #1e293b; }
    .report-box { border: 2px solid white; padding: 20px; background-color: #1e293b; color: white; font-family: monospace; border-radius: 10px;}
    h1, h2, h3 { color: #22d3ee !important; }
</style>
""", unsafe_allow_html=True)

# --- YAN PANEL (MANİFESTO) ---
with st.sidebar:
    st.title("🧬 Project DNA")
    st.caption("Sustainable Thermal & Ecosystem Forecasting System")
    
    with st.expander("🌍 Why This Project?", expanded=True):
        st.markdown("""
        **1. Early Warning:** STEF predicts metabolic collapse *before* mass mortality occurs.
        **2. Starvation Penalty:** Proves that nutritional stress reduces thermal tolerance by **1.07°C**.
        **3. Economic Shield:** Protects the $400B aquaculture industry via AI-driven policy.
        """)
    
    st.markdown("### 🧪 Algorithms")
    st.latex(r"SMR = a \cdot M^{b} \cdot e^{-E/kT}")
    st.info("PRISMA Meta-Analysis: N=68 Papers")

# --- ANA EKRAN ---
st.title("STEF GLOBAL 🌍")
st.markdown("**Real-Time Metabolic Intelligence System** | *Powered by Python*")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Simulation Lab")
    scenario = st.selectbox("IPCC Scenario", ["Present Day", "SSP1-2.6 (+1.5°C)", "SSP5-8.5 (+3.2°C)"])
    temp_shift = 1.5 if "1.5" in scenario else (3.2 if "3.2" in scenario else 0.0)
    
    st.markdown("---")
    ni = st.slider("Nutritional Index (NI)", 0.0, 1.0, 1.0, 0.1)
    
    if ni < 0.4:
        st.error("⚠️ STARVATION PENALTY APPLIED (-1.07°C)")
    else:
        st.success("✅ OPTIMAL NUTRITION")

with col2:
    # Gri kutu sorununu çözen standart harita
    m = folium.Map(location=[20, 0], zoom_start=2)
    output = st_folium(m, width=700, height=400, key="stef_map")

# --- HESAPLAMA MOTORU ---
if output['last_clicked']:
    lat, lng = output['last_clicked']['lat'], output['last_clicked']['lng']
    
    # Fiziksel Hesap
    base_temp = 28 * np.cos(np.deg2rad(lat)) + 5 + temp_shift
    temp = max(15, min(35, base_temp))
    
    # Risk Hesabı
    limit = 30.4 if ni < 0.4 else 31.5
    risk = (temp/25)*30 if temp < 25 else (30+((temp-25)/(limit-25))*60 if temp < limit else 100)
    risk = min(100, int(risk))
    
    # Sonuçlar
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Temperature", f"{temp:.1f}°C")
    m2.metric("Risk Score", f"{risk}%")
    m3.metric("Status", "CRITICAL" if risk > 90 else ("STRESS" if risk > 40 else "OPTIMAL"))
    
    # Grafik ve Rapor
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📈 Metabolic Trend")
        x = np.linspace(15, 35, 100)
        y = 50 * np.exp(0.09 * (x - 15))
        
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')
        
        ax.plot(x, y, color="#22d3ee", lw=3, label="Metabolic Demand")
        ax.axvline(x=limit, color="white", linestyle="--", alpha=0.5, label="Collapse Threshold")
        
        # Hareketli Nokta
        curr_y = 50 * np.exp(0.09 * (temp - 15))
        p_color = "#ef4444" if risk > 80 else "#22d3ee"
        ax.scatter([temp], [curr_y], color=p_color, s=200, edgecolor='white', zorder=5)
        
        ax.set_xlabel("Temperature (°C)", color='white')
        ax.tick_params(colors='white')
        ax.grid(alpha=0.1)
        ax.legend(facecolor='#1e293b', labelcolor='white')
        st.pyplot(fig)
        
    with c2:
        st.subheader("📑 Official Report")
        status_text = "FISHING BAN" if risk > 90 else ("REDUCE EFFORT" if risk > 40 else "MONITOR")
        st.markdown(f"""
        <div class="report-box">
            <h4>STEF ANALYSIS</h4>
            <p>ID: #AX-{int(time.time())}</p>
            <p>LOC: {lat:.2f}, {lng:.2f}</p>
            <p>TEMP: {temp:.1f}°C</p>
            <hr>
            <p style="color: {'#ef4444' if risk > 90 else '#22d3ee'}">
            <b>DECISION: {status_text}</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("👆 Click on the map to start the analysis.")
