import streamlit as st
import os
import base64
import pandas as pd
import requests
from PIL import Image
import re

# Import ROOT_DIR from utils to avoid hardcoding
from utils import apply_styling, get_paths, ROOT_DIR
from auth import update_user_profile, login_user, create_user
from dashboard import show_dashboard
from chatbot import show_chatbot
from about_us import show_about_page
from contact_us import show_contact_page
from privacy_policy import show_privacy_page
from landing_page import show_landing_page
from legal_pages import show_terms_page, show_cookies_page
from demo import show_demo_page
from admin_panel import show_admin_panel

# --- 🚀 DB INITIALIZATION (FIXED PATH) ---
from init_db import init_db

# --- VALIDATION FUNCTIONS ---
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_strong_password(password):
    if len(password) < 8: return False, "Must be at least 8 characters long."
    if not re.search(r"[A-Z]", password): return False, "Must contain at least one uppercase letter (A-Z)."
    if not re.search(r"[a-z]", password): return False, "Must contain at least one lowercase letter (a-z)."
    if not re.search(r"\d", password): return False, "Must contain at least one number (0-9)."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False, "Must contain at least one special character (e.g., @, #, $)."
    return True, "Valid"

def is_valid_image(uploaded_file):
    if uploaded_file is None: 
        return True, "No image"
    try:
        img = Image.open(uploaded_file)
        width, height = img.size
        if width < 150 or height < 150:
            return False, f"Image is too small ({width}x{height}). Minimum resolution must be 150x150 pixels."
        return True, "Valid"
    except Exception as e:
        return False, "Invalid file format."
# -----------------------------

# Initialize Firebase and Admin User
init_db()

# --- CONFIG ---
st.set_page_config(
    page_title="FinAnalyze Pro", 
    page_icon="🔹",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_styling()

# --- 🛠️ FIX: FORCE SIDEBAR VISIBILITY ---
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
        button[kind="header"] {
            display: block !important;
            visibility: visible !important;
        }
    </style>
""", unsafe_allow_html=True) 

# --- STATE ---
if 'user' not in st.session_state: st.session_state['user'] = None
if 'page' not in st.session_state: st.session_state['page'] = 'landing'
if 'report' not in st.session_state: st.session_state['report'] = None

# --- NAVBAR ---
def show_navbar():
    st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
    c_logo, c_home, c_about, c_contact, c_privacy = st.columns([6, 1, 1, 1, 1.2])
    
    with c_logo:
        st.markdown("### <span style='color:#00c6ff'>🔹</span> FinAnalyze Pro", unsafe_allow_html=True)
    
    with c_home:
        if st.button("Home", key="nav_home"):
            st.session_state['page'] = 'landing'; st.rerun()
    with c_about:
        if st.button("About", key="nav_about"):
            st.session_state['page'] = 'about'; st.rerun()
    with c_contact:
        if st.button("Contact", key="nav_contact"):
            st.session_state['page'] = 'contact'; st.rerun()
    with c_privacy:
        if st.button("Privacy", key="nav_privacy"):
            st.session_state['page'] = 'privacy'; st.rerun()
    
    st.markdown("---")



def render_privacy_policy():
    if st.button("Return to Application", key="back_from_privacy"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Privacy Policy")
    st.markdown('''**Effective Date: June 2026**\n\n**1. Data Collection and Zero-Storage Architecture**\nFinAnalyze employs an ephemeral data processing model. Financial statements (PDF/CSV) uploaded to the platform are parsed in-memory strictly for real-time analysis. We do not persistently store raw transaction logs, bank account numbers, or routing details on our servers. Upon session termination, all uploaded artifacts are immediately purged.\n\n**2. Artificial Intelligence and Third-Party APIs**\nTo facilitate advanced financial profiling, we utilize secure external APIs. Only anonymized, aggregated numerical parameters are transmitted for processing. No Personally Identifiable Information (PII) is utilized for training third-party machine learning models.\n\n**3. Cryptographic Security**\nUser authentication is secured via industry-standard hashing protocols (Bcrypt). Platform administrators do not have access to plaintext user passwords.\n\n**4. Data Retention and User Rights**\nUsers retain full control over their historical analysis logs and may request complete account deletion via our Support channels at any time.''')

def render_terms():
    if st.button("Return to Application", key="back_from_terms"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Terms of Service")
    st.markdown('''**Effective Date: June 2026**\n\n**1. Acceptance of Terms**\nBy accessing the FinAnalyze platform, you agree to be bound by these Terms of Service. This platform is designed strictly for educational and analytical modeling.\n\n**2. Nature of Service and Limitations**\nFinAnalyze utilizes K-Means clustering and predictive algorithms to simulate financial trajectories. These outputs are automated estimations and do not constitute certified financial, tax, or investment advice. Users should consult registered financial advisors before making critical financial decisions.\n\n**3. User Obligations**\nUsers are required to ensure that uploaded documents are appropriately redacted. Do not upload documents containing highly sensitive, unredacted credentials during this prototype phase. You are responsible for maintaining the confidentiality of your authentication credentials.\n\n**4. Limitation of Liability**\nWhile we strive for high analytical accuracy, financial markets are subject to volatility. FinAnalyze and its developers hold no liability for financial losses or discrepancies arising from reliance on the platform's automated projections.''')

def render_cookie():
    if st.button("Return to Application", key="back_from_cookie"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Cookie and Session Policy")
    st.markdown('''**1. Session State Management**\nFinAnalyze does not utilize traditional tracking cookies. Instead, we rely on native framework session states to maintain secure authentication and seamless navigation across the dashboard modules.\n\n**2. Essential Functionality**\nThese session states are strictly necessary. They preserve user interface preferences (such as theme selection) and temporarily retain analytical inputs to prevent data loss during module transitions.\n\n**3. Exclusivity of Tracking**\nWe do not deploy marketing pixels, third-party analytics trackers, or cross-site tracking mechanisms. User session data is confined entirely to the active application lifecycle and is not monetized or shared with external advertising entities.''')

# --- ROUTING LOGIC ---



# 0. OTHER PAGES (Highest Priority to avoid shadowing)
if st.session_state['page'] == 'about': show_navbar(); show_about_page()
elif st.session_state['page'] == 'contact': show_navbar(); show_contact_page()
elif st.session_state['page'] == 'demo': show_navbar(); show_demo_page()
elif st.session_state['page'] == 'privacy': render_privacy_policy()
elif st.session_state['page'] == 'terms': render_terms()
elif st.session_state['page'] == 'cookie': render_cookie()

# 1. LANDING PAGE
elif st.session_state['page'] == 'landing':

    show_navbar()
    show_landing_page() 

# 2. AUTH PAGE
elif st.session_state['page'] == 'auth':
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        st.markdown("<h2 style='text-align: center;'>Secure Access</h2>", unsafe_allow_html=True)
        tab_login, tab_register = st.tabs(["Login", "Register"])
        
        # --- LOGIN TAB UPDATE (WITH FORGOT PASSWORD) ---
        with tab_login:
            # Session state for Forgot Password flow
            if 'forgot_step' not in st.session_state: 
                st.session_state.forgot_step = 0
            
            # --- STATE 0: NORMAL LOGIN ---
            if st.session_state.forgot_step == 0:
                st.markdown("### Welcome Back")
                with st.form("login_form"):
                    e_login = st.text_input("Email Address").lower().strip()
                    p_login = st.text_input("Password", type="password")
                    
                    if st.form_submit_button("Sign In", use_container_width=True):
                        if e_login and p_login:
                            with st.spinner("Verifying..."):
                                user_data = login_user(e_login, p_login)
                                if user_data:
                                    st.toast(f"Welcome back, {user_data['name']}!", icon="👋")
                                    st.session_state['user'] = user_data 
                                    st.session_state['page'] = 'dashboard'
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid email or password.")
                        else:
                            st.warning("Please enter both email and password.")
                
                # Forgot Password Button (Form ke bahar)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Forgot Password?", key="forgot_btn"):
                    st.session_state.forgot_step = 1
                    st.rerun()

            # --- STATE 1: ENTER EMAIL ---
            elif st.session_state.forgot_step == 1:
                st.markdown("### Reset Password")
                st.caption("Enter your registered email address to receive a verification code.")
                
                reset_email = st.text_input("Email Address").lower().strip()
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Send OTP", use_container_width=True, type="primary"):
                        from auth import check_email_exists, send_email_otp
                        if check_email_exists(reset_email):
                            with st.spinner("Sending code..."):
                                otp, sent = send_email_otp(reset_email, "Password Reset Code")
                                if sent:
                                    st.session_state.reset_email = reset_email
                                    st.session_state.sent_code = otp
                                    st.session_state.forgot_step = 2
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to send email. Check your internet or email config.")
                        else:
                            st.error("❌ This email is not registered with us.")
                with c2:
                    if st.button("Back to Login", use_container_width=True):
                        st.session_state.forgot_step = 0
                        st.rerun()

            # --- STATE 2: VERIFY OTP ---
            elif st.session_state.forgot_step == 2:
                st.markdown("### Verify OTP")
                st.info(f"Code sent to {st.session_state.reset_email}")
                
                entered_code = st.text_input("Enter 4-digit Code")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Verify Code", use_container_width=True, type="primary"):
                        expected = st.session_state.sent_code
                        print(f"Expected: '{expected}', Entered: '{entered_code}'")
                        if str(entered_code).strip() == str(expected).strip():
                            st.session_state.forgot_step = 3
                            st.rerun()
                        else:
                            st.error("❌ Invalid Code. Please try again.")
                with c2:
                    if st.button("Cancel", use_container_width=True):
                        st.session_state.forgot_step = 0
                        st.rerun()

            # --- STATE 3: SET NEW PASSWORD ---
            elif st.session_state.forgot_step == 3:
                st.markdown("### Create New Password")
                
                with st.form("new_password_form"):
                    new_pw = st.text_input("New Password", type="password")
                    conf_pw = st.text_input("Confirm New Password", type="password")
                    
                    if st.form_submit_button("Save New Password", use_container_width=True):
                        if len(new_pw) < 6:
                            st.warning("Password must be at least 6 characters long.")
                        elif new_pw != conf_pw:
                            st.error("❌ Passwords do not match!")
                        else:
                            from auth import reset_user_password
                            reset_user_password(st.session_state.reset_email, new_pw)
                            st.success("✅ Password reset successfully! Please login with your new password.")
                            st.session_state.forgot_step = 0
                            st.rerun()

        # --- REGISTER TAB ---
        with tab_register:
            if 'signup_step' not in st.session_state: st.session_state.signup_step = 1
            if 'signup_data' not in st.session_state: st.session_state.signup_data = {}
            if 'signup_otp' not in st.session_state: st.session_state.signup_otp = None

            if st.session_state.signup_step == 1:
                st.markdown("### Create Account")
                with st.form("register_step1"):
                    new_user = st.text_input("Username").lower().strip()
                    new_fullname = st.text_input("Full Name")
                    new_email = st.text_input("Email").lower().strip()
                    new_phone = st.text_input("Phone")
                    new_pass = st.text_input("Password", type="password")
                    new_img = st.file_uploader("Profile Picture", type=['jpg', 'png', 'jpeg'])
                    if st.form_submit_button("Verify & Continue", use_container_width=True):
                        # 0. Missing Field Check
                        if not (new_user and new_email and new_pass):
                            st.error("❌ Required fields missing. Username, Email, and Password are mandatory.")
                        
                        # 1. Email Check
                        elif not is_valid_email(new_email):
                            st.error("❌ Invalid Email! Please enter a valid email format (e.g., ali@gmail.com).")
                            
                        # 2. Password Check
                        else:
                            is_valid_pass, pass_msg = is_strong_password(new_pass)
                            if not is_valid_pass:
                                st.error(f"❌ Weak Password: {pass_msg}")
                                
                            # 3. Profile Picture Check
                            else:
                                is_valid_img = True
                                img_msg = ""
                                if new_img is not None:
                                    is_valid_img, img_msg = is_valid_image(new_img)
                                    
                                if not is_valid_img:
                                    st.error(f"❌ Invalid Profile Picture: {img_msg}")
                                    
                                # 4. Agar sab theek hai toh asli kaam karein
                                else:
                                    from auth import send_email_otp
                                    img_storage = None
                                    if new_img is not None:
                                        try:
                                            img_storage = {"name": new_img.name, "type": new_img.type, "data": new_img.getvalue()}
                                        except: pass
                                    
                                    with st.spinner("Sending code..."):
                                        otp, sent = send_email_otp(new_email, "Verify Account")
                                        if sent:
                                            st.session_state.sent_code = otp
                                            st.session_state.signup_data = {'u': new_user, 'e': new_email, 'ph': new_phone, 'p': new_pass, 'n': new_fullname, 'img': img_storage}
                                            st.session_state.signup_step = 2
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to send OTP. Check internet connection.")

            elif st.session_state.signup_step == 2:
                st.markdown("### Verify Email")
                st.info(f"Code sent to {st.session_state.signup_data.get('e')}")
                entered_code = st.text_input("Enter Code")
                if st.button("Complete Registration", use_container_width=True):
                    expected = st.session_state.sent_code
                    print(f"Expected: '{expected}', Entered: '{entered_code}'")
                    if str(entered_code).strip() == str(expected).strip():
                        d = st.session_state.signup_data
                        result = create_user(d['u'], d['e'], d['ph'], d['p'], d['n'], d['img'])
                        if result == True:
                            st.success("Account Created. Now go to Login tab.")
                            st.session_state.signup_step = 1
                        else:
                            st.error(f"Failed: {result}")
                    else:
                        st.error("Invalid Code")
                if st.button("Back"):
                    st.session_state.signup_step = 1
                    st.rerun()

# 3. LOGGED IN USER
elif st.session_state['user']:
    user = st.session_state['user']
    with st.sidebar:
        img_to_show = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        if user.get('pic'):
            full_path = os.path.join(ROOT_DIR, user['pic'])
            if os.path.exists(full_path):
                img_to_show = Image.open(full_path)
        
        st.image(img_to_show, width=150)
        st.title(f"Hello, {user['name']}")
        menu = st.radio("Navigate", ["Analysis Hub", "Edit Profile", "FinBot AI"] if user['role'] != 'admin' else ["Admin Panel", "Edit Profile"])
        if st.button("Logout", icon="🔒"):
            st.session_state['user'] = None
            st.session_state['page'] = 'landing'
            st.rerun()

    if menu == "Analysis Hub": show_dashboard(user)
    elif menu == "Edit Profile": 
        st.title("Profile Settings")
        
        # Tabs Create Karein (Aapki images ke mutabiq)
        tab_personal, tab_security = st.tabs(["📝 Personal Info", "🔒 Security & Password"])
        
        # --- TAB 1: PERSONAL INFO ---
        with tab_personal:
            with st.form("edit_profile_form"):
                new_name = st.text_input("Full Name", value=user.get('name', ''))
                new_phone = st.text_input("Phone", value=user.get('phone', ''))
                new_pic = st.file_uploader("Update Picture", type=['jpg', 'png', 'jpeg'], help="Drag and drop file here. Limit 200MB per file - JPG, PNG, JPEG")
                
                if st.form_submit_button("Save Profile Changes", type="primary"):
                    from auth import update_user_profile
                    
                    # Agar nayi picture upload hui hai toh data prepare karein
                    img_data = None
                    if new_pic is not None:
                        img_data = {"name": new_pic.name, "data": new_pic.getvalue()}
                        
                    # Profile update function call karein
                    update_user_profile(user['id'], user['username'], new_name, new_phone, img_data)
                    st.success("✅ Profile Updated Successfully! Please logout and login again to see the changes.")

        # --- TAB 2: SECURITY & PASSWORD ---
        with tab_security:
            st.markdown("### Change Your Password")
            st.caption("If your Admin gave you a default password (e.g., 123456), please change it immediately for security.")
            
            with st.form("edit_password_form"):
                current_pw = st.text_input("Current Password", type="password")
                new_pw = st.text_input("New Password", type="password")
                confirm_pw = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password", type="primary"):
                    if not current_pw or not new_pw or not confirm_pw:
                        st.warning("⚠️ Please fill in all password fields.")
                    elif new_pw != confirm_pw:
                        st.error("❌ New passwords do not match!")
                    elif len(new_pw) < 6:
                        st.error("❌ Password must be at least 6 characters long.")
                    else:
                        from auth import update_user_password
                        res = update_user_password(user['username'], current_pw, new_pw)
                        
                        if res == True:
                            st.success("✅ Password Updated Successfully! Please login again with your new password.")
                            # Security feature: Password change ke baad session expire kar dein
                            st.session_state['user'] = None 
                            st.rerun()
                        else:
                            st.error(f"❌ {res}")
    elif menu == "FinBot AI": show_chatbot()
    elif menu == "Admin Panel": show_admin_panel(user)

# 4. OTHER PAGES
elif st.session_state['page'] == 'about': show_navbar(); show_about_page()
elif st.session_state['page'] == 'contact': show_navbar(); show_contact_page()
elif st.session_state['page'] == 'privacy': show_navbar(); show_privacy_page()
elif st.session_state['page'] == 'demo': show_navbar(); show_demo_page()