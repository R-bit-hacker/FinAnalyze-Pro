import pandas as pd
import os

# 1. Define File Paths
cluster_file_path = 'data/user_profiles_with_clusters.csv'
original_data_path = 'data/personal_finance_tracker_dataset.csv'

# Check if files exist
if not os.path.exists(cluster_file_path) or not os.path.exists(original_data_path):
    print("Error: Required files not found. Make sure Step 1 and Step 3 are completed.")
else:
    # 2. Load Data
    cluster_df = pd.read_csv(cluster_file_path)
    raw_df = pd.read_csv(original_data_path)

    # 3. Prepare the Data for Analysis
    # We take only 'user_id' and 'Cluster' from the trained model file
    user_clusters = cluster_df[['user_id', 'Cluster']]

    # We aggregate the RAW data (real dollar values) by user_id
    # FIX: Added numeric_only=True to ignore Date and Text columns causing the error
    raw_profiles = raw_df.groupby('user_id').mean(numeric_only=True).reset_index()

    # 4. Merge Clusters with Raw Data
    # Now we have Real Numbers + Cluster IDs in one table
    merged_df = pd.merge(raw_profiles, user_clusters, on='user_id')

    # 5. Group by Cluster to see the Average Behavior of each group
    # We select key columns that help define personality
    analysis_columns = [
        'monthly_income', 
        'monthly_expense_total', 
        'savings_rate', 
        'discretionary_spending', 
        'essential_spending',
        'debt_to_income_ratio',
        'investment_amount'
    ]
    
    # Calculate mean for each cluster
    cluster_summary = merged_df.groupby('Cluster')[analysis_columns].mean().round(2)

    # 6. Add a "Count" column to see how many users are in each cluster
    cluster_counts = merged_df['Cluster'].value_counts().sort_index()
    cluster_summary['User_Count'] = cluster_counts

    # 7. Print the Report
    print("\n--- CLUSTER ANALYSIS REPORT (Real Values) ---")
    print(cluster_summary.to_string())
    print("\n---------------------------------------------")
    
    # Save this summary to a CSV for reference
    cluster_summary.to_csv('data/cluster_summary_report.csv')
    print("Summary saved to 'data/cluster_summary_report.csv'")