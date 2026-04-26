import streamlit as st
import bcrypt
import re
import os
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import UPLOAD_FOLDER 

# --- CONFIGURATION ---
SENDER_EMAIL = "rubaisha1705@gmail.com" 
SENDER_PASSWORD = "eibe nkmf wozh edfw" 

# --- 🛑 PATHS SETUP (FIXED) ---
# Hum Project ka Main Folder (Root) hardcode kar rahe hain
# Taake 'root_dir' error na aaye aur DB bhi sahi jagah mile.
root_dir = r"C:\Users\DELL\Desktop\Financial_Profiler_FYP"

# Database aur Uploads dono isi folder mein honge
DB_PATH = os.path.join(root_dir, "users.db")

# --- VALIDATION ---
def validate_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def validate_phone(phone): return re.match(r"^03\d{9}$", phone)
def validate_name(name): return re.match(r"^[A-Za-z\s]+$", name)

# --- EMAIL FUNCTION ---
def send_email_otp(to_email, subject="Verification Code"):
    otp = str(random.randint(1000, 9999))
    if "your_email" in SENDER_EMAIL: return otp, False
    
    msg = MIMEMultipart()
    msg['From'] = "FinAnalyze Support"
    msg['To'] = to_email
    msg['Subject'] = f"{subject} - FinAnalyze"
    body = f"Hello,\n\nYour Verification Code is: {otp}\n\nValid for 10 minutes."
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return otp, True
    except Exception as e:
        print(f"Email Error: {e}")
        return otp, False

# --- COMPATIBILITY WRAPPER (To prevent app.py from breaking) ---
def run_query(query, params=(), commit=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return True
        else:
            return cursor.fetchall()
    except Exception as e:
        return []
    finally:
        if 'conn' in locals(): conn.close()

# --- CREATE USER (PROFESSIONAL MODE) ---
def create_user(username, email, phone, password, full_name, img_data, role='user'):
    # 1. Paths Setup (Hardcoded for stability)
    DESKTOP_PATH = r"C:\Users\DELL\Desktop\Financial_Profiler_FYP"
    REAL_DB_PATH = os.path.join(DESKTOP_PATH, "users.db")
    REAL_UPLOAD_DIR = os.path.join(DESKTOP_PATH, "uploads")
    
    # 2. Hashing
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # 3. Image Logic
    FINAL_IMAGE_PATH = None 
    
    if img_data:
        try:
            if not os.path.exists(REAL_UPLOAD_DIR):
                os.makedirs(REAL_UPLOAD_DIR)
            
            clean_name = "default.png"
            
            # CASE A: Dictionary
            if isinstance(img_data, dict):
                clean_name = f"{username}_{img_data.get('name', 'profile.png')}".replace(" ", "_")
                full_file_path = os.path.join(REAL_UPLOAD_DIR, clean_name)
                with open(full_file_path, "wb") as f:
                    f.write(img_data['data'])
            
            # CASE B: Direct Upload
            else:
                clean_name = f"{username}_{img_data.name}".replace(" ", "_")
                full_file_path = os.path.join(REAL_UPLOAD_DIR, clean_name)
                with open(full_file_path, "wb") as f: 
                    f.write(img_data.getbuffer())
            
            FINAL_IMAGE_PATH = f"uploads/{clean_name}"
            
        except Exception as e:
            # Sirf agar koi major error ho toh print karein, warna silent
            print(f"Image Save Error: {e}")

    # 4. Database Entry
    conn = None
    try:
        conn = sqlite3.connect(REAL_DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO users (username, email, phone_number, password, full_name, profile_pic, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
            (username, email, phone, hashed, full_name, FINAL_IMAGE_PATH, role, 1)
        )
        conn.commit()
        return True
        
    except Exception as e:
        return f"Database Error: {str(e)}"
    finally:
        if conn: conn.close()

def update_user_profile(uid, full_name, phone, img_file):
    # Existing logic remains same, just using absolute path
    query = "UPDATE users SET full_name = ?, phone_number = ? WHERE id = ?"
    params = [full_name, phone, uid]
    if img_file:
        try:
            upload_dir = os.path.join(root_dir, "uploads")
            if not os.path.exists(upload_dir): os.makedirs(upload_dir)
            clean_name = f"updated_{uid}_{img_file.name}".replace(" ", "_")
            full_path = os.path.join(upload_dir, clean_name)
            with open(full_path, "wb") as f: f.write(img_file.getbuffer())
            db_path = f"uploads/{clean_name}"
            query = "UPDATE users SET full_name = ?, phone_number = ?, profile_pic = ? WHERE id = ?"
            params = [full_name, phone, db_path, uid]
            if 'user' in st.session_state and st.session_state['user']:
                st.session_state['user']['pic'] = db_path
        except Exception: pass
    run_query(query, tuple(params), commit=True)

# Helper functions
def login_user(u, p): pass
def show_auth_page(): pass