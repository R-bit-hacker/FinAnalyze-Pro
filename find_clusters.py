import pandas as pd
import joblib
import numpy as np

# 1. Load Model and Scaler
kmeans = joblib.load('models/kmeans_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# 2. Define 4 Typical Personas (PKR Values) to test the Model
test_cases = {
    "Wealth Builder 🚀": [300000, 100000, 0.50, 0.0, 50000, 50000, 100000, 80, 0.33, 1.0],
    "Budget Challenger 📉": [30000, 35000, -0.10, 0.60, 5000, 30000, 0, 20, 1.16, 0.16],
    "Big Spender 🛍️": [150000, 140000, 0.05, 0.10, 100000, 40000, 0, 90, 0.93, 2.5],
    "Smart Saver 🛡️": [80000, 50000, 0.35, 0.0, 10000, 40000, 20000, 40, 0.62, 0.25]
}

print("\n--- CORRECT CLUSTER MAPPING ---")
print("Copy these IDs into your app.py file:\n")

for name, data in test_cases.items():
    # Convert list to DataFrame with correct column names
    cols = ['monthly_income', 'monthly_expense_total', 'savings_rate', 
            'debt_to_income_ratio', 'discretionary_spending', 'essential_spending',
            'investment_amount', 'transaction_count', 'expense_ratio', 'lifestyle_ratio']
    
    df_test = pd.DataFrame([data], columns=cols)
    
    # Scale and Predict
    scaled_data = scaler.transform(df_test)
    cluster_id = kmeans.predict(scaled_data)[0]
    
    print(f"Cluster {cluster_id} = {name}")

print("\n-------------------------------")