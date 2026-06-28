import pandas as pd
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from utils import get_db

def check_users():
    db = get_db()
    if not db:
        print("❌ Firebase not initialized.")
        return

    docs = db.collection('users').stream()
    data = []
    for doc in docs:
        u = doc.to_dict()
        data.append({
            "id": doc.id,
            "username": u.get('username'),
            "full_name": u.get('full_name'),
            "role": u.get('role')
        })

    df = pd.DataFrame(data)
    print("\n--- DATABASE REPORT ---")
    print(df)
    print("-----------------------")

if __name__ == "__main__":
    check_users()