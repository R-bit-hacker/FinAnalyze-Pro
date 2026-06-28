import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from utils import get_db

def promote_user(username):
    db = get_db()
    if not db:
        print("❌ Firebase not initialized.")
        return
        
    docs = db.collection('users').where('username', '==', username).limit(1).stream()
    doc = next(docs, None)
    
    if doc:
        print(f"User found! Current Role: {doc.to_dict().get('role')}")
        doc.reference.update({"role": "admin"})
        print(f"✅ Congratulations: '{username}' is now an admin!")
    else:
        print(f"❌ User '{username}' is not found in database. Check the spellings.")

# --- NICHE APNA USERNAME LIKHEIN ---
promote_user("rubaishamunir")