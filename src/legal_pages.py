import streamlit as st
from utils import show_footer, get_icon, scroll_to_top

def show_terms_page():
    scroll_to_top()
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center;">
        <h1 class="gradient-text">Terms of Service</h1>
        <p style="color: #888;">Effective Date: January 1, 2026</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # --- FIX: HTML string ko bilkul left align kar diya hai ---
    st.markdown("""
<div class="glass-card">
    <h3>1. Acceptance of Terms</h3>
    <p style="color:#aaa; line-height: 1.6;">By accessing and using FinAnalyze Pro, you accept and agree to be bound by the terms and provision of this agreement.</p>
    <br>
    <h3>2. Use of Service</h3>
    <p style="color:#aaa; line-height: 1.6;">This service is provided for educational and informational purposes only. The financial personas generated are based on AI algorithms and should not be considered as professional financial advice.</p>
    <br>
    <h3>3. User Accounts</h3>
    <p style="color:#aaa; line-height: 1.6;">You are responsible for maintaining the security of your account credentials. FinAnalyze cannot and will not be liable for any loss or damage from your failure to comply with this security obligation.</p>
    <br>
    <h3>4. Termination</h3>
    <p style="color:#aaa; line-height: 1.6;">We reserve the right to terminate or suspend your access to our service immediately, without prior notice or liability, for any reason whatsoever, including without limitation if you breach the Terms.</p>
</div>
""", unsafe_allow_html=True)
    
    show_footer()

def show_cookies_page():
    scroll_to_top()
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center;">
        <h1 class="gradient-text">Cookie Policy</h1>
        <p style="color: #888;">Understanding how we handle your session.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)

    # --- FIX: HTML string ko bilkul left align kar diya hai ---
    st.markdown(f"""
<div class="glass-card">
    <div style="display:flex; gap:15px; align-items:center; margin-bottom:20px;">
        {get_icon('bulb', '#00c6ff', 30)}
        <h3 style="margin:0;">What are Cookies?</h3>
    </div>
    <p style="color:#aaa;">Cookies are small pieces of text sent to your web browser by a website you visit. A cookie file is stored in your web browser and allows the Service or a third-party to recognize you and make your next visit easier and the Service more useful to you.</p>
</div>

<div class="glass-card">
    <h3>How FinAnalyze Uses Cookies</h3>
    <ul style="color:#aaa; line-height:1.8;">
        <li><b>Essential Cookies:</b> We use these to authenticate users and prevent fraudulent use of user accounts. Without these, the login functionality would not work.</li>
        <li><b>Session Cookies:</b> To remember your state (like which tab you are viewing) as you navigate through the app.</li>
        <li><b>No Tracking:</b> We do <u>not</u> use cookies for advertising or tracking your browsing history outside of this application.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
    
    show_footer()