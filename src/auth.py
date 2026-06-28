import streamlit as st
import bcrypt
import re
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils import UPLOAD_FOLDER, get_db
from PIL import Image

# --- VALIDATION FUNCTIONS ---
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_strong_password(password):
    if len(password) < 8: return False, "Kam az kam 8 characters hone chahiye."
    if not re.search(r"[A-Z]", password): return False, "Ek capital letter (A-Z) hona chahiye."
    if not re.search(r"[a-z]", password): return False, "Ek small letter (a-z) hona chahiye."
    if not re.search(r"\d", password): return False, "Ek number (0-9) hona chahiye."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): return False, "Ek special character (e.g., @, #, $) hona chahiye."
    return True, "Valid"

def is_valid_image(uploaded_file):
    if uploaded_file is None: 
        return True, "No image"
    try:
        img = Image.open(uploaded_file)
        width, height = img.size
        if width < 150 or height < 150:
            return False, f"Picture choti hai ({width}x{height}). Minimum 150x150 pixels honi chahiye."
        return True, "Valid"
    except Exception as e:
        return False, "File format theek nahi hai."

# --- CONFIGURATION ---
SENDER_EMAIL = "rubaisha1705@gmail.com" 
SENDER_PASSWORD = "eibe nkmf wozh edfw" 

# --- 🛑 PATHS SETUP ---
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

# --- LOGIN USER ---
def login_user(username, password):
    db = get_db()
    if not db: return None
    
    docs = db.collection('users').where('username', '==', username).limit(1).stream()
    for doc in docs:
        user_data = doc.to_dict()
        hashed_pw = user_data.get('password') or user_data.get('password_hash')
        
        if hashed_pw:
            db_hash_bytes = hashed_pw.encode('utf-8') if isinstance(hashed_pw, str) else hashed_pw
            if bcrypt.checkpw(password.encode('utf-8'), db_hash_bytes):
                return {
                    "id": doc.id,
                    "name": user_data.get('full_name', ''),
                    "username": user_data.get('username', ''),
                    "role": user_data.get('role', 'user'),
                    "pic": user_data.get('profile_pic', '')
                }
    return None

# --- CREATE USER ---
def create_user(username, email, phone, password, full_name, img_data, role='user'):
    db = get_db()
    if not db: return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
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

    doc_ref = db.collection('users').document()
    doc_ref.set({
        "username": username,
        "email": email,
        "phone_number": phone,
        "password": hashed,
        "full_name": full_name,
        "profile_pic": pic_path,
        "role": role,
        "is_verified": 1
    })
    return True

# --- UPDATE PROFILE & PICTURE ---
def update_user_profile(uid, username, full_name, phone, img_data=None):
    db = get_db()
    if not db: return
    
    doc_ref = db.collection('users').document(uid)
    update_data = {
        "full_name": full_name,
        "phone_number": phone
    }
    
    if img_data and 'data' in img_data:
        file_name = f"{username}_profile.png"
        pic_path = os.path.join(REAL_UPLOAD_DIR, file_name)
        try:
            # File save karein
            with open(pic_path, "wb") as f:
                f.write(img_data['data'])
            
            rel_pic_path = f"uploads/{file_name}"
            update_data["profile_pic"] = rel_pic_path
        except Exception as e:
            print(f"Error saving updated image: {e}")
            
    doc_ref.update(update_data)

# --- UPDATE PASSWORD ---
def update_user_password(username, current_password, new_password):
    db = get_db()
    if not db: return "Database connection error."
    
    docs = db.collection('users').where('username', '==', username).limit(1).stream()
    doc = next(docs, None)
    
    if doc:
        user_data = doc.to_dict()
        hashed_pw = user_data.get('password') or user_data.get('password_hash')
        
        db_hash_bytes = hashed_pw.encode('utf-8') if isinstance(hashed_pw, str) else hashed_pw
        
        if bcrypt.checkpw(current_password.encode('utf-8'), db_hash_bytes):
            new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            doc.reference.update({"password": new_hashed})
            return True
        else:
            return "Incorrect current password."
    return "User not found in database."

# --- CHECK IF EMAIL EXISTS ---
def check_email_exists(email):
    db = get_db()
    if not db: return False
    
    docs = db.collection('users').where('email', '==', email).limit(1).stream()
    return next(docs, None) is not None

# --- FORGOT PASSWORD RESET ---
def reset_user_password(email, new_password):
    db = get_db()
    if not db: return False
    
    docs = db.collection('users').where('email', '==', email).limit(1).stream()
    doc = next(docs, None)
    
    if doc:
        new_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        doc.reference.update({"password": new_hashed})
        return True
    return False