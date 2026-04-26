import pandas as pd
import joblib
import os
import sys

# --- SMART PATH FINDING ---
# Get the directory where this script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Check two probable locations for models:
# 1. Inside src/models
path_option_1 = os.path.join(current_dir, 'models')
# 2. In the root folder (one level up) -> models/
path_option_2 = os.path.join(os.path.dirname(current_dir), 'models')

MODEL_DIR = None

if os.path.exists(os.path.join(path_option_1, 'kmeans_model.pkl')):
    MODEL_DIR = path_option_1
    print(f"✅ Found models in: {MODEL_DIR}")
elif os.path.exists(os.path.join(path_option_2, 'kmeans_model.pkl')):
    MODEL_DIR = path_option_2
    print(f"✅ Found models in: {MODEL_DIR}")
else:
    print("❌ Error: Could not find 'models' folder with 'kmeans_model.pkl'.")
    print(f"Checked: \n1. {path_option_1}\n2. {path_option_2}")
    sys.exit()

# --- LOAD MODELS ---
try:
    kmeans = joblib.load(os.path.join(MODEL_DIR, 'kmeans_model.pkl'))
    scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler.pkl'))
    print("✅ Models Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading Models: {e}")
    sys.exit()

# --- DEFINE TEST CASES ---
# Typical profiles to test cluster behavior
test_cases = {
    "Smart Saver 🛡️": [100000, 40000, 0.50, 0.0, 10000, 30000, 0, 30, 0.40, 0.33],
    "Big Spender 🛍️": [100000, 95000, 0.05, 0.20, 55000, 40000, 0, 30, 0.95, 1.375],
    "Wealth Builder 🚀": [300000, 100000, 0.50, 0.0, 50000, 50000, 100000, 50, 0.33, 1.0],
    "Budget Challenger 📉": [40000, 45000, -0.125, 1.5, 5000, 40000, 0, 20, 1.125, 0.125]
}

cols = ['monthly_income', 'monthly_expense_total', 'savings_rate', 'debt_to_income_ratio', 'discretionary_spending', 'essential_spending', 'investment_amount', 'transaction_count', 'expense_ratio', 'lifestyle_ratio']

print("\n🔍 CHECKING CLUSTER MAPPING...\n")
print(f"{'Persona Name':<20} | {'Cluster ID'}")
print("-" * 35)

results = {}

for name, values in test_cases.items():
    df = pd.DataFrame([values], columns=cols)
    scaled = scaler.transform(df)
    cluster_id = kmeans.predict(scaled)[0]
    
    print(f"{name:<20} | {cluster_id}")
    
    # Store clean name for dictionary (e.g., "Smart Saver")
    clean_name = " ".join(name.split()[:2]) + " " + name.split()[2]
    results[int(cluster_id)] = clean_name

# --- PRINT THE RESULT DICTIONARY ---
print("\n" + "="*50)
print("✅ COPY PASTE THIS INTO 'src/dashboard.py' (Line ~38)")
print("="*50 + "\n")

print("personas = {")
for cid in sorted(results.keys()):
    print(f"    {cid}: \"{results[cid]}\",")
print("}")
print("\n" + "="*50)