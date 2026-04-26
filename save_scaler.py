import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

# 1. Load Raw Data
df = pd.read_csv('data/personal_finance_tracker_dataset.csv')

# --- CRITICAL FIX: Convert USD to PKR ---
# Must match the preprocessing logic exactly!
currency_cols = ['monthly_income', 'monthly_expense_total', 'budget_goal', 
                 'loan_payment', 'investment_amount', 'emergency_fund', 
                 'discretionary_spending', 'essential_spending', 'rent_or_mortgage']

for col in currency_cols:
    if col in df.columns:
        df[col] = df[col] * 60

print("Currency converted to PKR for Scaler.")

# 2. Feature Engineering
features = ['monthly_income', 'monthly_expense_total', 'savings_rate', 
            'debt_to_income_ratio', 'discretionary_spending', 'essential_spending',
            'investment_amount', 'transaction_count']

# Group by User
user_profile = df.groupby('user_id')[features].mean().reset_index()

# Add Ratios
user_profile['expense_ratio'] = user_profile['monthly_expense_total'] / user_profile['monthly_income']
user_profile['lifestyle_ratio'] = user_profile['discretionary_spending'] / (user_profile['essential_spending'] + 1)

# 3. Fit and Save Scaler
cols_to_scale = features + ['expense_ratio', 'lifestyle_ratio']
scaler = StandardScaler()
scaler.fit(user_profile[cols_to_scale])

if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(scaler, 'models/scaler.pkl')
print("Success! PKR-Calibrated Scaler saved to models/scaler.pkl")