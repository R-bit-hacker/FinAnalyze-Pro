import sqlite3
import bcrypt
import os

DB_NAME = "users.db"
UPLOAD_DIR = "uploads"

def init_db():
    # 1. Cleanup old DB
    if os.path.exists(DB_NAME):
        try:
            os.remove(DB_NAME)
            print("🗑️ Old database removed.")
        except PermissionError:
            print("⚠️ Error: Close the app first (Ctrl+C in terminal).")
            return
    
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 2. Users Table
    c.execute('''
        CREATE TABLE users (
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

    # 3. NEW: Analysis History Table
    c.execute('''
        CREATE TABLE analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            income REAL,
            expense REAL,
            savings REAL,
            debt REAL,
            persona TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # 4. Super Admin
    admin_pass = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, email, phone_number, password, full_name, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              ("admin", "admin@finanalyze.com", "03001234567", admin_pass, "Super Administrator", "admin", 1))

    conn.commit()
    conn.close()
    print("✅ Database Initialized with History Table!")

if __name__ == "__main__":
    init_db()