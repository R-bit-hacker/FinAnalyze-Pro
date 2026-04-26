import streamlit as st
import sqlite3
import os
import streamlit.components.v1 as components

# --- CONFIG ---
GROQ_API_KEY = "your_key_here"

# --- SMART PATH SYSTEM ---
def get_paths():
    # Get the directory where utils.py is located (src)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Go up one level to find the Project Root (Financial_Profiler_FYP)
    root_dir = os.path.dirname(current_dir)
    
    # Define paths relative to the root
    db_path = os.path.join(root_dir, "users.db")
    upload_folder = os.path.join(root_dir, "uploads")
    csv_path = os.path.join(root_dir, "data", "user_profiles_with_clusters.csv")
    models_dir = os.path.join(root_dir, "models")
    
    return db_path, upload_folder, csv_path, models_dir, root_dir

# Initialize Paths
DB_PATH, UPLOAD_FOLDER, CSV_PATH, MODELS_DIR, ROOT_DIR = get_paths()

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- DATABASE HELPER ---
def run_query(query, params=(), commit=False):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    try:
        c.execute(query, params)
        if commit: conn.commit()
        res = c.fetchall() if not commit else True
        return res
    except Exception as e: return str(e)
    finally: conn.close()

# --- SCROLL TO TOP FUNCTION ---
def scroll_to_top():
    js = """
    <script>
        var body = window.parent.document.querySelector(".main");
        if (body) { body.scrollTop = 0; }
    </script>
    """
    st.components.v1.html(js, height=0, width=0)

# --- HISTORY FUNCTIONS ---
def save_analysis_to_db(user_id, inc, exp, sav, dbt, persona):
    query = "INSERT INTO analysis_history (user_id, income, expense, savings, debt, persona) VALUES (?, ?, ?, ?, ?, ?)"
    run_query(query, (user_id, inc, exp, sav, dbt, persona), commit=True)

def get_user_history(user_id):
    query = "SELECT income, expense, savings, debt, persona, timestamp FROM analysis_history WHERE user_id = ? ORDER BY timestamp DESC"
    return run_query(query, (user_id,))

# --- ICON ENGINE (COMPLETE) ---
def get_icon(name, color="#00c6ff", size=24):
    """Returns a professional SVG icon string."""
    icons = {
        "dashboard": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>',
        "history": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>',
        "wallet": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"></path><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"></path><path d="M18 12a2 2 0 0 0-2 2c0 1.1.9 2 2 2h4v-4h-4z"></path></svg>',
        "chart": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10"></path><path d="M12 20V4"></path><path d="M6 20v-6"></path></svg>',
        "target": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle></svg>',
        "mail": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>',
        "phone": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>',
        "lock": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>',
        "bulb": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="9" y1="18" x2="15" y2="18"></line><line x1="10" y1="22" x2="14" y2="22"></line><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 12 3 4.65 4.65 0 0 0 7.5 7.5c0 2.15 1.1 3.9 2.91 4.5"></path><path d="M12 18v-2"></path><path d="M12 7v-2"></path></svg>',
        "edit": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>',
        "check": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>'
    }
    return icons.get(name, "")

# --- STYLING ENGINE (FIXED) ---
def apply_styling():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
            
            [data-testid="stAppViewContainer"] {
                background-color: #000000;
                background-image: 
                    radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
                    radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
                    radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
                background-attachment: fixed;
                color: #e0e0e0;
                font-family: 'Outfit', sans-serif;
            }

            /* ✅ FIX: Make Sidebar Button & Header Visible */
            header {
                visibility: visible !important;
                background: transparent !important;
            }
            /* Hide Default Footer only */
            footer {visibility: hidden;}
            
            #MainMenu {visibility: visible;}
            
            /* Sidebar Styling */
            section[data-testid="stSidebar"] {
                display: block !important;
                visibility: visible !important;
                background-color: rgba(10, 10, 20, 0.95);
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
            button[kind="header"] {
                display: block !important;
                visibility: visible !important;
                color: white !important;
            }

            /* Glassmorphism Cards */
            .glass-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 25px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, border-color 0.3s ease;
            }
            .glass-card:hover {
                transform: translateY(-3px);
                border-color: rgba(0, 242, 96, 0.5);
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            }

            .stButton > button {
                white-space: nowrap !important;
                background: linear-gradient(135deg, #2b5876 0%, #4e4376 100%);
                border: none; color: white; padding: 12px 24px; border-radius: 12px;
                font-weight: 600; width: 100%; transition: all 0.3s;
            }
            .stButton > button:hover { transform: scale(1.02); box-shadow: 0 5px 15px rgba(78, 67, 118, 0.4); }
            
            div[data-testid="stHorizontalBlock"] button { background: transparent; border: 1px solid rgba(255,255,255,0.3); border-radius: 30px; }
            div[data-testid="stHorizontalBlock"] button:hover { background: white; color: black; border-color: white; }

            .stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
                background-color: rgba(0,0,0,0.3) !important; border: 1px solid rgba(255,255,255,0.2) !important;
                color: white !important; border-radius: 10px !important;
            }
            .gradient-text {
                background: linear-gradient(to right, #00c6ff, #0072ff);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;
            }
            div[data-testid="stPlotlyChart"] {
                background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px; padding: 15px; transition: transform 0.3s ease;
            }
            div[data-testid="stPlotlyChart"]:hover { transform: translateY(-5px); border-color: rgba(0, 198, 255, 0.5); }

            /* FOOTER LINKS */
            .footer-link div.stButton > button {
                background-color: transparent !important;
                border: none !important;
                color: #a0a0a0 !important;
                padding: 0px !important;
                margin: 0px !important;
                text-align: left !important;
                display: inline-block !important;
                width: auto !important;
                box-shadow: none !important;
                font-weight: 400 !important;
                height: auto !important;
                line-height: 1.5 !important;
                text-decoration: none !important;
            }
            .footer-link div.stButton > button:hover {
                color: #00f260 !important;
                text-decoration: none !important;
                transform: translateX(5px) !important;
                background-color: transparent !important;
            }
            .social-icon { transition: transform 0.2s; }
            .social-icon:hover { transform: scale(1.2); }
        </style>
    """, unsafe_allow_html=True)

# --- GLOBAL FOOTER (COMPLETE) ---
def show_footer():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(0,0,0,0.6); padding: 60px 0; border-top: 1px solid rgba(255,255,255,0.05);">
    """, unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    
    with c1:
        st.markdown("""
            <h3 style="color: white; margin-bottom: 15px; font-weight: 800; font-size: 1.8rem;">FinAnalyze.</h3>
            <p style="color: #888; font-size: 0.9rem; line-height: 1.6; max-width: 300px;">
                Decoding financial DNA with advanced AI. Empowering the next generation of wealth builders.
            </p>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("<h4 style='color: #fff; margin-bottom: 20px; font-size: 1.1rem;'>Company</h4>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="footer-link">', unsafe_allow_html=True)
            if st.button("About Us", key="f_about"): st.session_state['page'] = 'about'; st.rerun()
            if st.button("Contact Support", key="f_contact"): st.session_state['page'] = 'contact'; st.rerun()
            if st.button("Development Team", key="f_team"): st.session_state['page'] = 'landing'; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown("<h4 style='color: #fff; margin-bottom: 20px; font-size: 1.1rem;'>Legal</h4>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="footer-link">', unsafe_allow_html=True)
            if st.button("Privacy Policy", key="f_privacy"): st.session_state['page'] = 'privacy'; st.rerun()
            if st.button("Terms of Service", key="f_terms"): st.session_state['page'] = 'terms'; st.rerun()
            if st.button("Cookie Policy", key="f_cookies"): st.session_state['page'] = 'cookies'; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown("<h4 style='color: #fff; margin-bottom: 20px; font-size: 1.1rem;'>Connect</h4>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; gap: 15px;">
            <a href="https://linkedin.com" target="_blank" class="social-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
            </a>
            <a href="https://facebook.com" target="_blank" class="social-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path></svg>
            </a>
            <a href="https://instagram.com" target="_blank" class="social-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <hr style="border-color: rgba(255,255,255,0.05); margin: 30px 0;">
        <div style="text-align: center; color: #555; font-size: 0.8rem;">
            © 2026 FinAnalyze Pro. All Rights Reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)