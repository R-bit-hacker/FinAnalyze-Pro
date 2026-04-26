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
    
    pic_path = ""
    # Agar user ne picture upload ki hai, toh pehle usko save karein
    if img_data and 'data' in img_data:
        file_name = f"{username}_profile.png"
        pic_path = os.path.join(REAL_UPLOAD_DIR, file_name)
        try:
            with open(pic_path, "wb") as f:
                f.write(img_data['data'])
            # Database mein save karne ke liye relative path use karein
            pic_path = f"uploads/{file_name}"
        except Exception as e:
            print(f"Image save error: {e}")

    # Database query mein profile_pic add karein
    query = "INSERT INTO users (username, email, phone_number, password, full_name, profile_pic, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    params = (username, email, phone, hashed, full_name, pic_path, role, 1)
    
    return run_query(query, params, commit=True)

# --- UPDATE PROFILE & PICTURE ---
def update_user_profile(uid, username, full_name, phone, img_data=None):
    if img_data and 'data' in img_data:
        file_name = f"{username}_profile.png"
        pic_path = os.path.join(REAL_UPLOAD_DIR, file_name)
        try:
            # File save karein
            with open(pic_path, "wb") as f:
                f.write(img_data['data'])
            
            # Database mein path aur baqi data update karein
            rel_pic_path = f"uploads/{file_name}"
            query = "UPDATE users SET full_name = ?, phone_number = ?, profile_pic = ? WHERE id = ?"
            run_query(query, (full_name, phone, rel_pic_path, uid), commit=True)
        except Exception as e:
            print(f"Error saving updated image: {e}")
    else:
        # Agar picture upload nahi ki toh sirf text data update karein
        query = "UPDATE users SET full_name = ?, phone_number = ? WHERE id = ?"
        run_query(query, (full_name, phone, uid), commit=True)

# --- UPDATE PASSWORD ---
def update_user_password(username, current_password, new_password):
    # 1. Pehle current password verify karein
    results = run_query("SELECT password FROM users WHERE username = ?", (username,))
    if results and len(results) > 0:
        hashed_pw = results[0][0]
        
        # Kya purana password theek hai?
        if bcrypt.checkpw(current_password.encode('utf-8'), hashed_pw):
            # 2. Naya password hash karein aur DB mein save karein
            new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            query = "UPDATE users SET password = ? WHERE username = ?"
            run_query(query, (new_hashed, username), commit=True)
            return True
        else:
            return "Incorrect current password."
    return "User not found in database."

    # --- CHECK IF EMAIL EXISTS ---
def check_email_exists(email):
    results = run_query("SELECT id FROM users WHERE email = ?", (email,))
    return True if results and len(results) > 0 else False

# --- FORGOT PASSWORD RESET ---
def reset_user_password(email, new_password):
    new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    query = "UPDATE users SET password = ? WHERE email = ?"
    run_query(query, (new_hashed, email), commit=True)
    return True