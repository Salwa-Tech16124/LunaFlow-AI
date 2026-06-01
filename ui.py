import streamlit as st

def apply_theme(is_dark=False):
    """Apply the custom feminine premium theme using CSS."""
    
    # Define variables based on theme
    if is_dark:
        bg_color = "#1A1423"
        card_bg = "rgba(36, 27, 47, 0.7)"
        primary = "#FF7EB6"
        lavender = "#C8A2FF"
        text = "#FFFFFF"
        text_sec = "#D8C9E8"
        border_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#FFF8FC"
        card_bg = "rgba(255, 255, 255, 0.7)"
        primary = "#FF7EB6"
        lavender = "#E6D8FF"
        text = "#4A3B52"
        text_sec = "#7D6B91"
        border_color = "rgba(255, 255, 255, 0.5)"

    custom_css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {{
            --primary: {primary};
            --secondary: {lavender};
            --background: {bg_color};
            --cards: {card_bg};
            --text: {text};
            --text-sec: {text_sec};
            --border: {border_color};
        }}
        
        /* Global Background & Font */
        .stApp {{
            background-color: var(--background);
            color: var(--text);
            font-family: 'Inter', sans-serif;
            transition: background-color 0.5s ease;
        }}

        /* Typography */
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: var(--text) !important;
            transition: color 0.5s ease;
        }}

        h1, h2, h3 {{
            color: var(--primary) !important;
            font-weight: 700;
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Premium Glassmorphism Cards */
        .metric-card {{
            background: var(--cards);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 25px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border: 1px solid var(--border);
            transition: all 0.3s ease;
            animation: fadeIn 0.6s ease-out forwards;
            height: 100%;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(255, 126, 182, 0.15);
        }}
        
        .metric-title {{
            font-size: 0.9rem;
            color: var(--text-sec) !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .metric-value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary) !important;
        }}
        
        /* Buttons */
        .stButton>button {{
            background: linear-gradient(135deg, var(--primary), #E0609B);
            color: white !important;
            border: none;
            border-radius: 25px;
            padding: 0.6rem 2.5rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(255, 126, 182, 0.3);
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 6px 20px rgba(255, 126, 182, 0.4);
        }}
        
        /* Tabs Premium Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 15px;
            background: transparent;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: var(--cards);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 12px 25px;
            border: 1px solid var(--border);
            color: var(--text-sec);
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--primary) !important;
            color: white !important;
            border: none;
            box-shadow: 0 4px 15px rgba(255, 126, 182, 0.3);
        }}
        
        .stTabs [aria-selected="true"] p, .stTabs [aria-selected="true"] span {{
            color: white !important;
        }}

        /* Upload / Input Sections */
        .stTextInput>div>div>input, .stNumberInput>div>div>input, .stDateInput>div>div>input, .stSelectbox>div>div>div {{
            background-color: var(--background) !important;
            color: var(--text) !important;
            border: 1px solid var(--border) !important;
            border-radius: 15px !important;
            padding: 10px 15px;
            transition: all 0.3s ease;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
        }}
        
        .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus, .stDateInput>div>div>input:focus {{
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(255, 126, 182, 0.2) !important;
        }}

        /* Sidebar & Extra components */
        section[data-testid="stSidebar"] {{
            background-color: var(--cards) !important;
            backdrop-filter: blur(15px);
            border-right: 1px solid var(--border);
        }}

        /* Sakura Decor Effects */
        .sakura-container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            overflow: hidden;
        }}

        @keyframes fall {{
            0% {{ transform: translateY(-10px) rotate(0deg); opacity: 0; }}
            20% {{ opacity: 0.6; }}
            100% {{ transform: translateY(100vh) rotate(360deg); opacity: 0; }}
        }}
        
        .petal {{
            position: absolute;
            font-size: 1.2rem;
            animation: fall linear infinite;
            color: #FFB7D5;
            filter: blur(1px);
        }}

        /* -------------------------------------
           MOBILE-FIRST RESPONSIVE OPTIMIZATIONS
           ------------------------------------- */
           
        /* General touch spacing */
        button, input, select, textarea {{
            touch-action: manipulation;
        }}

        /* Tablets (768px and down) */
        @media (max-width: 768px) {{
            .metric-card {{
                padding: 20px;
                margin-bottom: 15px;
            }}
            .metric-value {{
                font-size: 1.6rem;
            }}
            .stButton>button {{
                width: 100%;
                padding: 0.8rem;
            }}
        }}

        /* Large Phones (414px and down) */
        @media (max-width: 414px) {{
            h1 {{ font-size: 2.2rem !important; }}
            h2 {{ font-size: 1.8rem !important; }}
            h3 {{ font-size: 1.5rem !important; }}
            .metric-card {{
                padding: 15px;
                border-radius: 20px;
            }}
            .metric-title {{
                font-size: 0.8rem;
            }}
            .metric-value {{
                font-size: 1.4rem;
            }}
        }}

        /* Medium Phones (390px and down) */
        @media (max-width: 390px) {{
            h1 {{ font-size: 2rem !important; }}
            .metric-card {{
                padding: 12px;
            }}
            .metric-value {{
                font-size: 1.3rem;
            }}
            .stTabs [data-baseweb="tab"] {{
                padding: 8px 12px;
                font-size: 0.9rem;
            }}
        }}

        /* Small Phones (360px and down) */
        @media (max-width: 360px) {{
            h1 {{ font-size: 1.8rem !important; }}
            .metric-value {{
                font-size: 1.2rem;
            }}
            .stButton>button {{
                padding: 0.6rem;
                font-size: 0.9rem;
            }}
        }}

    </style>
    """
    
    # Add subtle floating sakura petals only if not dark mode (or could be in both, user said Sakura aesthetics)
    # Just a few subtle elements so it doesn't block content.
    sakura_html = """
    <div class="sakura-container">
        <div class="petal" style="left: 10%; animation-duration: 15s; animation-delay: 0s;">🌸</div>
        <div class="petal" style="left: 30%; animation-duration: 22s; animation-delay: 5s; font-size: 0.8rem;">✨</div>
        <div class="petal" style="left: 60%; animation-duration: 18s; animation-delay: 2s;">🌸</div>
        <div class="petal" style="left: 85%; animation-duration: 25s; animation-delay: 7s; font-size: 1.5rem;">🦋</div>
    </div>
    """
    
    st.markdown(custom_css + sakura_html, unsafe_allow_html=True)

def metric_card(title, value, subtitle=""):
    """Render a styled premium metric card."""
    st.markdown(f"""
        <div class="metric-card" style="display: flex; flex-direction: column; justify-content: center;">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div style="font-size: 0.85rem; color: var(--text-sec); margin-top: 8px; font-weight: 500;">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

def get_logo_svg(width=40, height=40):
    """Return the Crescent Moon SVG string."""
    return f"""
    <svg width="{width}" height="{height}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">
        <defs>
            <linearGradient id="moonGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FF7EB6"/>
                <stop offset="100%" stop-color="#C4A7F4"/>
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="2" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="url(#moonGradient)" filter="url(#glow)"/>
    </svg>
    """
