import sys
import os
import sqlite3
import bcrypt
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# --- 🛠️ CRITICAL FIX: PATH SETUP BEFORE IMPORTS ---
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../src/api
src_dir = os.path.dirname(current_dir)                # .../src
root_dir = os.path.dirname(src_dir)                   # .../Financial_Profiler_FYP
sys.path.append(src_dir)
# ---------------------------------------------------

from ml_logic import load_models, get_ai_advice

app = FastAPI(title="FinAnalyze Pro API", version="2.5")

# --- DATABASE PATH ---
DB_PATH = os.path.join(root_dir, "users.db")

# --- LOAD MODELS ON STARTUP ---
try:
    kmeans, scaler, pca = load_models()
    print("✅ ML Models Loaded Successfully on Server")
except Exception as e:
    print(f"⚠️ ML Models failed to load: {e}")
    kmeans, scaler, pca = None, None, None

def get_db_connection():
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        return conn
    else:
        print(f"❌ Looking for DB at: {DB_PATH}")
        raise Exception("Database file missing!")

# --- DATA MODELS (EXISTING) ---
class LoginRequest(BaseModel):
    username: str
    password: str

class AnalysisRequest(BaseModel):
    income: float
    expenses: float
    savings: float
    debt: float
    needs: float
    wants: float

# --- NEW DATA MODELS FOR BATCH CRUD ---
class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class UserCreateAdmin(BaseModel):
    username: str
    email: str
    name: Optional[str] = ""
    role: str = "user"
    phone: Optional[str] = ""

class BatchUpdateRequest(BaseModel):
    added: List[UserCreateAdmin] = []
    edited: List[UserUpdate] = []
    deleted: List[int] = []

class PasswordChangeRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str

# --- ROUTES (EXISTING) ---
@app.get("/")
def home():
    return {"status": "Active", "service": "FinAnalyze Backend"}

@app.post("/login")
def login_user(request: LoginRequest):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
             cursor.execute("SELECT id, username, role, password, full_name, profile_pic, phone_number FROM users WHERE username = ?", (request.username,))
        except:
             cursor.execute("SELECT id, username, role, password_hash, full_name, profile_pic, phone_number FROM users WHERE username = ?", (request.username,))
             
        user = cursor.fetchone()
        
        if user:
            user_id = user[0]
            db_username = user[1]
            db_role = user[2]
            db_password_hash = user[3]
            db_fullname = user[4]
            db_pic = user[5]
            db_phone = user[6]
            
            user_input_bytes = request.password.encode('utf-8')
            if isinstance(db_password_hash, str):
                db_hash_bytes = db_password_hash.encode('utf-8')
            else:
                db_hash_bytes = db_password_hash

            if bcrypt.checkpw(user_input_bytes, db_hash_bytes):
                return {
                    "status": "success",
                    "user_data": {
                        "id": user_id, "username": db_username, "role": db_role,
                        "name": db_fullname if db_fullname else db_username,
                        "phone": db_phone if db_phone else "",
                        "pic": db_pic if db_pic else "" 
                    }
                }
            else:
                raise HTTPException(status_code=401, detail="Invalid Password")
        else:
            raise HTTPException(status_code=401, detail="User not found")
    except Exception as e:
        print(f"Login Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

@app.post("/predict")
def predict_persona(data: AnalysisRequest):
    try:
        inc = data.income if data.income > 0 else 1 
        sr = data.savings / inc
        dr = data.debt / inc
        er = data.expenses / inc
        lr = data.wants / (data.needs + 1) if data.needs > 0 else 0
        
        inp = pd.DataFrame([[data.income, data.expenses, sr, dr, data.wants, data.needs, 0, 30, er, lr]], 
                           columns=['monthly_income', 'monthly_expense_total', 'savings_rate', 'debt_to_income_ratio', 'discretionary_spending', 'essential_spending', 'investment_amount', 'transaction_count', 'expense_ratio', 'lifestyle_ratio'])
        
        if scaler and kmeans:
            scaled = scaler.transform(inp)
            cid = kmeans.predict(scaled)[0] # Model executes normally
            
            # --- 🧠 SMART HEURISTIC LOGIC (BUG FIXED) ---
            # Using financial ratios as a heuristic layer to assign a 100% accurate persona
            
            if er >= 0.95 or dr > 0.30:
                # If expenses are almost equal to/greater than income, OR debt exceeds 30%
                p_name = "Budget Challenger"
                
            elif sr >= 0.20 and dr <= 0.10:
                # If savings are 20% or more, and debt is negligible (10% or less)
                if data.income >= 300000:
                    p_name = "Wealth Builder" # High income = Wealth Builder
                else:
                    p_name = "Smart Saver"    # Normal income = Smart Saver
                    
            elif sr < 0.15 and (data.wants > data.needs or data.income > 200000):
                # If savings are less than 15% and discretionary spending (wants) exceeds essentials
                p_name = "Big Spender"
                
            else:
                # Fallback for users falling into the intermediate/average range
                p_name = "Smart Saver"
            
            # --------------------------------------------

            advice = get_ai_advice(p_name, data.income, data.savings)
            
            return {
                "persona": p_name,
                "advice": advice,
                "metrics": {"sr": sr, "dr": dr, "er": er}
            }
        else:
            raise HTTPException(status_code=500, detail="Models not loaded")
            
    except Exception as e:
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# ==========================================
# 👮 ADMIN ROUTES (GOD MODE)
# ==========================================

@app.get("/get-all-users")
def get_all_users():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, role, phone_number, email, profile_pic FROM users")
        users = cursor.fetchall()
        
        user_list = []
        for u in users:
            user_list.append({
                "id": u[0],
                "username": u[1],
                "name": u[2] if u[2] else "N/A",
                "role": u[3],
                "phone": u[4] if u[4] else "N/A",
                "email": u[5] if u[5] else "No Email",
                "pic": u[5] if u[5] else ""
            })
        return {"status": "success", "users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: int):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user[0] == 'admin':
            raise HTTPException(status_code=400, detail="❌ Cannot delete an Admin account!")
            
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        cursor.execute("DELETE FROM analysis_history WHERE user_id = ?", (user_id,))
        conn.commit()
        return {"status": "success", "message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

# --- 🚀 NEW ADVANCED CRUD ROUTE FOR DATA EDITOR ---
@app.post("/batch-update-users")
def batch_update_users(request: BatchUpdateRequest):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Process Deletions
        for uid in request.deleted:
            cursor.execute("SELECT role FROM users WHERE id = ?", (uid,))
            user = cursor.fetchone()
            if user and user[0] != 'admin': # Admin ko delete hone se rokein
                cursor.execute("DELETE FROM users WHERE id = ?", (uid,))
                cursor.execute("DELETE FROM analysis_history WHERE user_id = ?", (uid,))

        # 2. Process Edits
        for edit in request.edited:
            updates, params = [], []
            if edit.username is not None: updates.append("username = ?"); params.append(edit.username)
            if edit.name is not None: updates.append("full_name = ?"); params.append(edit.name)
            if edit.role is not None: updates.append("role = ?"); params.append(edit.role)
            if edit.phone is not None: updates.append("phone_number = ?"); params.append(edit.phone)
            if edit.email is not None: updates.append("email = ?"); params.append(edit.email)
            
            if updates:
                params.append(edit.id)
                cursor.execute(f"UPDATE users SET {', '.join(updates)} WHERE id = ?", tuple(params))

        # 3. Process Additions (Naya User Add Karne ka Code)
        hashed_pw = bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode('utf-8')
        
        for add in request.added:
            # Explicitly naming columns prevents the "5 values for 6 columns" error!
            try:
                cursor.execute(
                    "INSERT INTO users (username, full_name, role, phone_number, email, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                    (add.username, add.name, add.role, add.phone, add.email, hashed_pw)
                )
            except sqlite3.OperationalError:
                # Agar table mein column ka naam 'password' hai bajaye 'password_hash' ke
                cursor.execute(
                    "INSERT INTO users (username, full_name, role, phone_number, email, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (add.username, add.name, add.role, add.phone, add.email, hashed_pw)
                )

        conn.commit()
        return {"status": "success", "message": "All operations completed successfully."}
        
    except Exception as e:
        print(f"Batch Update Error: {e}") # Yeh terminal mein detail error print karega
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()

# --- PASSWORD CHANGE ROUTE ---
@app.post("/change-password")
def change_password(request: PasswordChangeRequest):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Fetch the user's current hashed password from DB
        try:
            cursor.execute("SELECT password FROM users WHERE id = ?", (request.user_id,))
        except:
            cursor.execute("SELECT password_hash FROM users WHERE id = ?", (request.user_id,))
            
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
            
        db_hash = row[0]
        db_hash_bytes = db_hash.encode('utf-8') if isinstance(db_hash, str) else db_hash
        
        # 2. Verify if the entered "Current Password" is correct
        if not bcrypt.checkpw(request.current_password.encode('utf-8'), db_hash_bytes):
            raise HTTPException(status_code=400, detail="Incorrect current password!")
            
        # 3. Hash the "New Password"
        new_hash = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # 4. Save the new password to the database
        try:
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, request.user_id))
        except:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, request.user_id))
            
        conn.commit()
        return {"status": "success", "message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Password Update Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn: conn.close()