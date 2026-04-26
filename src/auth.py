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

# --- 🛑 PATHS SETUP ---
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
    msg = MIMEMultipart()
    msg['From'] = "FinAnalyze Support"
    msg['To'] = to_email
    msg['Subject'] = f"{subject} - FinAnalyze"
    body = f"Hello,\n\nYour Verification Code is: {otp}"
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return otp, True
    except:
        return otp, False

# --- 🚨 FIXED COMPATIBILITY WRAPPER ---
def run_query(query, params=(), commit=False):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL,
            phone_number TEXT, password TEXT NOT NULL, full_name TEXT,
            profile_pic TEXT, role TEXT DEFAULT 'user', is_verified INTEGER DEFAULT 0)''')
        cursor.execute(query, params)
        if commit:
            conn.commit()
            return True
        return cursor.fetchall()
    except Exception as e:
        print(f"DB Error: {e}")
        return False if commit else []
    finally:
        conn.close()

# --- LOGIN USER ---
def login_user(username, password):
    results = run_query("SELECT id, username, password, full_name, role, profile_pic FROM users WHERE username = ?", (username,))
    if results and len(results) > 0:
        uid, uname, hashed_pw, fname, role, pic = results[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
            return {"id": uid, "name": fname, "username": uname, "role": role, "pic": pic}
    return None

# --- CREATE USER ---
def create_user(username, email, phone, password, full_name, img_data, role='user'):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Database mein seedha insert karein
    query = "INSERT INTO users (username, email, phone_number, password, full_name, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?)"
    params = (username, email, phone, hashed, full_name, role, 1)
    return run_query(query, params, commit=True)

def update_user_profile(uid, full_name, phone, img_file):
    query = "UPDATE users SET full_name = ?, phone_number = ? WHERE id = ?"
    run_query(query, (full_name, phone, uid), commit=True)