import joblib
import os
import pandas as pd
# Removed 'import streamlit' to make this file backend-compatible
from utils import MODELS_DIR

# Using a global variable to cache models in memory
_MODELS = None

def load_models():
    """Loads models efficiently. Only loads once (Singleton pattern)."""
    global _MODELS
    
    if _MODELS is not None:
        return _MODELS
    
    try:
        k = joblib.load(os.path.join(MODELS_DIR, 'kmeans_model.pkl'))
        s = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        p = joblib.load(os.path.join(MODELS_DIR, 'pca_model.pkl'))
        
        _MODELS = (k, s, p)
        return k, s, p
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None, None

def get_ai_advice(persona, income, savings):
    advice_map = {
        "Smart Saver": [
            "Consider parking excess savings in mutual funds.",
            "Look into high-yield term deposits.",
            "Maintain your 6-month emergency fund."
        ],
        "Wealth Builder": [
            "Diversify your portfolio across stocks and real estate.",
            "Rebalance your assets quarterly.",
            "Maximize tax-saving investment options."
        ],
        "Big Spender": [
            "Strictly follow the 50/30/20 budgeting rule.",
            "Wait 48 hours before making any non-essential purchase.",
            "Track your daily small expenses (latte factor)."
        ],
        "Budget Challenger": [
            "Focus on paying off high-interest debt first.",
            "Start a micro-savings fund (even Rs. 500/month).",
            "Explore freelance options to increase income."
        ]
    }
    # Default advice if persona not found
    return advice_map.get(persona, ["Track your spending daily.", "Try to save at least 10% of income.", "Avoid new debt."])