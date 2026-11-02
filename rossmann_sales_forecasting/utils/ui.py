import streamlit as st

def apply_custom_css():
    """
    Applies an ultra-clean, high-contrast white and royal/cerulean blue design system.
    Guarantees that all fonts, headings, cards, inputs, tables, and metrics have
    maximum readability with deep high-contrast text (#0f172a, #1e293b) on clean backgrounds.
    Prevents letter overlapping/overwriting by avoiding broad CSS overrides on Streamlit icon ligatures.
    """
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&display=swap');
        
        /* Global Typography targeting text elements specifically */
        html, body, p, span, li, label, .stMarkdown {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0f172a;
            letter-spacing: normal !important;
            word-spacing: normal !important;
            line-height: 1.5;
        }
        
        /* Preserve Streamlit internal icons so words do not overwrite buttons/dropdowns */
        [data-testid="stIconMaterial"], 
        [class*="material-symbols"], 
        span[data-testid*="Icon"], 
        i[class*="material-icons"] {
            font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
            letter-spacing: normal !important;
        }

        /* Main Headings */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            letter-spacing: normal !important;
            line-height: 1.3 !important;
        }

        /* Top Header Box */
        .header-box {
            background: linear-gradient(135deg, #f0f7ff 0%, #e0f2fe 100%);
            border: 1.5px solid #7dd3fc;
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 24px;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.08);
        }
        .header-title {
            font-size: 2.1rem;
            color: #0369a1 !important;
            margin: 0;
            font-weight: 800;
            letter-spacing: normal !important;
            line-height: 1.25 !important;
        }
        .header-subtitle {
            font-size: 1.05rem;
            color: #334155 !important;
            margin-top: 6px;
            margin-bottom: 0;
            font-weight: 500;
            line-height: 1.4 !important;
        }

        /* KPI Card Styling */
        .kpi-card {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 12px;
            padding: 20px 22px;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.05);
            transition: all 0.2s ease-in-out;
            height: 100%;
        }
        .kpi-card:hover {
            border-color: #0284c7;
            box-shadow: 0 8px 20px rgba(2, 132, 199, 0.14);
            transform: translateY(-2px);
        }
        .kpi-label {
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #475569 !important;
            font-weight: 700;
            margin-bottom: 6px;
        }
        .kpi-value {
            font-size: 1.95rem;
            font-weight: 800;
            color: #0284c7 !important;
            font-family: 'Outfit', sans-serif !important;
            margin: 0;
            letter-spacing: normal !important;
            line-height: 1.2 !important;
        }
        .kpi-subtext {
            font-size: 0.85rem;
            color: #059669 !important;
            font-weight: 700;
            margin-top: 5px;
        }

        /* Pill Badges */
        .badge-pill {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .badge-best {
            background-color: #dbeafe;
            color: #1e40af !important;
            border: 1.5px solid #60a5fa;
        }
        .badge-success {
            background-color: #d1fae5;
            color: #065f46 !important;
            border: 1.5px solid #34d399;
        }

        /* Hero Prediction Result Card */
        .prediction-hero-card {
            background: linear-gradient(135deg, #0369a1 0%, #075985 100%);
            border: 2px solid #38bdf8;
            color: #ffffff !important;
            border-radius: 16px;
            padding: 28px;
            box-shadow: 0 12px 30px rgba(3, 105, 161, 0.3);
            text-align: center;
            margin: 22px 0;
        }
        .prediction-hero-title {
            font-size: 1.05rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #e0f2fe !important;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .prediction-hero-value {
            font-size: 3.4rem;
            font-weight: 900;
            color: #ffffff !important;
            font-family: 'Outfit', sans-serif !important;
            margin: 0;
            letter-spacing: normal !important;
            line-height: 1.15 !important;
            text-shadow: 0 2px 8px rgba(0,0,0,0.25);
        }
        .prediction-hero-details {
            font-size: 1rem;
            margin-top: 12px;
            color: #f0f9ff !important;
            font-weight: 500;
        }

        /* Streamlit UI Widget Text Readability */
        .stSelectbox label, .stTextInput label, .stNumberInput label, .stRadio label, .stDateInput label {
            font-weight: 700 !important;
            color: #0f172a !important;
            font-size: 0.95rem !important;
            margin-bottom: 4px !important;
        }
        div[data-baseweb="select"] > div {
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
            color: #0f172a !important;
            font-weight: 600 !important;
            background-color: #ffffff !important;
        }
        input {
            color: #0f172a !important;
            font-weight: 600 !important;
        }

        /* Tabs Styling */
        button[data-baseweb="tab"] {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            color: #475569 !important;
            padding: 10px 18px !important;
            letter-spacing: normal !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #0284c7 !important;
            border-bottom-color: #0284c7 !important;
            border-bottom-width: 3px !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 10px 22px !important;
            letter-spacing: normal !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
            color: #ffffff !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25) !important;
        }
        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 16px rgba(2, 132, 199, 0.4) !important;
            transform: translateY(-1px) !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1.5px solid #e2e8f0 !important;
        }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #1e293b !important;
        }
        
        /* Metric widget styling */
        div[data-testid="stMetricValue"] > div {
            color: #0f172a !important;
            font-weight: 800 !important;
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: normal !important;
        }
        div[data-testid="stMetricLabel"] > label {
            color: #475569 !important;
            font-weight: 700 !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, badge: str = "ML Production"):
    st.markdown(f"""
    <div class="header-box">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <h1 class="header-title">{title}</h1>
            <span class="badge-pill badge-best">{badge}</span>
        </div>
        <p class="header-subtitle">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_kpi(label: str, value: str, subtext: str = "", delta_color: str = "#059669"):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {f'<div class="kpi-subtext" style="color: {delta_color} !important;">{subtext}</div>' if subtext else ''}
    </div>
    """, unsafe_allow_html=True)
