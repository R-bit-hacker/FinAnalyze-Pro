import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

# 1. Define Paths
dataset_path = 'data/personal_finance_tracker_dataset.csv'
output_path = 'data/processed_financial_data.csv'
models_dir = 'models'

# Check/Create Models Directory
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(dataset_path):
    print(f"Error: File '{dataset_path}' not found.")
else:
    # 2. Load Data
    df = pd.read_csv(dataset_path)
    print("Data loaded successfully.")

    # --- CRITICAL FIX: Convert USD to PKR ---
    currency_cols = ['monthly_income', 'monthly_expense_total', 'budget_goal', 
                     'loan_payment', 'investment_amount', 'emergency_fund', 
                     'discretionary_spending', 'essential_spending', 'rent_or_mortgage']
    
    for col in currency_cols:
        if col in df.columns:
            df[col] = df[col] * 60
    
    print("Step 1: Currency converted to PKR (Simulated).")

    # 3. Select Features
    features = [
        'monthly_income', 
        'monthly_expense_total', 
        'savings_rate', 
        'debt_to_income_ratio', 
        'discretionary_spending', 
        'essential_spending',
        'investment_amount',
        'transaction_count'
    ]

    # 4. Aggregate Data (Group by User)
    user_profile = df.groupby('user_id')[features].mean().reset_index()

    # 5. Feature Engineering (Ratios)
    user_profile['expense_ratio'] = user_profile['monthly_expense_total'] / user_profile['monthly_income']
    user_profile['lifestyle_ratio'] = user_profile['discretionary_spending'] / (user_profile['essential_spending'] + 1)

    # 6. Scaling & Saving Scaler
    scaler = StandardScaler()
    cols_to_scale = features + ['expense_ratio', 'lifestyle_ratio']
    
    user_profile_scaled = user_profile.copy()
    user_profile_scaled[cols_to_scale] = scaler.fit_transform(user_profile[cols_to_scale])

    # Save the Scaler (Ye line pehle missing thi)
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    print(f"Step 2: Scaler model saved to {scaler_path}")

    # 7. Save Processed Data
    user_profile_scaled.to_csv(output_path, index=False)
    print(f"Success! Processed PKR data saved to: {output_path}")