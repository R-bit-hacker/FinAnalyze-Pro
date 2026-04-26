import streamlit as st
import os
import base64
import pandas as pd
import requests
from PIL import Image

# Import ROOT_DIR from utils to avoid hardcoding
from utils import apply_styling, run_query, get_paths, ROOT_DIR
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

# Exact path dhoondne ke liye dynamic logic
db_file = os.path.join(os.getcwd(), "users.db")
if not os.path.exists(db_file):
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

# --- ROUTING LOGIC ---

# 1. LANDING PAGE
if st.session_state['page'] == 'landing':
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
                    u_login = st.text_input("Username")
                    p_login = st.text_input("Password", type="password")
                    
                    if st.form_submit_button("Sign In", use_container_width=True):
                        if u_login and p_login:
                            with st.spinner("Verifying..."):
                                user_data = login_user(u_login, p_login)
                                if user_data:
                                    st.toast(f"Welcome back, {user_data['name']}!", icon="👋")
                                    st.session_state['user'] = user_data 
                                    st.session_state['page'] = 'dashboard'
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid username or password.")
                        else:
                            st.warning("Please enter both username and password.")
                
                # Forgot Password Button (Form ke bahar)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Forgot Password?", key="forgot_btn"):
                    st.session_state.forgot_step = 1
                    st.rerun()

            # --- STATE 1: ENTER EMAIL ---
            elif st.session_state.forgot_step == 1:
                st.markdown("### Reset Password")
                st.caption("Enter your registered email address to receive a verification code.")
                
                reset_email = st.text_input("Email Address")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Send OTP", use_container_width=True, type="primary"):
                        from auth import check_email_exists, send_email_otp
                        if check_email_exists(reset_email):
                            with st.spinner("Sending code..."):
                                otp, sent = send_email_otp(reset_email, "Password Reset Code")
                                if sent:
                                    st.session_state.reset_email = reset_email
                                    st.session_state.reset_otp = otp
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
                
                entered_otp = st.text_input("Enter 4-digit Code")
                
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Verify Code", use_container_width=True, type="primary"):
                        if entered_otp == st.session_state.reset_otp:
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
                    new_user = st.text_input("Username")
                    new_fullname = st.text_input("Full Name")
                    new_email = st.text_input("Email")
                    new_phone = st.text_input("Phone")
                    new_pass = st.text_input("Password", type="password")
                    new_img = st.file_uploader("Profile Picture", type=['jpg', 'png', 'jpeg'])
                    if st.form_submit_button("Verify & Continue", use_container_width=True):
                        if new_user and new_email and new_pass:
                            from auth import send_email_otp
                            img_storage = None
                            if new_img is not None:
                                try:
                                    img_storage = {"name": new_img.name, "type": new_img.type, "data": new_img.getvalue()}
                                except: pass
                            otp, sent = send_email_otp(new_email, "Verify Account")
                            st.session_state.signup_otp = otp
                            st.session_state.signup_data = {'u': new_user, 'e': new_email, 'ph': new_phone, 'p': new_pass, 'n': new_fullname, 'img': img_storage}
                            st.session_state.signup_step = 2
                            st.rerun()
                        else:
                            st.error("Required fields missing")

            elif st.session_state.signup_step == 2:
                st.markdown("### Verify Email")
                st.info(f"Code sent to {st.session_state.signup_data.get('e')}")
                otp_check = st.text_input("Enter Code")
                if st.button("Complete Registration", use_container_width=True):
                    if otp_check == st.session_state.signup_otp:
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