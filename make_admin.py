import sqlite3
import os

# Kyunki file root folder mein hai, db bhi yahin hai
db_file = "users.db"

def promote_user(username):
    if not os.path.exists(db_file):
        print(f"❌ Error: Database file '{db_file}' nahi mili!")
        return

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    
    # Check current user
    c.execute("SELECT role FROM users WHERE username = ?", (username,))
    res = c.fetchone()
    
    if res:
        print(f"User found! Current Role: {res[0]}")
        # Update to admin
        c.execute("UPDATE users SET role = 'admin' WHERE username = ?", (username,))
        conn.commit()
        print(f"✅ Congratulations: '{username}' is now an admin!")
    else:
        print(f"❌ User '{username}' is not found in database. Check the spellings.")
        
    conn.close()

# --- NICHE APNA USERNAME LIKHEIN ---
promote_user("rubaishamunir")