import sqlite3
import bcrypt
import os

# Absolute path 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "users.db")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")

def init_db():
    # 1. Ensure UPLOAD_DIR exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # 2. Users Table (IF NOT EXISTS added)
    c.execute('''
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

    # 3. Analysis History Table (IF NOT EXISTS added)
    c.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
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
    
    # 4. Super Admin (Sirf tab insert hoga agar admin table khali ho)
    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        admin_pass = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, email, phone_number, password, full_name, role, is_verified) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                  ("admin", "admin@finanalyze.com", "03001234567", admin_pass, "Super Administrator", "admin", 1))
        print("👤 Super Admin created.")

    conn.commit()
    conn.close()
    print("✅ Database check complete (Tables are ready)!")

if __name__ == "__main__":
    init_db()