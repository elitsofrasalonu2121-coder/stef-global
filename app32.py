import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sayfa Ayarları
st.set_page_config(
    layout="wide", 
    page_title="STEF Global | Elite Analysis", 
    page_icon="🧬",
    initial_sidebar_state="collapsed"
)

# Profesyonel "Midnight Slate" Teması (Göz yormayan gri-lacivert)
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: #cbd5e1; }
    section[data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1e293b; }
    h1, h2, h3, h4 { color: #38bdf8 !important; }
    div[data-testid="metric-container"] { background-color: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: #94a3b8; }
    .stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom: 2px solid #38bdf8; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (HAMBURGER MENÜ) ---
with st.sidebar:
    st.title("🧬 STEF GLOBAL")
    st.caption("Scientific Decision Support System")
    st.markdown("---")
    
    with st.expander("🌍 PROJECT MISSION", expanded=True):
        st.write("**Target:** *Mugil cephalus*")
        st.write("Modeling the 'Invisible Collapse' through metabolic energy budgets.")

    with st.expander("📚 LITERATURE DATABASE (N=68)"):
        refs = pd.DataFrame({
            "ID": ["REF-01", "REF-02", "REF-03", "REF-04", "REF-05"],
            "Author": ["Pörtner et al.", "Cheung & Pauly", "Claireaux & Lefrançois", "Fry, F.E.J.", "STEF Team"],
            "Finding": ["Oxygen Limitation", "Gill Theory", "Aerobic Scope", "Metabolic Framework", "Starvation Penalty"]
        })
        st.dataframe(refs, hide_index=True)

    with st.expander("🧮 ALGORITHMS"):
        st.latex(r"SMR = a \cdot M^{b} \cdot e^{-E/kT}")
        st.write("Starvation Penalty:")
        st.latex(r"T_{crit} = T_{opt} - 1.07 \cdot (1 - NI)")

# --- ANA EKRAN ---
st.title("STEF GLOBAL: Ecosystem Intelligence")

c1, c2 = st.columns([1, 1])
with c1:
    scenario = st.selectbox("CLIMATE SCENARIO", ["Present Day", "SSP1-2.6 (+1.5°C)", "SSP5-8.5 (+3.2°C)"])
with c2:
    ni = st.slider("NUTRITIONAL INDEX (NI)", 0.0, 1.0, 1.0, 0.1)
    if ni < 0.4: st.error("⚠️ STARVATION PENALTY ACTIVE (-1.07°C)")

# Harita
m = folium.Map(location=[36, 30], zoom_start=4, tiles="OpenStreetMap")
output = st_folium(m, width=900, height=400, key="stef_map")

# --- ANALİZ MOTORU ---
if output['last_clicked']:
    lat, lng = output['last_clicked']['lat'], output['last_clicked']['lng']
    
    temp_shift = 1.5 if "1.5" in scenario else (3.2 if "3.2" in scenario else 0.0)
    base_t = 28 * np.cos(np.deg2rad(lat)) + 5 + temp_shift
    T = max(10, min(36, base_t))
    
    limit = 30.4 if ni < 0.4 else 31.5
    risk = int(min(100, (T/limit)*100 if T < limit else 100))

    st.markdown("---")
    st.subheader(f"📊 6-CORE ANALYSIS DASHBOARD ({lat:.2f}, {lng:.2f})")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Temperature", f"{T:.1f} °C", f"+{temp_shift}°C")
    m2.metric("Risk Score", f"{risk}%", "Metabolic Load")
    m3.metric("Status", "CRITICAL" if risk > 85 else "STABLE")

    tabs = st.tabs(["📈 Metabolic", "🩸 Oxygen", "📉 Threshold", "🗓️ Annual", "🛡️ Margin", "💀 Survival"])
    plt.style.use('dark_background')

    # 1. Metabolic
    with tabs[0]:
        fig, ax = plt.subplots(figsize=(8, 3))
        x = np.linspace(10, 36, 100); y = 50 * np.exp(0.08 * (x - 10))
        ax.plot(x, y, color="#38bdf8", lw=3); ax.axvline(limit, color="red", ls="--")
        ax.scatter([T], [50 * np.exp(0.08 * (T - 10))], color="red", s=100)
        st.pyplot(fig)

    # 2. Oxygen
    with tabs[1]:
        fig, ax = plt.subplots(figsize=(8, 3))
        x = np.linspace(10, 36, 100)
        ax.plot(x, 14 * np.exp(-0.02 * x), color="#4ade80", label="Supply")
        ax.plot(x, 2 * np.exp(0.09 * x), color="#f472b6", label="Demand")
        ax.legend(); st.pyplot(fig)

    # 3. Threshold
    with tabs[2]:
        fig, ax = plt.subplots(figsize=(8, 2))
        ax.barh(["Critical Limit"], [limit], color="#fbbf24")
        ax.set_xlim(20, 35); st.pyplot(fig)

    # 4. Annual
    with tabs[3]:
        fig, ax = plt.subplots(figsize=(8, 3))
        m_x = np.arange(1, 13); t_y = T + 5 * np.sin((m_x - 5) * np.pi / 6)
        ax.plot(m_x, t_y, marker='o', color="#38bdf8"); ax.axhline(limit, color="red", ls="--")
        st.pyplot(fig)

    # 5. Margin
    with tabs[4]:
        fig, ax = plt.subplots(figsize=(8, 2))
        margin = limit - T
        ax.barh(["Safety Margin"], [margin], color="green" if margin > 2 else "red")
        ax.set_xlim(-2, 10); st.pyplot(fig)

    # 6. Survival
    with tabs[5]:
        fig, ax = plt.subplots(figsize=(8, 3))
        years = np.arange(2026, 2036); pop = 100 * np.exp(-(0.05 + risk/500) * (years - 2026))
        ax.plot(years, pop, color="#a78bfa", lw=3); st.pyplot(fig)

    if st.button("📄 GENERATE REPORT"):
        st.success("Analysis finalized for the official record.")
else:
    st.info("👆 Please click on a marine location on the map.")
