"""
ICU 72h Mortality Risk Dashboard — Pastel Aesthetic
Run with: streamlit run 6.Dashboard.py
"""

import numpy as np
import pandas as pd
import joblib
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')

# Force sidebar open regardless of stored browser state
st.set_page_config(
    page_title="ICU Mortality Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

#MainMenu, footer, header { visibility: hidden; }

/* ── Global font + background ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f7f3ee;
}
.stApp { background: #f7f3ee !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ddd5f0 0%, #e8dff5 60%, #d5e8e0 100%) !important;
    border-right: 1px solid #c9bfe8 !important;
}
section[data-testid="stSidebar"] p { color: #2d2d3a; }
section[data-testid="stSidebar"] span { color: #2d2d3a; }
section[data-testid="stSidebar"] label { color: #2d2d3a !important; }

/* ── Sidebar toggle arrow ── */
[data-testid="collapsedControl"] {
    background-color: #c9bfe8 !important;
    border-radius: 0 8px 8px 0 !important;
}
[data-testid="collapsedControl"] svg path { fill: #2d2d3a !important; }

/* ── Top header ── */
.top-header {
    background: linear-gradient(135deg, #e8dff5 0%, #d5e8e0 100%);
    padding: 20px 28px;
    border-radius: 16px;
    margin-bottom: 24px;
    border: 1px solid #c9bfe8;
    box-shadow: 0 4px 16px rgba(168,140,210,0.12);
}
.top-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7em;
    font-weight: 400;
    color: #2d2d3a;
    margin: 0 0 4px 0;
}
.top-header .subtitle { font-size: 0.88em; color: #5a5a72; margin: 0; }

/* ── Stat cards ── */
.stat-card {
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    margin-bottom: 16px;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.stat-card .s-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.1em;
    font-weight: 400;
    margin: 6px 0 4px 0;
}
.stat-card .s-label {
    font-size: 0.75em;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a5a72;
}

/* ── Section cards ── */
.section-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 24px;
    margin-bottom: 20px;
    border: 1px solid #e8e2f4;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05em;
    font-weight: 400;
    color: #2d2d3a;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 2px solid #ede8f5;
}

/* ── Risk banner ── */
.risk-banner {
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 20px;
    border: 2px solid;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.risk-banner h2 {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9em;
    font-weight: 400;
    margin: 0 0 6px 0;
    color: #2d2d3a;
}
.risk-banner p { margin: 0; font-size: 1.05em; color: #2d2d3a; }

/* ── Alert boxes ── */
.alert-crit { background:#fdecea; border-left:4px solid #e07070; padding:14px 16px; border-radius:10px; margin:8px 0; color:#2d2d3a; }
.alert-warn { background:#fef6e4; border-left:4px solid #e8b86d; padding:14px 16px; border-radius:10px; margin:8px 0; color:#2d2d3a; }
.alert-ok   { background:#eaf6f0; border-left:4px solid #7bc4a0; padding:12px 16px; border-radius:10px; margin:8px 0; color:#2d2d3a; }
.alert-rec  { background:#eaf0fb; border-left:4px solid #7da8d8; padding:14px 16px; border-radius:10px; margin:8px 0; color:#2d2d3a; }

/* ── Metrics ── */
div[data-testid="metric-container"] {
    background: #f4f0fb;
    border-radius: 12px;
    padding: 12px 14px;
    border: 1px solid #ddd5f0;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #a8c5b5 0%, #8fb5a5 100%) !important;
    color: #2d2d3a !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1em !important;
    padding: 12px 20px !important;
    box-shadow: 0 2px 8px rgba(168,197,181,0.4) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #96b5a5 0%, #7da595 100%) !important;
    box-shadow: 0 4px 14px rgba(168,197,181,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Dropdowns ── */
div[data-baseweb="select"] > div {
    background-color: #f4f0fb !important;
    border-color: #c9bfe8 !important;
    border-radius: 10px !important;
    color: #2d2d3a !important;
}
ul[data-baseweb="menu"] { background-color: #f4f0fb !important; }
ul[data-baseweb="menu"] li { background-color: #f4f0fb !important; color: #2d2d3a !important; }
ul[data-baseweb="menu"] li:hover { background-color: #ddd5f0 !important; }

/* ── Radio ── */
div[data-baseweb="radio"] div[role="radio"] { border-color: #a890d0 !important; }
div[data-baseweb="radio"] div[aria-checked="true"] {
    background-color: #a890d0 !important;
    border-color: #a890d0 !important;
}

/* ── Slider ── */
div[data-baseweb="slider"] div[role="slider"] {
    background-color: #a8c5b5 !important;
    border-color: #a8c5b5 !important;
}
div[data-baseweb="slider"] [data-testid="stSliderTrackActive"] {
    background-color: #a8c5b5 !important;
}

/* ── Divider ── */
hr { border-color: #e0d8f0 !important; }

/* ── Footer ── */
.footer {
    font-size: 0.75em;
    color: #8888a0;
    margin-top: 28px;
    text-align: center;
    padding: 12px;
    background: #eee8f8;
    border-radius: 10px;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    background: linear-gradient(135deg, #c9bfe8, #b5d5c8);
    padding: 22px 16px;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 16px;
}

/* ── Fix Plotly SVG text (don't let global CSS wash it out) ── */
svg text { fill: #2d2d3a !important; }

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LOAD MODEL & DATA
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        model     = joblib.load('icu_mortality_model.pkl')
        threshold = joblib.load('icu_mortality_threshold.pkl')
        return model, float(threshold), False
    except FileNotFoundError:
        return None, 0.143, True

@st.cache_data
def load_ref():
    try:
        df = pd.read_csv('mimic dataset/icu_final_df.csv')
        df['outcome'] = df['mortality_icu'].map({0: 'Survived', 1: 'Died'})
        return df
    except:
        return None

MODEL, THRESHOLD, DEMO_MODE = load_model()
REF_DF = load_ref()

COLORS   = {'Survived': '#7bc4a0', 'Died': '#e07070'}
PLOT_BG  = '#fdfbf8'
PLOT_FONT= '#2d2d3a'

NORMAL_RANGES = {
    'mean_hr':         (60,  100, 40,  140),
    'mean_sbp':        (90,  140, 70,  180),
    'mean_dbp':        (60,  90,  40,  120),
    'mean_map':        (70,  100, 50,  130),
    'mean_rr':         (12,  20,  8,   30),
    'mean_spo2':       (95,  100, 88,  100),
    'mean_temp_c':     (36.1,37.2,35.0,39.5),
    'mean_lactate':    (0.5, 2.0, 0,   4.0),
    'mean_creatinine': (0.6, 1.2, 0,   3.0),
    'mean_bilirubin':  (0.2, 1.2, 0,   5.0),
    'mean_wbc':        (4.5, 11.0,2.0, 20.0),
    'mean_hemog':      (12,  17,  7,   20),
    'mean_sodium':     (136, 145, 125, 155),
    'mean_potassium':  (3.5, 5.0, 2.5, 6.5),
    'mean_bun':        (7,   20,  0,   50),
    'mean_platelets':  (150, 400, 50,  700),
}
ALERT_COLORS = {'normal': '#7bc4a0', 'warning': '#e8b86d', 'critical': '#e07070'}

def get_alert_level(feature, value):
    if feature not in NORMAL_RANGES or value is None:
        return 'normal'
    lo_n, hi_n, lo_c, hi_c = NORMAL_RANGES[feature]
    if value < lo_c or value > hi_c: return 'critical'
    if value < lo_n or value > hi_n: return 'warning'
    return 'normal'

def plot_layout(height=320, legend=True):
    axis_style = dict(
        color=PLOT_FONT,
        tickcolor=PLOT_FONT,
        tickfont=dict(color=PLOT_FONT, size=11),
        title=dict(font=dict(color=PLOT_FONT, size=12)),
        linecolor='#c9bfe8',
        gridcolor='#ede8f5'
    )
    base = dict(
        height=height,
        template='plotly_white',
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family='DM Sans', color=PLOT_FONT, size=12),
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=axis_style,
        yaxis=axis_style,
    )
    if legend:
        base['legend'] = dict(
            orientation='h', y=1.08,
            font=dict(color=PLOT_FONT, size=12),
            bgcolor='rgba(0,0,0,0)'
        )
    else:
        base['showlegend'] = False
    return base

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:2.2em">🏥</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.15em;
                    color:#2d2d3a;margin-top:4px">ICU Risk</div>
        <div style="font-size:0.75em;color:#5a5a72;margin-top:2px">Mortality Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["🏠  Overview",
         "⚕️  Patient Assessment",
         "📊  Data Overview",
         "⚙️  Model Info"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    if DEMO_MODE:
        st.warning("⚠️ Demo mode — model not found")
    else:
        st.markdown(f"""
        <div style="background:#eaf6f0;border-radius:10px;padding:12px 14px;
                    border:1px solid #b5d5c8;margin-bottom:10px">
            <div style="font-size:0.75em;font-weight:600;color:#5a5a72;
                        text-transform:uppercase;letter-spacing:0.05em">Model Status</div>
            <div style="color:#2d8a5e;font-weight:600;margin-top:2px">✓ Live Model Loaded</div>
            <div style="font-size:0.82em;color:#5a5a72;margin-top:4px">
                Threshold: <b style="color:#2d2d3a">{THRESHOLD:.4f}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if REF_DF is not None:
        n    = len(REF_DF)
        mort = REF_DF['mortality_icu'].mean()
        st.markdown(f"""
        <div style="background:#f4f0fb;border-radius:10px;padding:12px 14px;
                    border:1px solid #ddd5f0">
            <div style="font-size:0.75em;font-weight:600;color:#5a5a72;
                        text-transform:uppercase;letter-spacing:0.05em">Dataset</div>
            <div style="font-weight:600;color:#2d2d3a;margin-top:2px">{n:,} patients</div>
            <div style="font-size:0.82em;color:#c05050;margin-top:4px">
                {mort:.1%} mortality rate
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TOP HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="top-header">
    <div>
        <h1>🏥 ICU 72h Mortality Risk Dashboard</h1>
        <p class="subtitle">Clinical decision support for healthcare providers &amp; nurse practitioners</p>
    </div>
    <div style="text-align:right;font-size:0.85em;color:#5a5a72">
        HGB + RF + XGBoost Ensemble<br>
        <span style="color:#2d8a5e;font-weight:600">● Live</span>
        &nbsp;| Threshold: <b style="color:#2d2d3a">{THRESHOLD:.3f}</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════════════
if page == "🏠  Overview":

    if REF_DF is None:
        st.warning("Reference dataset not found. Place `icu_final_df.csv` in the `mimic dataset/` folder.")
        st.stop()

    df         = REF_DF
    n_total    = len(df)
    n_died     = int(df['mortality_icu'].sum())
    n_survived = n_total - n_died
    mort_rate  = n_died / n_total
    median_age = int(df['age'].median())
    median_los = df['los'].median()

    cards = [
        ("#eaf0fb","#7da8d8","Total Patients", f"{n_total:,}"),
        ("#eaf6f0","#7bc4a0","Survived",        f"{n_survived:,}"),
        ("#fdecea","#e07070","Died in ICU",     f"{n_died:,}"),
        ("#fef6e4","#e8b86d","Mortality Rate",  f"{mort_rate:.1%}"),
        ("#f4f0fb","#a890d0","Median Age",      f"{median_age} yrs"),
        ("#fdf4ea","#d4a870","Median LOS",      f"{median_los:.1f}d"),
    ]
    cols = st.columns(6)
    for col, (bg, accent, label, val) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="stat-card" style="background:{bg};border-top:4px solid {accent}">'
                f'<div class="s-label">{label}</div>'
                f'<div class="s-value" style="color:{accent}">{val}</div>'
                f'</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card"><div class="section-title">Outcome Distribution</div>',
                    unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=['Survived','Died'], values=[n_survived, n_died],
            marker_colors=['#a8d8c0','#e8a090'], hole=0.52,
            textinfo='label+percent', textfont=dict(size=13, color='#2d2d3a'),
        ))
        fig_pie.update_layout(**plot_layout(280, legend=False))
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="section-card"><div class="section-title">Age Distribution by Outcome</div>',
                    unsafe_allow_html=True)
        fig_age = go.Figure()
        for outcome, color in [('Survived','#a8d8c0'),('Died','#e8a090')]:
            fig_age.add_trace(go.Histogram(
                x=df[df['outcome']==outcome]['age'], name=outcome,
                marker_color=color, opacity=0.78, nbinsx=30
            ))
        fig_age.update_layout(barmode='overlay', **plot_layout(280))
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="section-card"><div class="section-title">Mortality Rate by Care Unit</div>',
                    unsafe_allow_html=True)
        unit_mort = (df.groupby('careunit')['mortality_icu']
                       .mean().sort_values() * 100).reset_index()
        fig_unit = px.bar(unit_mort, x='mortality_icu', y='careunit', orientation='h',
                          color='mortality_icu',
                          color_continuous_scale=['#b5d5c8','#e8c4b8','#e07070'],
                          labels={'mortality_icu':'Mortality %','careunit':''})
        fig_unit.update_layout(**plot_layout(300, legend=False), coloraxis_showscale=False)
        fig_unit.update_traces(texttemplate='%{x:.1f}%', textposition='outside',
                               textfont=dict(color='#2d2d3a'))
        st.plotly_chart(fig_unit, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="section-card"><div class="section-title">Key Lab Medians by Outcome</div>',
                    unsafe_allow_html=True)
        labs       = ['mean_lactate','mean_creatinine','mean_bun','mean_bilirubin','mean_wbc']
        lab_labels = ['Lactate','Creatinine','BUN','Bilirubin','WBC']
        fig_lab = go.Figure()
        for outcome, color in [('Survived','#a8d8c0'),('Died','#e8a090')]:
            sub = df[df['outcome']==outcome]
            fig_lab.add_trace(go.Bar(
                name=outcome, x=lab_labels,
                y=[sub[c].median() for c in labs],
                marker_color=color, opacity=0.9
            ))
        fig_lab.update_layout(barmode='group', **plot_layout(300))
        st.plotly_chart(fig_lab, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown('<div class="section-card"><div class="section-title">Mortality Rate by Admission Location</div>',
                    unsafe_allow_html=True)
        adm = (df.groupby('admission_loc')['mortality_icu']
                 .mean().sort_values(ascending=False)*100).reset_index()
        fig_adm = px.bar(adm, x='admission_loc', y='mortality_icu',
                         color='mortality_icu',
                         color_continuous_scale=['#b5d5c8','#e8c4b8','#e07070'],
                         labels={'mortality_icu':'Mortality %','admission_loc':''})
        fig_adm.update_layout(**plot_layout(290, legend=False),
                              coloraxis_showscale=False, xaxis_tickangle=-20)
        st.plotly_chart(fig_adm, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="section-card"><div class="section-title">Length of Stay by Outcome</div>',
                    unsafe_allow_html=True)
        fig_los = go.Figure()
        for outcome, color in [('Survived','#a8d8c0'),('Died','#e8a090')]:
            sub = df[df['outcome']==outcome]['los'].dropna()
            sub = sub[sub < sub.quantile(0.97)]
            fig_los.add_trace(go.Box(
                y=sub, name=outcome, marker_color=color,
                boxmean=True, boxpoints=False
            ))
        fig_los.update_layout(**plot_layout(290), yaxis_title='LOS (days)')
        st.plotly_chart(fig_los, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PAGE 2 — PATIENT ASSESSMENT
# ═══════════════════════════════════════════════════════
elif page == "⚕️  Patient Assessment":

    st.markdown('<div class="section-card"><div class="section-title">👤 Demographics & Admission</div>',
                unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    with d1:
        age    = st.slider("Age (years)", 18, 110, 65)
        gender = st.radio("Gender", ["M","F"], horizontal=True)
    with d2:
        race   = st.selectbox("Race", ["WHITE","BLACK/AFRICAN AMERICAN",
                                        "HISPANIC/LATINO","ASIAN","OTHER/UNKNOWN"])
        los    = st.slider("LOS so far (days)", 0.0, 30.0, 2.0, 0.5)
    with d3:
        careunit = st.selectbox("Care Unit", [
            "Medical Intensive Care Unit (MICU)",
            "Surgical Intensive Care Unit (SICU)",
            "Cardiac Vascular Intensive Care Unit (CVICU)",
            "Medical/Surgical Intensive Care Unit (MICU/SICU)",
            "Coronary Care Unit (CCU)",
            "Neuro Surgical Intensive Care Unit (Neuro SICU)",
            "Trauma SICU (TSICU)"])
        admit_loc = st.selectbox("Admission Via", [
            "EMERGENCY ROOM","TRANSFER FROM HOSPITAL","PHYSICIAN REFERRAL",
            "WALK-IN/SELF REFERRAL","PROCEDURE SITE","PACU"])
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">💓 Vital Signs</div>',
                unsafe_allow_html=True)
    v1, v2, v3 = st.columns(3)
    with v1:
        hr      = st.slider("Mean HR (bpm)",    20, 200, 80)
        hr_min  = st.slider("Min HR",           20, 200, 70)
        hr_max  = st.slider("Max HR",           20, 200, 95)
        sbp     = st.slider("Mean SBP (mmHg)",  50, 220, 120)
        sbp_min = st.slider("Min SBP",          50, 220, 100)
        sbp_max = st.slider("Max SBP",          50, 220, 140)
    with v2:
        dbp     = st.slider("Mean DBP (mmHg)",  30, 140, 75)
        dbp_min = st.slider("Min DBP",          30, 140, 60)
        dbp_max = st.slider("Max DBP",          30, 140, 90)
        map_    = st.slider("Mean MAP (mmHg)",  40, 150, 90)
        map_min = st.slider("Min MAP",          40, 150, 70)
        map_max = st.slider("Max MAP",          40, 150, 110)
    with v3:
        rr      = st.slider("Mean RR (/min)",   4,  50,  16)
        rr_min  = st.slider("Min RR",           4,  50,  12)
        rr_max  = st.slider("Max RR",           4,  50,  20)
        spo2    = st.slider("Mean SpO2 (%)",    60.0,100.0,97.0,0.5)
        spo2_min= st.slider("Min SpO2",         60.0,100.0,94.0,0.5)
        spo2_max= st.slider("Max SpO2",         60.0,100.0,100.0,0.5)
    vx1, vx2 = st.columns(2)
    with vx1:
        temp  = st.slider("Mean Temp (°C)",   34.0,42.0,37.0,0.1)
        fio2  = st.slider("Max FiO2",         0.21,1.0,0.21,0.01)
    with vx2:
        pao2  = st.slider("Max PaO2 (mmHg)", 20,500,90,5)
        urine = st.slider("Urine 72h (mL)",  0,8000,1500,100)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">🧪 Laboratory Values</div>',
                unsafe_allow_html=True)
    l1, l2, l3 = st.columns(3)
    with l1:
        cr      = st.slider("Mean Creatinine",  0.0,15.0,1.0,0.1)
        cr_min  = st.slider("Min Creatinine",   0.0,15.0,0.8,0.1)
        cr_max  = st.slider("Max Creatinine",   0.0,15.0,1.2,0.1)
        lac     = st.slider("Mean Lactate",     0.0,20.0,1.0,0.1)
        lac_min = st.slider("Min Lactate",      0.0,20.0,0.5,0.1)
        lac_max = st.slider("Max Lactate",      0.0,20.0,1.5,0.1)
        bili    = st.slider("Mean Bilirubin",   0.0,30.0,0.8,0.1)
        bili_min= st.slider("Min Bilirubin",    0.0,30.0,0.5,0.1)
        bili_max= st.slider("Max Bilirubin",    0.0,30.0,1.0,0.1)
    with l2:
        wbc     = st.slider("Mean WBC (K/uL)",  0.0,50.0,8.0,0.5)
        wbc_min = st.slider("Min WBC",          0.0,50.0,5.0,0.5)
        wbc_max = st.slider("Max WBC",          0.0,50.0,11.0,0.5)
        hgb     = st.slider("Mean Hemoglobin",  3.0,22.0,12.0,0.5)
        hgb_min = st.slider("Min Hemoglobin",   3.0,22.0,10.0,0.5)
        hgb_max = st.slider("Max Hemoglobin",   3.0,22.0,14.0,0.5)
        plt_    = st.slider("Mean Platelets",   10,800,200,10)
        plt_min = st.slider("Min Platelets",    10,800,150,10)
        plt_max = st.slider("Max Platelets",    10,800,250,10)
    with l3:
        na      = st.slider("Mean Sodium",      110,165,139)
        na_min  = st.slider("Min Sodium",       110,165,136)
        na_max  = st.slider("Max Sodium",       110,165,142)
        k       = st.slider("Mean Potassium",   1.5,9.0,4.0,0.1)
        k_min   = st.slider("Min Potassium",    1.5,9.0,3.5,0.1)
        k_max   = st.slider("Max Potassium",    1.5,9.0,4.5,0.1)
        bun     = st.slider("Mean BUN",         0,150,15)
        bun_min = st.slider("Min BUN",          0,150,10)
        bun_max = st.slider("Max BUN",          0,150,20)
    st.markdown('</div>', unsafe_allow_html=True)

    assess_btn = st.button("⚕️  Assess Mortality Risk", type="primary", use_container_width=True)

    def build_patient_df():
        return pd.DataFrame([{
            'age':age,'gender':gender,'los':los,
            'max_hr':hr_max,'min_hr':hr_min,'mean_hr':hr,
            'max_sbp':sbp_max,'min_sbp':sbp_min,'mean_sbp':sbp,
            'max_dbp':dbp_max,'min_dbp':dbp_min,'mean_dbp':dbp,
            'min_map':map_min,'max_map':map_max,'mean_map':map_,
            'max_rr':rr_max,'min_rr':rr_min,'mean_rr':rr,
            'min_spo2':spo2_min,'max_spo2':spo2_max,'mean_spo2':spo2,
            'max_fio2':fio2,'max_pao2':pao2,'mean_temp_c':temp,
            'max_creatinine':cr_max,'min_creatinine':cr_min,'mean_creatinine':cr,
            'max_lactate':lac_max,'min_lactate':lac_min,'mean_lactate':lac,
            'max_bilirubin':bili_max,'min_bilirubin':bili_min,'mean_bilirubin':bili,
            'max_wbc':wbc_max,'min_wbc':wbc_min,'mean_wbc':wbc,
            'max_hemog':hgb_max,'min_hemog':hgb_min,'mean_hemog':hgb,
            'max_sodium':na_max,'min_sodium':na_min,'mean_sodium':na,
            'max_potassium':k_max,'min_potassium':k_min,'mean_potassium':k,
            'max_bun':bun_max,'min_bun':bun_min,'mean_bun':bun,
            'max_platelets':plt_max,'min_platelets':plt_min,'mean_platelets':plt_,
            'total_urine_72h':urine,
            'race_clean':race,'careunit':careunit,'admission_loc':admit_loc,
        }])

    if assess_btn:
        patient_df = build_patient_df()

        if MODEL is not None:
            prob = float(MODEL.predict_proba(patient_df)[0, 1])
        else:
            prob = min(0.99, max(0.01,
                0.05 + (age-50)*0.004 + max(0,lac-2.0)*0.08
                + max(0,cr-1.5)*0.05 + max(0,90-spo2)*0.02
                + max(0,65-map_)*0.01))

        prediction = 1 if prob >= THRESHOLD else 0

        if   prob < THRESHOLD:            risk_label,risk_bg,risk_border,risk_emoji = "LOW RISK",      "#eaf6f0","#7bc4a0","🟢"
        elif prob < THRESHOLD + 0.15:     risk_label,risk_bg,risk_border,risk_emoji = "MODERATE RISK", "#fef6e4","#e8b86d","🟡"
        elif prob < THRESHOLD + 0.35:     risk_label,risk_bg,risk_border,risk_emoji = "HIGH RISK",     "#fdecea","#e07070","🟠"
        else:                             risk_label,risk_bg,risk_border,risk_emoji = "CRITICAL RISK", "#fce8e8","#c04040","🔴"

        key_vitals = {
            'mean_hr':hr,'mean_sbp':sbp,'mean_map':map_,'mean_rr':rr,
            'mean_spo2':spo2,'mean_temp_c':temp,'mean_lactate':lac,
            'mean_creatinine':cr,'mean_bilirubin':bili,'mean_wbc':wbc,
            'mean_potassium':k,'mean_sodium':na,'mean_platelets':plt_,
            'mean_bun':bun,'mean_hemog':hgb,
        }
        critical_flags, warning_flags = [], []
        for feat, val in key_vitals.items():
            level = get_alert_level(feat, val)
            lbl   = feat.replace('mean_','').replace('_',' ').title()
            if feat in NORMAL_RANGES:
                lo_n,hi_n,lo_c,hi_c = NORMAL_RANGES[feat]
                if level == 'critical':
                    critical_flags.append(f"{lbl}: {val:.1f}  [{'↓ LOW' if val<lo_c else '↑ HIGH'}]")
                elif level == 'warning':
                    warning_flags.append(f"{lbl}: {val:.1f}  [{'↓ LOW' if val<lo_n else '↑ HIGH'}]")

        recs = []
        if lac > 2.0:   recs.append("Elevated lactate — IV fluids, sepsis workup, source control")
        if map_ < 65:   recs.append("MAP < 65 mmHg — initiate vasopressor therapy per protocol")
        if spo2 < 92:   recs.append("SpO2 < 92% — increase FiO2, evaluate for intubation")
        if cr > 2.0:    recs.append("Elevated creatinine — nephrology consult, review nephrotoxins")
        if rr > 25:     recs.append("Tachypnoea RR > 25 — ABG, CXR, consider NIV / intubation")
        if plt_ < 100:  recs.append("Thrombocytopenia — bleeding risk, review anticoagulation")
        if k > 5.5:     recs.append("Hyperkalaemia > 5.5 — ECG, calcium gluconate, kayexalate / dialysis")
        if k < 3.0:     recs.append("Hypokalaemia < 3.0 — IV potassium replacement, cardiac monitoring")
        if hgb < 7:     recs.append("Hgb < 7 g/dL — consider transfusion per protocol")
        if bun > 40:    recs.append("Elevated BUN — assess for AKI, GI bleed, volume status")
        if urine < 500: recs.append("Oliguria < 500 mL/72h — fluid challenge, assess for AKI / obstruction")
        if prediction == 1 and not recs:
            recs.append("High composite risk — escalate monitoring, ICU team review")

        st.markdown(
            f'<div class="risk-banner" style="background:{risk_bg};border-color:{risk_border}">'
            f'<h2>{risk_emoji} {risk_label}</h2>'
            f'<p>72h Mortality Probability: <b>{prob*100:.1f}%</b> &nbsp;·&nbsp; '
            f'Threshold: {THRESHOLD:.3f} &nbsp;·&nbsp; '
            f'{"⚠️ Intervention recommended" if prediction==1 else "✅ Continue standard monitoring"}</p>'
            f'</div>', unsafe_allow_html=True)

        g1, g2 = st.columns(2)
        with g1:
            st.markdown('<div class="section-card"><div class="section-title">Risk Gauge</div>',
                        unsafe_allow_html=True)
            t = THRESHOLD
            fig_g = go.Figure(go.Indicator(
                mode='gauge+number',
                value=round(prob*100,1),
                number={'suffix':'%','font':{'size':44,'color':'#2d2d3a'}},
                gauge={
                    'axis':{'range':[0,100],'tickcolor':'#5a5a72',
                            'tickfont':{'color':'#5a5a72','size':11}},
                    'bar':{'color':risk_border,'thickness':0.26},
                    'bgcolor':PLOT_BG, 'borderwidth':0,
                    'steps':[
                        {'range':[0,           t*100],         'color':'#d8f0e4'},
                        {'range':[t*100,        (t+0.15)*100], 'color':'#fef0d0'},
                        {'range':[(t+0.15)*100, (t+0.35)*100], 'color':'#fde0d8'},
                        {'range':[(t+0.35)*100, 100],          'color':'#f8c8c8'},
                    ],
                    'threshold':{'line':{'color':'#2d2d3a','width':3},
                                 'thickness':0.85,'value':t*100}
                }
            ))
            fig_g.update_layout(height=270, margin=dict(t=30,b=10,l=20,r=20),
                                paper_bgcolor=PLOT_BG,
                                font=dict(family='DM Sans',color='#2d2d3a'))
            st.plotly_chart(fig_g, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with g2:
            st.markdown('<div class="section-card"><div class="section-title">Key Values at a Glance</div>',
                        unsafe_allow_html=True)
            m1,m2,m3 = st.columns(3)
            m1.metric("MAP",        f"{map_:.0f} mmHg",  delta=f"{map_-70:.0f} vs floor",  delta_color="normal")
            m2.metric("Lactate",    f"{lac:.1f} mmol/L", delta=f"{lac-2:.1f} vs upper",    delta_color="inverse")
            m3.metric("SpO2",       f"{spo2:.1f}%",      delta=f"{spo2-95:.1f} vs lower",  delta_color="normal")
            m4,m5,m6 = st.columns(3)
            m4.metric("HR",         f"{hr:.0f} bpm",     delta=f"{hr-80:.0f} vs norm")
            m5.metric("Creatinine", f"{cr:.1f} mg/dL",   delta=f"{cr-1.2:.1f} vs upper",   delta_color="inverse")
            m6.metric("RR",         f"{rr:.0f} /min",    delta=f"{rr-20:.0f} vs upper",    delta_color="inverse")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card"><div class="section-title">📊 Vitals & Labs Status</div>',
                    unsafe_allow_html=True)
        bar_labels = ['HR\n(bpm)','SBP\n(mmHg)','MAP\n(mmHg)','RR\n(/min)',
                      'SpO2\n(%)','Temp\n(°C)','Lactate','Creatinine',
                      'K+\n(mEq/L)','Hgb\n(g/dL)','Platelets\n(K/uL)']
        bar_vals   = [hr,sbp,map_,rr,spo2,temp,lac,cr,k,hgb,plt_]
        bar_feats  = ['mean_hr','mean_sbp','mean_map','mean_rr','mean_spo2',
                      'mean_temp_c','mean_lactate','mean_creatinine',
                      'mean_potassium','mean_hemog','mean_platelets']
        bar_colors = [ALERT_COLORS[get_alert_level(f,v)] for f,v in zip(bar_feats,bar_vals)]
        fig_bar = go.Figure(go.Bar(
            x=bar_labels, y=bar_vals, marker_color=bar_colors,
            text=[f'{v:.1f}' for v in bar_vals], textposition='outside',
            textfont=dict(color='#2d2d3a', size=11)
        ))
        fig_bar.update_layout(**plot_layout(330, legend=False), yaxis_title='Value',
                              title=dict(text='Green=Normal  Orange=Warning  Red=Critical',
                                         font=dict(size=11,color='#5a5a72'),x=0))
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        a1, a2 = st.columns(2)
        with a1:
            st.markdown('<div class="section-card"><div class="section-title">🚨 Clinical Alerts</div>',
                        unsafe_allow_html=True)
            if critical_flags:
                st.markdown('<div class="alert-crit"><b style="color:#c04040">🚨 CRITICAL VALUES</b><br>'
                            + '<br>'.join(f'• {f}' for f in critical_flags)+'</div>',
                            unsafe_allow_html=True)
            if warning_flags:
                st.markdown('<div class="alert-warn"><b style="color:#c08030">⚠️ WARNING VALUES</b><br>'
                            + '<br>'.join(f'• {f}' for f in warning_flags)+'</div>',
                            unsafe_allow_html=True)
            if not critical_flags and not warning_flags:
                st.markdown('<div class="alert-ok">✅ All monitored values within normal range.</div>',
                            unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with a2:
            st.markdown('<div class="section-card"><div class="section-title">📋 Clinical Action Items</div>',
                        unsafe_allow_html=True)
            if recs:
                st.markdown('<div class="alert-rec"><b style="color:#3a6fa8">Recommended Actions</b><br>'
                            + '<br>'.join(f'• {r}' for r in recs)+'</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-ok">✅ No immediate actions flagged.</div>',
                            unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if REF_DF is not None:
            st.markdown('<div class="section-card"><div class="section-title">📈 Patient Percentile vs MIMIC Reference</div>',
                        unsafe_allow_html=True)
            st.caption("Where does this patient sit relative to those who survived vs died in the reference dataset?")
            ref_died = REF_DF[REF_DF['mortality_icu']==1]
            ref_surv = REF_DF[REF_DF['mortality_icu']==0]
            cfeats  = ['mean_lactate','mean_creatinine','mean_map','mean_hr','mean_spo2','mean_rr']
            clabels = ['Lactate','Creatinine','MAP','HR','SpO2','RR']
            cvals   = [lac,cr,map_,hr,spo2,rr]
            fig_ctx = go.Figure()
            for feat,label,val in zip(cfeats,clabels,cvals):
                if feat in ref_died.columns:
                    pd_ = (ref_died[feat].dropna()<=val).mean()*100
                    ps_ = (ref_surv[feat].dropna()<=val).mean()*100
                    fig_ctx.add_trace(go.Bar(name='vs Died',x=[label],y=[pd_],
                        marker_color='#e8a090',opacity=0.85,
                        text=f'{pd_:.0f}th',textposition='outside',
                        textfont=dict(color='#2d2d3a'),
                        legendgroup='died',showlegend=(label=='Lactate')))
                    fig_ctx.add_trace(go.Bar(name='vs Survived',x=[label],y=[ps_],
                        marker_color='#a8d8c0',opacity=0.85,
                        text=f'{ps_:.0f}th',textposition='outside',
                        textfont=dict(color='#2d2d3a'),
                        legendgroup='surv',showlegend=(label=='Lactate')))
            fig_ctx.update_layout(barmode='group',**plot_layout(360),
                                  yaxis_title='Percentile rank (%)')
            st.plotly_chart(fig_ctx, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PAGE 3 — DATA OVERVIEW
# ═══════════════════════════════════════════════════════
elif page == "📊  Data Overview":

    if REF_DF is None:
        st.warning("Reference dataset not found.")
        st.stop()

    df       = REF_DF
    VITALS   = ['mean_hr','mean_sbp','mean_dbp','mean_map','mean_rr','mean_spo2','mean_temp_c']
    LABS     = ['mean_creatinine','mean_lactate','mean_bilirubin','mean_wbc',
                'mean_hemog','mean_sodium','mean_potassium','mean_bun','mean_platelets']
    NUM_COLS = [c for c in df.select_dtypes('number').columns if c != 'mortality_icu']

    st.markdown('<div class="section-card"><div class="section-title">Distribution Explorer</div>',
                unsafe_allow_html=True)
    dc1, dc2 = st.columns([2,1])
    with dc1:
        feat  = st.selectbox("Select feature", NUM_COLS,
                             index=NUM_COLS.index('mean_lactate') if 'mean_lactate' in NUM_COLS else 0)
    with dc2:
        ptype = st.radio("Plot type", ['Histogram','Box','Violin'], horizontal=True)

    data = df[[feat,'outcome']].dropna()
    kw   = dict(color='outcome', color_discrete_map={'Survived':'#a8d8c0','Died':'#e8a090'})
    if ptype == 'Histogram':
        fig_d = px.histogram(data, x=feat, barmode='overlay', opacity=0.75, nbins=60, **kw)
    elif ptype == 'Box':
        fig_d = px.box(data, x='outcome', y=feat, boxmode='group', **kw)
    else:
        fig_d = px.violin(data, x='outcome', y=feat, box=True, **kw)
    fig_d.update_layout(**plot_layout(380))
    st.plotly_chart(fig_d, use_container_width=True)
    s_med = data[data['outcome']=='Survived'][feat].median()
    d_med = data[data['outcome']=='Died'][feat].median()
    st.caption(f"Survived median: **{s_med:.2f}**  ·  Died median: **{d_med:.2f}**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Correlation Heatmap</div>',
                unsafe_allow_html=True)
    grp = st.radio("Feature group", ['Vitals','Labs','All means'], horizontal=True)
    if grp == 'Vitals':  hcols = VITALS + ['mortality_icu']
    elif grp == 'Labs':  hcols = LABS   + ['mortality_icu']
    else:                hcols = VITALS + LABS + ['age','los','mortality_icu']
    hcols = [c for c in hcols if c in df.columns]
    corr  = df[hcols].corr()
    fig_h = px.imshow(corr, text_auto='.2f', aspect='auto',
                      color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    fig_h.update_layout(**plot_layout(520, legend=False))
    fig_h.update_traces(textfont=dict(color='#2d2d3a', size=10))
    st.plotly_chart(fig_h, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Missing Data Map</div>',
                unsafe_allow_html=True)
    miss = (df.isnull().mean()*100).sort_values(ascending=False)
    miss = miss[miss>0].reset_index()
    miss.columns = ['feature','missing_pct']
    fig_m = px.bar(miss, x='missing_pct', y='feature', orientation='h',
                   color='missing_pct',
                   color_continuous_scale=['#c8e6da','#e8c4b8','#e07070'],
                   labels={'missing_pct':'Missing %'})
    layout_m = plot_layout(420, legend=False)
    layout_m['yaxis']['categoryorder'] = 'total ascending'
    layout_m['coloraxis_showscale'] = False
    fig_m.update_layout(**layout_m)
    st.plotly_chart(fig_m, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# PAGE 4 — MODEL INFO
# ═══════════════════════════════════════════════════════
elif page == "⚙️  Model Info":

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-title">⚙️ Model Configuration</div>
            <table style="width:100%;border-collapse:collapse;font-size:0.9em">
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Model type</td><td style="padding:8px 4px;color:#2d2d3a">Soft-voting ensemble</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Components</td><td style="padding:8px 4px;color:#2d2d3a">HGB (w=2) + RF (w=1) + XGBoost (w=2)</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Calibration</td><td style="padding:8px 4px;color:#2d2d3a">Platt sigmoid</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">CV strategy</td><td style="padding:8px 4px;color:#2d2d3a">StratifiedKFold (5 fold)</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">CV scorer</td><td style="padding:8px 4px;color:#2d2d3a">Recall with precision floor &ge; 0.40</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Resampling</td><td style="padding:8px 4px;color:#2d2d3a">SMOTE (k_neighbors=5)</td></tr>
                <tr style="border-bottom:1px solid #ede8f5"><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Decision threshold</td><td style="padding:8px 4px;color:#2d2d3a"><b>{THRESHOLD:.4f}</b></td></tr>
                <tr><td style="padding:8px 4px;color:#5a5a72;font-weight:600">Mode</td><td style="padding:8px 4px;color:#2d8a5e;font-weight:600">{"Demo" if DEMO_MODE else "✓ Live model"}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="section-card">
            <div class="section-title">📐 Class Imbalance Strategy</div>
            <p style="color:#5a5a72;font-weight:600;margin:10px 0 6px 0">Resampling</p>
            <ul style="color:#2d2d3a;margin:0 0 14px 0;padding-left:18px;line-height:1.8">
                <li>SMOTE oversampling inside imblearn.Pipeline</li>
                <li>Applied only on training folds — no data leakage</li>
            </ul>
            <p style="color:#5a5a72;font-weight:600;margin:10px 0 6px 0">Class weighting</p>
            <ul style="color:#2d2d3a;margin:0 0 14px 0;padding-left:18px;line-height:1.8">
                <li>class_weight='balanced' on HGB</li>
                <li>Explicit ratio search on RF (w in [5,7,10,15,20])</li>
                <li>scale_pos_weight = neg/pos on XGBoost</li>
            </ul>
            <p style="color:#5a5a72;font-weight:600;margin:10px 0 6px 0">Threshold selection</p>
            <ul style="color:#2d2d3a;margin:0;padding-left:18px;line-height:1.8">
                <li>Recall &ge; 0.80 constraint enforced first</li>
                <li>Precision floor &ge; 0.40 to avoid rubber-stamp predictions</li>
                <li>F1 maximised within those constraints</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">📏 Clinical Normal Ranges Reference</div>',
                unsafe_allow_html=True)
    ranges_data = []
    for feat, (lo_n,hi_n,lo_c,hi_c) in NORMAL_RANGES.items():
        ranges_data.append({
            'Feature':      feat.replace('mean_','').replace('_',' ').title(),
            'Normal Low':   lo_n, 'Normal High':  hi_n,
            'Critical Low': lo_c, 'Critical High': hi_c
        })
    st.dataframe(pd.DataFrame(ranges_data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown(
    f'<div class="footer">'
    f'ICU Mortality Risk Dashboard &nbsp;·&nbsp; '
    f'HGB + RF + XGBoost Soft-Voting Ensemble &nbsp;·&nbsp; '
    f'Threshold: {THRESHOLD:.4f} &nbsp;·&nbsp; '
    f'For clinical decision support only — not a substitute for clinical judgment.'
    f'</div>',
    unsafe_allow_html=True
)