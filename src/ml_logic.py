import joblib
import os
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

# Removed 'import streamlit' to make this file backend-compatible
from utils import MODELS_DIR

load_dotenv()

# Using a global variable to cache models in memory
_MODELS = None

def load_models():
    """Loads models efficiently. Only loads once (Singleton pattern)."""
    global _MODELS
    
    if _MODELS is not None:
        return _MODELS
    
    try:
        import json
        k = joblib.load(os.path.join(MODELS_DIR, 'kmeans_model.pkl'))
        s = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
        p = joblib.load(os.path.join(MODELS_DIR, 'pca_model.pkl'))
        
        with open(os.path.join(MODELS_DIR, 'cluster_mapping.json'), 'r') as f:
            mapping = json.load(f)
        
        _MODELS = (k, s, p, mapping)
        return k, s, p, mapping
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        return None, None, None, None

def get_ai_advice(persona, income, savings):
    api_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=api_key)
    
    prompt = f"""You are an expert financial advisor for the FinAnalyze app.
A user has been classified as the '{persona}' persona.
Their monthly income is PKR {income:,.0f} and total savings are PKR {savings:,.0f}.
Provide exactly 3 short, highly personalized financial recommendations based on this data.

Format your response exactly as the following HTML structure without any markdown backticks (do NOT wrap in ```html). Do NOT include any intro or outro text, ONLY the HTML.

<div style="background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(119, 93, 208, 0.3); border-radius: 15px; padding: 18px 25px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
    <div style="color: #e0e0e0; font-size: 0.95rem; font-weight: 300; letter-spacing: 0.3px;">
        [Recommendation 1]
    </div>
</div>
<div style="background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(119, 93, 208, 0.3); border-radius: 15px; padding: 18px 25px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
    <div style="color: #e0e0e0; font-size: 0.95rem; font-weight: 300; letter-spacing: 0.3px;">
        [Recommendation 2]
    </div>
</div>
<div style="background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(119, 93, 208, 0.3); border-radius: 15px; padding: 18px 25px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
    <div style="color: #e0e0e0; font-size: 0.95rem; font-weight: 300; letter-spacing: 0.3px;">
        [Recommendation 3]
    </div>
</div>"""

    resp = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}], 
        model="llama-3.3-70b-versatile"
    )
    reply = resp.choices[0].message.content
    return reply.replace("```html", "").replace("```", "").strip()

    # --- ADD THIS AT THE END OF ml_logic.py ---

def calculate_finscore(income, expense, savings, debt):
    """
    Proprietary Algorithm to calculate Financial Health Score (300 to 850)
    """
    # Base score
    score = 300
    
    # 1. Savings Reward (Up to +350 points)
    if income > 0:
        savings_ratio = savings / income
        # Max reward if saving 30% or more
        reward = min(350, int((savings_ratio / 0.3) * 350))
        score += reward
        
    # 2. Expense Discipline (Up to +200 points)
    if income > 0:
        expense_ratio = expense / income
        if expense_ratio <= 0.5:
            score += 200 # Excellent
        elif expense_ratio <= 0.7:
            score += 100 # Good
        elif expense_ratio <= 0.9:
            score += 50  # Average
            
    # 3. Debt Penalty (Deduction up to -150 points)
    if income > 0 and debt > 0:
        debt_ratio = debt / income
        penalty = min(150, int(debt_ratio * 150))
        score -= penalty
        
    # Cap the score between 300 (Lowest) and 850 (Excellent)
    final_score = max(300, min(850, int(score)))
    
    # Determine Status
    if final_score >= 750: status = "Excellent"
    elif final_score >= 650: status = "Good"
    elif final_score >= 500: status = "Average"
    else: status = "Poor"
    
    return final_score, status

    # --- NEW FEATURE: ROBO-ADVISOR OPTIMIZATION ENGINE ---
def robo_advisor_plan(target_amount, months, current_savings, monthly_income, monthly_expense):
    """
    Mathematical algorithm to calculate feasibility of a financial goal.
    """
    remaining_amount = max(0, target_amount - current_savings)
    if remaining_amount == 0:
        return 0, "Target Already Achieved! 🎉", "#00E396" # Green
        
    if months <= 0:
        return 0, "Invalid timeline.", "#FF4560" # Red
        
    required_monthly = remaining_amount / months
    disposable_income = monthly_income - monthly_expense
    
    # Logic / Guardrails
    if disposable_income <= 0:
        advice = "⚠️ Critical: Your expenses exceed your income. You cannot save for this goal right now."
        color = "#FF4560" # Red
    elif required_monthly > disposable_income:
        shortfall = required_monthly - disposable_income
        advice = f"🚨 Unrealistic Goal: You are short by PKR {shortfall:,.0f} every month. Try extending the timeline or cutting expenses."
        color = "#FF4560" # Red
    elif required_monthly > (disposable_income * 0.7):
        advice = "🟡 Aggressive Goal: Possible, but it requires investing 70%+ of your remaining income. Strict budgeting needed."
        color = "#FEB019" # Orange/Warning
    else:
        advice = "✅ Achievable Goal: You are well on track! You can comfortably save this amount."
        color = "#00E396" # Green
        
    return required_monthly, advice, color

def get_future_growth_verdict(current_sav, monthly_sav, y1, y5, y10, rate=0.12):
    api_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=api_key)
    
    prompt = f"""You are an expert financial forecaster for the FinAnalyze app.
A user has the following projected trajectory assuming a {rate*100}% annual return:
- Current Savings: PKR {current_sav:,}
- Monthly Contribution: PKR {monthly_sav:,}
- Year 1 Projected: PKR {y1:,.0f}
- Year 5 Projected: PKR {y5:,.0f}
- Year 10 Projected: PKR {y10:,.0f}

Please provide a highly concise, ONE-PARAGRAPH 'Growth Verdict'. 
Highlight any major milestones they will hit (e.g., reaching their first million). Be encouraging but realistic. 
Format your response using basic HTML tags (like <b>) instead of Markdown backticks so it renders cleanly. Do not wrap the whole response in a code block.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        max_completion_tokens=250,
    )
    
    return response.choices[0].message.content

def parse_bank_statement_with_llm(raw_text):
    import json
    api_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=api_key)
    
    prompt = f"""You are a highly advanced financial data extraction AI. Extract all outgoing expenses/debits from this raw bank statement text. Ignore incoming money/credits.

Categorize the expenses into two totals: Essentials (e.g., bills, rent, groceries, pharmacy) and Lifestyle (e.g., dining, netflix, shopping).

Return ONLY a valid JSON object in this exact format, with no markdown or extra text: {{"essentials": 15000.0, "lifestyle": 5000.0}}

RAW TEXT:
{raw_text}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_completion_tokens=150,
        )
        content = response.choices[0].message.content.strip()
        # Remove any stray markdown if the model hallucinates it despite instructions
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        
        parsed = json.loads(content.strip())
        return parsed.get("essentials", 0.0), parsed.get("lifestyle", 0.0)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF with AI: {e}")