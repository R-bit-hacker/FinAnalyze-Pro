import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import joblib
import json
import os

def generate_synthetic_data(n_per_class=250):
    np.random.seed(42)
    data = []
    
    # 1. Budget Challenger (High debt/expenses > income)
    for _ in range(n_per_class):
        inc = np.random.uniform(30000, 80000)
        exp = inc * np.random.uniform(1.0, 1.2)
        sav = 0.0
        dbt = np.random.uniform(10000, 100000)
        needs = exp * np.random.uniform(0.7, 0.9)
        wants = exp - needs
        data.append([inc, exp, sav, dbt, wants, needs])
        
    # 2. Smart Saver (20% savings, no/low debt)
    for _ in range(n_per_class):
        inc = np.random.uniform(50000, 150000)
        exp = inc * np.random.uniform(0.6, 0.8)
        sav = inc * np.random.uniform(0.15, 0.25)
        dbt = 0.0
        needs = exp * np.random.uniform(0.6, 0.8)
        wants = exp - needs
        data.append([inc, exp, sav, dbt, wants, needs])
        
    # 3. Big Spender (High income, high wants/lifestyle, low savings)
    for _ in range(n_per_class):
        inc = np.random.uniform(100000, 300000)
        exp = inc * np.random.uniform(0.85, 1.1)
        sav = inc * np.random.uniform(0.01, 0.05)
        dbt = np.random.uniform(inc * 0.5, inc * 1.5)
        wants = exp * np.random.uniform(0.5, 0.7)  # High wants
        needs = exp - wants
        data.append([inc, exp, sav, dbt, wants, needs])
        
    # 4. Wealth Builder (High income, >40% savings, low debt)
    for _ in range(n_per_class):
        inc = np.random.uniform(150000, 500000)
        exp = inc * np.random.uniform(0.3, 0.5)
        sav = inc * np.random.uniform(0.4, 0.6)
        dbt = np.random.uniform(0, inc * 0.05)
        needs = exp * np.random.uniform(0.7, 0.9)
        wants = exp - needs
        data.append([inc, exp, sav, dbt, wants, needs])

    df = pd.DataFrame(data, columns=['inc', 'exp', 'sav', 'dbt', 'wants', 'needs'])
    
    # Calculate derived features matching dashboard.py exactly
    df['savings_rate'] = df['sav'] / df['inc']
    df['debt_to_income_ratio'] = df['dbt'] / df['inc']
    df['unused_1'] = 0
    df['unused_2'] = 0
    df['expense_ratio'] = df['exp'] / df['inc']
    df['lifestyle_ratio'] = df['wants'] / (df['needs'] + 1)
    
    # Ordered features: [inc, exp, savings_rate, debt_to_income_ratio, wants, needs, 0, 0, expense_ratio, lifestyle_ratio]
    features = df[['inc', 'exp', 'savings_rate', 'debt_to_income_ratio', 'wants', 'needs', 'unused_1', 'unused_2', 'expense_ratio', 'lifestyle_ratio']]
    return features

def train_and_export():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    print("Training StandardScaler...")
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)
    
    print("Training KMeans (k=4)...")
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(scaled_data)
    
    print("Training PCA (fallback)...")
    pca = PCA(n_components=2)
    pca.fit(scaled_data)
    
    # Dynamic Mapping of Centers
    centers = scaler.inverse_transform(kmeans.cluster_centers_)
    centers_df = pd.DataFrame(centers, columns=df.columns)
    
    # Determine indices
    bc_idx = centers_df['debt_to_income_ratio'].idxmax()
    wb_idx = centers_df['savings_rate'].idxmax()
    
    remaining = [i for i in range(4) if i not in (bc_idx, wb_idx)]
    
    if centers_df.loc[remaining[0], 'lifestyle_ratio'] > centers_df.loc[remaining[1], 'lifestyle_ratio']:
        bs_idx = remaining[0]
        ss_idx = remaining[1]
    else:
        bs_idx = remaining[1]
        ss_idx = remaining[0]
        
    cluster_mapping = {
        str(bc_idx): "Budget Challenger",
        str(wb_idx): "Wealth Builder",
        str(bs_idx): "Big Spender",
        str(ss_idx): "Smart Saver"
    }
    
    print("\n--- Dynamically Mapped Clusters ---")
    for k, v in cluster_mapping.items():
        k_int = int(k)
        print(f"Cluster {k} [{v}]:")
        print(f"  Debt/Income:  {centers_df.loc[k_int, 'debt_to_income_ratio']:.2f}")
        print(f"  Savings Rate: {centers_df.loc[k_int, 'savings_rate']:.2f}")
        print(f"  Lifestyle:    {centers_df.loc[k_int, 'lifestyle_ratio']:.2f}")
        print(f"  Exp Ratio:    {centers_df.loc[k_int, 'expense_ratio']:.2f}")
    
    models_dir = os.path.join(os.getcwd(), 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(kmeans, os.path.join(models_dir, 'kmeans_model.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(pca, os.path.join(models_dir, 'pca_model.pkl'))
    
    with open(os.path.join(models_dir, 'cluster_mapping.json'), 'w') as f:
        json.dump(cluster_mapping, f)
        
    print(f"\n[SUCCESS] Models and cluster_mapping.json successfully saved to {models_dir}")

if __name__ == "__main__":
    train_and_export()