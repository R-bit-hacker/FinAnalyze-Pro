import streamlit as st
import os
import base64
from utils import show_footer, get_icon

def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return ""

def show_landing_page():
    
    # --- HERO SECTION ---
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style="padding-top: 40px; animation: fadeIn 1s ease-out;">
            <div style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; background: rgba(0, 198, 255, 0.1); border-radius: 30px; border: 1px solid rgba(0, 198, 255, 0.2); margin-bottom: 20px;">
                """ + get_icon('chart', '#00c6ff', 18) + """
                <span style="color: #00c6ff; font-weight: 600; font-size: 0.8rem; letter-spacing: 1px;">AI-POWERED FINANCE</span>
            </div>
            <h1 style="font-size: 4rem; line-height: 1.1; font-weight: 800; margin-top: 15px; margin-bottom: 20px;">
                Master Your Money <br>
                <span class="gradient-text">With Data Science.</span>
            </h1>
            <p style="font-size: 1.2rem; color: #b0b0b0; line-height: 1.6; margin-bottom: 35px;">
                Stop guessing. Get a personalized financial persona, track habits, and receive AI-driven wealth advice instantly.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        b1, b2 = st.columns([1, 1.5])
        with b1:
            if st.button("GET STARTED", type="primary", use_container_width=True):
                st.session_state['page'] = 'auth'
                st.rerun()
        with b2:
            if st.button("VIEW DEMO", use_container_width=True):
                st.session_state['page'] = 'demo' # Links to Demo Page
                st.rerun()

    with col2:
        # --- VISUAL MOCKUP (No Emojis) ---
        st.markdown("""
        <div style="position: relative; margin-top: 20px; animation: float 6s ease-in-out infinite;">
            <div class="glass-card" style="background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02)); border: 1px solid rgba(255,255,255,0.1); padding: 30px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:20px;">
                    <div>
                        <div style="font-size:0.8rem; color:#888; letter-spacing: 1px;">TOTAL SAVINGS</div>
                        <div style="font-size:2rem; font-weight:700; color:white;">PKR 124,500</div>
                    </div>
                    """ + get_icon('wallet', '#00c6ff', 32) + """
                </div>
                <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin: 20px 0;">
                    <div style="width: 75%; height: 100%; background: linear-gradient(90deg, #00c6ff, #0072ff); border-radius: 2px;"></div>
                </div>
                <div style="display:flex; justify-content: space-between; align-items: center;">
                    <div style="display:flex; align-items:center; gap:10px;">
                         """ + get_icon('check', '#00f260', 20) + """
                        <div>
                            <div style="font-size:0.9rem; color:white; font-weight:600;">Smart Saver</div>
                            <div style="font-size:0.7rem; color:#aaa;">AI Persona Identified</div>
                        </div>
                    </div>
                    <div style="font-size:0.8rem; color:#00f260;">+15% this month</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- FEATURES GRID ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-size: 2.5rem; font-weight: 800;'>Why Choose FinAnalyze?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#888; margin-bottom:50px;'>Enterprise-grade security meets consumer simplicity.</p>", unsafe_allow_html=True)
    
    f1, f2, f3 = st.columns(3)
    
    def feature_card(icon_name, icon_color, title, desc):
        return f"""
        <div class="glass-card" style="height:100%; text-align:left;">
            <div style="margin-bottom:20px;">{get_icon(icon_name, icon_color, 40)}</div>
            <h3 style="margin-bottom:10px; color:white; font-size: 1.3rem;">{title}</h3>
            <p style="color:#aaa; font-size:0.95rem; line-height: 1.6;">{desc}</p>
        </div>
        """

    with f1: st.markdown(feature_card("lock", "#00f260", "Bank-Grade Security", "Your data is hashed with bcrypt and encrypted in transit. We prioritize privacy."), unsafe_allow_html=True)
    with f2: st.markdown(feature_card("bulb", "#00c6ff", "AI Persona Engine", "ML algorithms decode spending habits to find your unique financial DNA."), unsafe_allow_html=True)
    with f3: st.markdown(feature_card("target", "#ff0844", "Precision Insights", "Get real-time feedback on 50/30/20 rule adherence and actionable steps."), unsafe_allow_html=True)

    # --- TEAM SECTION ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    my_pic = get_img_as_base64(os.path.join(base_dir, "data", "me.jpg"))
    ayesha_pic = get_img_as_base64(os.path.join(base_dir, "data", "ayesha.jpg"))
    
    if not my_pic: my_pic = "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
    else: my_pic = f"data:image/jpeg;base64,{my_pic}"
    if not ayesha_pic: ayesha_pic = "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"
    else: ayesha_pic = f"data:image/jpeg;base64,{ayesha_pic}"

    st.markdown(f"""
    <div style="text-align:center;">
        <h2 style="font-weight: 800;">Built by Students, for Students.</h2>
        <br><br>
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;">
            <div class="glass-card" style="width: 280px; padding: 30px; text-align: center;">
                <img src="{my_pic}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 2px solid #00c6ff; padding: 4px;">
                <h3 style="margin-top: 20px; font-size: 1.2rem;">Rubaisha Munir</h3>
                <p style="color: #00c6ff; font-weight: 600; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;">Lead Developer</p>
                <p style="color: #888; font-size: 0.85rem; margin-top: 10px;">Full Stack Architecture & AI</p>
            </div>
            <div class="glass-card" style="width: 280px; padding: 30px; text-align: center;">
                <img src="{ayesha_pic}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover; border: 2px solid #fff; padding: 4px;">
                <h3 style="margin-top: 20px; font-size: 1.2rem;">Ayesha Nadeem</h3>
                <p style="color: #fff; font-weight: 600; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;">Data Analyst</p>
                <p style="color: #888; font-size: 0.85rem; margin-top: 10px;">Dataset Curation & Research</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    show_footer()