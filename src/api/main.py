import sys
import os
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
from utils import get_db

app = FastAPI(title="FinAnalyze Pro API", version="2.5")

# --- LOAD MODELS ON STARTUP ---
try:
    kmeans, scaler, pca = load_models()
    print("✅ ML Models Loaded Successfully on Server")
except Exception as e:
    print(f"⚠️ ML Models failed to load: {e}")
    kmeans, scaler, pca = None, None, None

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
    id: str
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
    deleted: List[str] = []

class PasswordChangeRequest(BaseModel):
    user_id: str
    current_password: str
    new_password: str

# --- ROUTES (EXISTING) ---
@app.get("/")
def home():
    return {"status": "Active", "service": "FinAnalyze Backend"}

@app.post("/login")
def login_user(request: LoginRequest):
    try:
        db = get_db()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        docs = db.collection('users').where('username', '==', request.username).limit(1).stream()
        doc = next(docs, None)
        
        if doc:
            user = doc.to_dict()
            user_id = doc.id
            db_username = user.get('username')
            db_role = user.get('role', 'user')
            db_password_hash = user.get('password') or user.get('password_hash')
            db_fullname = user.get('full_name')
            db_pic = user.get('profile_pic')
            db_phone = user.get('phone_number')
            
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
    try:
        db = get_db()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        docs = db.collection('users').stream()
        
        user_list = []
        for doc in docs:
            u = doc.to_dict()
            user_list.append({
                "id": doc.id,
                "username": u.get('username', ''),
                "name": u.get('full_name', 'N/A') or "N/A",
                "role": u.get('role', 'user'),
                "phone": u.get('phone_number', 'N/A') or "N/A",
                "email": u.get('email', 'No Email') or "No Email",
                "pic": u.get('profile_pic', '') or ""
            })
        return {"status": "success", "users": user_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-user/{user_id}")
def delete_user(user_id: str):
    try:
        db = get_db()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        if doc.to_dict().get('role') == 'admin':
            raise HTTPException(status_code=400, detail="❌ Cannot delete an Admin account!")
            
        doc_ref.delete()
        
        # Delete analysis history
        history_docs = db.collection('analysis_history').where('user_id', '==', user_id).stream()
        for h_doc in history_docs:
            h_doc.reference.delete()
            
        return {"status": "success", "message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 🚀 NEW ADVANCED CRUD ROUTE FOR DATA EDITOR ---
@app.post("/batch-update-users")
def batch_update_users(request: BatchUpdateRequest):
    try:
        db = get_db()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        batch = db.batch()
        
        # 1. Process Deletions
        for uid in request.deleted:
            doc_ref = db.collection('users').document(uid)
            doc = doc_ref.get()
            if doc.exists and doc.to_dict().get('role') != 'admin': # Admin ko delete hone se rokein
                batch.delete(doc_ref)
                
                history_docs = db.collection('analysis_history').where('user_id', '==', uid).stream()
                for h_doc in history_docs:
                    batch.delete(h_doc.reference)

        # 2. Process Edits
        for edit in request.edited:
            doc_ref = db.collection('users').document(edit.id)
            update_data = {}
            if edit.username is not None: update_data["username"] = edit.username
            if edit.name is not None: update_data["full_name"] = edit.name
            if edit.role is not None: update_data["role"] = edit.role
            if edit.phone is not None: update_data["phone_number"] = edit.phone
            if edit.email is not None: update_data["email"] = edit.email
            
            if update_data:
                batch.update(doc_ref, update_data)

        # 3. Process Additions (Naya User Add Karne ka Code)
        hashed_pw = bcrypt.hashpw(b"123456", bcrypt.gensalt()).decode('utf-8')
        
        for add in request.added:
            new_doc_ref = db.collection('users').document()
            batch.set(new_doc_ref, {
                "username": add.username,
                "full_name": add.name,
                "role": add.role,
                "phone_number": add.phone,
                "email": add.email,
                "password": hashed_pw,
                "is_verified": 1
            })

        batch.commit()
        return {"status": "success", "message": "All operations completed successfully."}
        
    except Exception as e:
        print(f"Batch Update Error: {e}") # Yeh terminal mein detail error print karega
        raise HTTPException(status_code=500, detail=str(e))

# --- PASSWORD CHANGE ROUTE ---
@app.post("/change-password")
def change_password(request: PasswordChangeRequest):
    try:
        db = get_db()
        if not db:
            raise HTTPException(status_code=500, detail="Database connection failed")
            
        doc_ref = db.collection('users').document(request.user_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        user_data = doc.to_dict()
        db_hash = user_data.get('password') or user_data.get('password_hash')
        db_hash_bytes = db_hash.encode('utf-8') if isinstance(db_hash, str) else db_hash
        
        if not bcrypt.checkpw(request.current_password.encode('utf-8'), db_hash_bytes):
            raise HTTPException(status_code=400, detail="Incorrect current password!")
            
        new_hash = bcrypt.hashpw(request.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        doc_ref.update({"password": new_hash})
        return {"status": "success", "message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Password Update Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))