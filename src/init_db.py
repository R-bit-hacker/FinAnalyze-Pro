import bcrypt
import os
import sys

# Setup path so we can import utils
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from utils import get_db

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

def init_db():
    # 1. Ensure UPLOAD_DIR exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    db = get_db()
    if not db:
        print("❌ Firebase not initialized. Make sure firebase_credentials.json is in the root directory.")
        return

    # 4. Super Admin (Sirf tab insert hoga agar admin user na ho)
    docs = db.collection('users').where('username', '==', 'admin').limit(1).stream()
    if not next(docs, None):
        admin_pass = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db.collection('users').document().set({
            "username": "admin",
            "email": "admin@finanalyze.com",
            "phone_number": "03001234567",
            "password": admin_pass,
            "full_name": "Super Administrator",
            "role": "admin",
            "is_verified": 1
        })
        print("👤 Super Admin created.")
    else:
        print("👤 Super Admin already exists.")

    print("✅ Database check complete (Firebase is ready)!")

if __name__ == "__main__":
    init_db()