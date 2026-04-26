import streamlit as st
import os
import base64
import pandas as pd
import requests
from PIL import Image

# Import ROOT_DIR from utils to avoid hardcoding
from utils import apply_styling, run_query, get_paths, ROOT_DIR
from auth import show_auth_page, update_user_profile
from dashboard import show_dashboard
from chatbot import show_chatbot
from about_us import show_about_page
from contact_us import show_contact_page
from privacy_policy import show_privacy_page
from landing_page import show_landing_page
from legal_pages import show_terms_page, show_cookies_page
from demo import show_demo_page
from admin_panel import show_admin_panel

# --- 🚀 DB INITIALIZATION ---
from init_db import init_db
# Check if DB exists in current directory, if not, create it
if not os.path.exists(os.path.join(os.getcwd(), "users.db")):
    init_db()
else:
    # Optional: ensure tables are there without wiping data
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
        /* Sidebar ko zabardasti dikhao */
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
        }
        /* Agar toggle button gayab hai to wapis lao */
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
        
        # --- LOGIN TAB ---
        with tab_login:
            st.markdown("### Welcome Back")
            with st.form("login_form"):
                u_login = st.text_input("Username")
                p_login = st.text_input("Password", type="password")
                
                # Button
                if st.form_submit_button("Sign In", use_container_width=True):
                    if u_login and p_login:
                        with st.spinner("Verifying credentials..."):
                            try:
                                API_URL = "https://rubaisha-finanalyze-api.hf.space"
                                response = requests.post(
                                    f"{API_URL}/login", 
                                    json={"username": u_login, "password": p_login},
                                    timeout=10 
                                )
                                
                                if response.status_code == 200:
                                    data = response.json()
                                    st.toast(f"Welcome back, {data['user_data']['name']}!", icon="👋")
                                    st.session_state['user'] = data['user_data'] 
                                    st.session_state['page'] = 'dashboard'
                                    st.rerun()
                                else:
                                    try:
                                        err_msg = response.json().get("detail", "Login Failed")
                                    except:
                                        err_msg = "Invalid credentials"
                                    st.error(f"❌ {err_msg}")
                                    
                            except requests.exceptions.ConnectionError:
                                st.error("🔌 Service Unavailable. Please try again later.")
                            except Exception as e:
                                st.error("⚠️ An unexpected error occurred. Please contact support.")
                    else:
                        st.warning("Please enter both username and password.")

        # --- REGISTER TAB (FULL LOGIC PRESERVED) ---
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
                            from auth import validate_email, send_email_otp
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
                        from auth import create_user
                        d = st.session_state.signup_data
                        result = create_user(d['u'], d['e'], d['ph'], d['p'], d['n'], d['img'])
                        if result == True:
                            st.success("Account Created.")
                            st.session_state.signup_step = 1
                            st.session_state.signup_data = {}
                        else:
                            st.error(f"Failed: {result}")
                    else:
                        st.error("Invalid Code")
                if st.button("Back"):
                    st.session_state.signup_step = 1
                    st.rerun()

# 3. LOGGED IN USER (UPDATED SECTION)
elif st.session_state['user']:
    user = st.session_state['user']

    # --- 1. DETERMINE MENU BASED ON ROLE ---
    if user.get('role') == 'admin':
        # Admin gets specialized menu
        menu_options = ["Admin Panel", "Edit Profile"]
        # Default index handling if needed (Streamlit handles it by name match usually)
    else:
        # Standard User Menu
        menu_options = ["Analysis Hub", "Edit Profile", "FinBot AI"]

    # --- 2. SIDEBAR WITH IMAGE FIX ---
    with st.sidebar:
        # Image Logic
        img_to_show = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
        
        if user.get('pic'):
            full_path = os.path.join(ROOT_DIR, user['pic'])
            if os.path.exists(full_path):
                img_to_show = Image.open(full_path)
        
        # ✅ FIX: Increased width to prevent blur
        st.image(img_to_show, width=150)
        
        st.title(f"Hello, {user['name']}")
        st.caption(f"Role: {user['role'].upper()}")
        
        st.divider()
        
        # Dynamic Menu based on Role
        menu = st.radio("Navigate", menu_options)

        st.divider()
        # LOGOUT BUTTON
        if st.button("Logout", icon="🔒"):
            st.session_state['user'] = None
            st.session_state['page'] = 'landing'
            st.rerun()

    # --- PAGE ROUTING ---
    if menu == "Analysis Hub":
        show_dashboard(user)
        
    elif menu == "Edit Profile":
        st.title("Profile Settings")
        
        # Tabs
        tab1, tab2 = st.tabs(["📝 Personal Info", "🔒 Security & Password"])
        
        # --- TAB 1: PERSONAL INFO ---
        with tab1:
            with st.form("edit_profile_form"):
                nn = st.text_input("Full Name", value=user['name'])
                nph = st.text_input("Phone", value=user.get('phone', ''), max_chars=11)
                nimg = st.file_uploader("Update Picture", type=['jpg', 'png', 'jpeg'])
                if st.form_submit_button("Save Profile Changes", type="primary"):
                    update_user_profile(user['id'], nn, nph, nimg)
                    st.success("Profile Updated Successfully!")
                    # Session state update so that name changes immediately
                    st.session_state['user']['name'] = nn
                    st.session_state['user']['phone'] = nph
                    st.rerun()
                    
        # --- TAB 2: CHANGE PASSWORD ---
        with tab2:
            st.markdown("#### Change Your Password")
            st.caption("If your Admin gave you a default password (e.g., 123456), please change it immediately for security.")
            
            with st.form("change_password_form"):
                curr_pw = st.text_input("Current Password", type="password")
                new_pw = st.text_input("New Password", type="password")
                conf_pw = st.text_input("Confirm New Password", type="password")
                
                if st.form_submit_button("Update Password", type="primary"):
                    if not curr_pw or not new_pw or not conf_pw:
                        st.warning("⚠️ Please fill in all password fields.")
                    elif new_pw != conf_pw:
                        st.error("❌ New passwords do not match!")
                    elif len(new_pw) < 6:
                        st.error("❌ New password must be at least 6 characters long.")
                    else:
                        with st.spinner("Updating password securely..."):
                            try:
                                import requests
                                API_URL = "http://127.0.0.1:8000"
                                res = requests.post(
                                    f"{API_URL}/change-password",
                                    json={
                                        "user_id": user['id'],
                                        "current_password": curr_pw,
                                        "new_password": new_pw
                                    }
                                )
                                if res.status_code == 200:
                                    st.success("✅ Password updated successfully! Next time, log in with your new password.")
                                else:
                                    err = res.json().get('detail', 'Update failed')
                                    st.error(f"❌ {err}")
                            except Exception as e:
                                st.error("🔌 Backend server is unreachable.")
        
    elif menu == "FinBot AI":
        show_chatbot()
        
    elif menu == "Admin Panel":
        # Only accessible via menu logic if role is admin
        show_admin_panel(user)

# 4. OTHER PAGES
elif st.session_state['page'] == 'about': show_navbar(); show_about_page()
elif st.session_state['page'] == 'contact': show_navbar(); show_contact_page()
elif st.session_state['page'] == 'privacy': show_navbar(); show_privacy_page()
elif st.session_state['page'] == 'terms': show_navbar(); show_terms_page()
elif st.session_state['page'] == 'cookies': show_navbar(); show_cookies_page()
elif st.session_state['page'] == 'demo': show_navbar(); show_demo_page()