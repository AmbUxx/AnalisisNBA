"""
Estilos CSS modulares para la aplicación - Estilo Betting/Fintech
"""

MAIN_CSS = """
    <style>
    /* Dark Mode Base */
    .main {
        background: #0a0e27;
        color: #e0e0e0;
        padding-top: 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    .block-container {
        background: #0f1422;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #1a2332;
    }
    
    /* Tipografía Monoespaciada para Números */
    .mono-number {
        font-family: 'Courier New', 'Consolas', monospace;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Títulos */
    h1 {
        color: #00ff88;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 2rem;
    }
    
    h2 {
        color: #00d9ff;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-size: 1.5rem;
    }
    
    h3 {
        color: #b4b4ff;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
    }
    
    /* Sidebar Dark */
    .sidebar .sidebar-content {
        background: #0f1422;
        border-right: 2px solid #1a2332;
    }
    
    [data-testid="stSidebar"] {
        background: #0f1422;
    }
    
    /* Botones - Neon Style */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00d9ff 100%);
        color: #0a0e27;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.2s;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.6);
        transform: translateY(-2px);
    }
    
    /* Tabs Dark */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #1a1f3a;
        border-radius: 8px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: #b4b4ff;
        border-radius: 6px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00ff88;
        color: #0a0e27;
    }
    
    /* Métricas - Compactas y Monoespaciadas */
    [data-testid="stMetricValue"] {
        font-family: 'Courier New', monospace;
        font-size: 1.75rem;
        font-weight: 700;
        color: #00ff88;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b4b4ff;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Courier New', monospace;
        font-weight: 600;
    }
    
    /* Tablas Compactas - High Density */
    .dataframe {
        background: #0f1422;
        border: 1px solid #1a2332;
        border-radius: 8px;
        font-size: 0.85rem;
    }
    
    .dataframe th {
        background: #1a2332;
        color: #00d9ff;
        font-weight: 600;
        padding: 0.5rem 0.75rem;
        font-size: 0.8rem;
    }
    
    .dataframe td {
        padding: 0.4rem 0.75rem;
        color: #e0e0e0;
        border-bottom: 1px solid #1a2332;
    }
    
    /* Alertas - Naranja */
    .stAlert {
        background: rgba(255, 140, 0, 0.1);
        border-left: 4px solid #ff8c00;
        color: #ffb366;
    }
    
    /* Info Boxes */
    .stInfo {
        background: rgba(0, 217, 255, 0.1);
        border-left: 4px solid #00d9ff;
        color: #66e0ff;
    }
    
    /* Success - Verde Neon */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1);
        border-left: 4px solid #00ff88;
        color: #66ffb3;
    }
    
    /* Badges y Tags */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    .badge-positive {
        background: rgba(0, 255, 136, 0.2);
        color: #00ff88;
        border: 1px solid #00ff88;
    }
    
    .badge-negative {
        background: rgba(255, 68, 68, 0.2);
        color: #ff4444;
        border: 1px solid #ff4444;
    }
    
    .badge-neutral {
        background: rgba(180, 180, 255, 0.2);
        color: #b4b4ff;
        border: 1px solid #b4b4ff;
    }
    
    /* Cards - Bento Grid Style */
    .bet-card {
        background: #0f1422;
        border: 1px solid #1a2332;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .bet-card:hover {
        border-color: #00ff88;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f1422;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1a2332;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff88;
    }
    
    /* Select boxes */
    .stSelectbox label {
        color: #b4b4ff;
        font-weight: 600;
    }
    
    /* Captions */
    .stCaption {
        color: #888;
        font-size: 0.75rem;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: #1a2332;
        color: #b4b4ff;
        border-radius: 6px;
    }
    </style>
"""

def apply_custom_styles():
    """Aplica los estilos CSS personalizados."""
    import streamlit as st
    st.markdown(MAIN_CSS, unsafe_allow_html=True)
