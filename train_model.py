import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import joblib
import os

# 1. Define File Paths
input_file = 'data/processed_financial_data.csv'
output_labeled_file = 'data/user_profiles_with_clusters.csv'
model_dir = 'models'

# Ensure the models directory exists
if not os.path.exists(model_dir):
    os.makedirs(model_dir)
    print(f"Created directory: {model_dir}")

# 2. Load the processed data
if not os.path.exists(input_file):
    print(f"Error: Input file '{input_file}' not found. Please run preprocessing first.")
else:
    df = pd.read_csv(input_file)
    print("Data loaded successfully.")

    # 3. Prepare Data for Training
    # We must drop 'user_id' because it's just an identifier, not a behavioral feature.
    # The remaining columns are already scaled from the previous step.
    X = df.drop(columns=['user_id'])

    print(f"Training model on {X.shape[0]} users with {X.shape[1]} features...")

    # 4. Apply K-Means Clustering
    # We are choosing 4 clusters based on the Scope Document examples:
    # (Saver, Impulsive Buyer, Minimalist, Risk Taker)
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)

    # Add the cluster labels back to the dataframe
    df['Cluster'] = clusters

    print("K-Means Clustering completed.")

    # 5. Apply PCA (Dimensionality Reduction) for Visualization
    # This reduces our many features down to 2 components (x and y) for plotting on the dashboard.
    pca = PCA(n_components=2)
    pca_components = pca.fit_transform(X)

    # Add PCA coordinates to the dataframe
    df['PCA_x'] = pca_components[:, 0]
    df['PCA_y'] = pca_components[:, 1]

    print("PCA Transformation completed.")

    # 6. Save the Models and Data
    # We save the trained models so the website can use them later without retraining every time.
    joblib.dump(kmeans, os.path.join(model_dir, 'kmeans_model.pkl'))
    joblib.dump(pca, os.path.join(model_dir, 'pca_model.pkl'))
    
    # Save the new dataset with Cluster IDs and PCA coordinates
    df.to_csv(output_labeled_file, index=False)

    print("\n--- Summary ---")
    print(f"1. Trained KMeans model saved to: {os.path.join(model_dir, 'kmeans_model.pkl')}")
    print(f"2. Trained PCA model saved to: {os.path.join(model_dir, 'pca_model.pkl')}")
    print(f"3. Labeled user data saved to: {output_labeled_file}")
    print("Step 3 Complete. Ready for Analysis.")