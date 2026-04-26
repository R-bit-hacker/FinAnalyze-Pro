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

# --- 🛑 PATHS SETUP (DYNAMIC & FINAL FIX) ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(base_dir, "users.db")
REAL_UPLOAD_DIR = os.path.join(base_dir, "uploads")

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
        return otp, False

# --- COMPATIBILITY WRAPPER ---
def run_query(query, params=(), commit=False):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number TEXT,
                password TEXT NOT NULL,
                full_name TEXT,
                profile_pic TEXT,
                role TEXT DEFAULT 'user',
                is_verified INTEGER DEFAULT 0
            )
        ''')
        
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

# --- LOGIN USER ---
def login_user(username, password):
    results = run_query("SELECT id, username, password, full_name, role, profile_pic FROM users WHERE username = ?", (username,))
    if results:
        uid, uname, hashed_pw, fname, role, pic = results[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
            return {"id": uid, "name": fname, "username": uname, "role": role, "pic": pic}
    return None

# --- CREATE USER ---
def create_user(username, email, phone, password, full_name, img_data, role='user'):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    FINAL_IMAGE_PATH = None 
    
    if img_data:
        try:
            if not os.path.exists(REAL_UPLOAD_DIR): os.makedirs(REAL_UPLOAD_DIR)
            clean_name = f"{username}_{img_data.name if hasattr(img_data, 'name') else 'profile.png'}".replace(" ", "_")
            full_file_path = os.path.join(REAL_UPLOAD_DIR, clean_name)
            with open(full_file_path, "wb") as f: 
                f.write(img_data.getbuffer() if hasattr(img_data, 'getbuffer') else img_data['data'])
            FINAL_IMAGE_PATH = f"uploads/{clean_name}"
        except: pass

    res = run_query(
        "INSERT INTO users (username, email, phone_number, password, full_name, profile_pic, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (username, email, phone, hashed, full_name, FINAL_IMAGE_PATH, role, 1),
        commit=True
    )
    return res

def update_user_profile(uid, full_name, phone, img_file):
    query = "UPDATE users SET full_name = ?, phone_number = ? WHERE id = ?"
    params = [full_name, phone, uid]
    if img_file:
        try:
            if not os.path.exists(REAL_UPLOAD_DIR): os.makedirs(REAL_UPLOAD_DIR)
            clean_name = f"updated_{uid}_{img_file.name}".replace(" ", "_")
            full_path = os.path.join(REAL_UPLOAD_DIR, clean_name)
            with open(full_path, "wb") as f: f.write(img_file.getbuffer())
            db_path = f"uploads/{clean_name}"
            query = "UPDATE users SET full_name = ?, phone_number = ?, profile_pic = ? WHERE id = ?"
            params = [full_name, phone, db_path, uid]
            if 'user' in st.session_state and st.session_state['user']:
                st.session_state['user']['pic'] = db_path
        except: pass
    run_query(query, tuple(params), commit=True)