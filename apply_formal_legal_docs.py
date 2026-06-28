import sys

# Update app.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

app_target = '''def render_privacy_policy():
    if st.button("⬅️ Return to App", key="back_from_privacy"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🛡️ Privacy Policy")
    st.markdown(\'\'\'**Last Updated: June 2026**\\n\\nWelcome to **FinAnalyze**. We believe that financial data privacy is a fundamental human right. This document outlines how we securely process your data to generate AI-driven financial personas.\\n\\n### 1. Data Collection & Zero-Storage Policy\\nFinAnalyze operates on an ephemeral data processing model. When you upload your financial statements (PDF/CSV) or enter data manually:\\n* **No Raw Storage:** We **do not** save your bank account numbers, routing details, or raw transaction logs to any database.\\n* **In-Memory Processing:** Data is parsed strictly in-memory during your active session to run our K-Means Clustering algorithm. Once the session terminates, the raw files are permanently destroyed.\\n\\n### 2. AI Model & API Usage\\nTo generate advanced insights, we utilize state-of-the-art LLMs (via secure Groq API endpoints). We ensure that only anonymized, aggregated numerical parameters (e.g., total income, spending ratios) are sent for text generation. **No Personally Identifiable Information (PII) is ever shared with third-party AI models.**\\n\\n### 3. Account Security\\nYour user credentials (Email and Password) are secured using industry-standard cryptographic hashing algorithms (Bcrypt). Our development team cannot view or reverse-engineer your password.\\n\\n### 4. Your Rights\\nYou have the absolute right to request the deletion of your account and your historical analysis logs. You can initiate this request via our Contact Support page.\'\'\')

def render_terms():
    if st.button("⬅️ Return to App", key="back_from_terms"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("⚖️ Terms of Service")
    st.markdown(\'\'\'**Effective Date: June 2026**\\n\\nBy accessing and utilizing the **FinAnalyze** platform, you agree to comply with the following Terms of Service.\\n\\n### 1. Educational and Analytical Purposes Only\\nFinAnalyze is an AI-powered financial profiling and predictive analytics tool. The insights provided by our K-Means clustering engine, Future Projections, and Robo-Advisor are for **educational and informational purposes only**.\\n* **Not Financial Advice:** We are not certified financial planners, brokers, or tax advisors. The platform's outputs should not be interpreted as professional financial or investment advice.\\n\\n### 2. User Responsibilities\\nYou are responsible for the accuracy of the financial parameters you input. Do not upload documents containing unredacted, highly sensitive credentials (such as full credit card numbers) during this prototype phase.\\n\\n### 3. Forecasting Limitations\\nThe "Future Projections" and "Stress Tester" modules use mathematical models to simulate compounding wealth and inflation. However, real-world financial markets are highly volatile. FinAnalyze holds no liability for financial losses incurred based on these automated projections.\\n\\n### 4. Acceptable Use\\nYou agree not to reverse-engineer our Machine Learning architecture, spam our contact endpoints, or attempt unauthorized access to our Firebase backend.\'\'\')

def render_cookie():
    if st.button("⬅️ Return to App", key="back_from_cookie"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("🍪 Cookie & Session Policy")
    st.markdown(\'\'\'**Transparency in Tracking**\\n\\nFinAnalyze takes a minimalist and privacy-first approach to browser storage.\\n\\n### 1. What We Use (Session State)\\nInstead of intrusive tracking cookies, FinAnalyze utilizes Python-based **Streamlit Session States**. These act as strictly necessary, temporary cookies that exist only while your browser tab is open. We use them to:\\n* Keep you securely logged in as you navigate between the Dashboard, New Analysis, and Robo-Advisor.\\n* Remember your interface preferences (e.g., Galixo dark theme persistence).\\n* Retain your analytical inputs so you don't lose progress if you switch tabs.\\n\\n### 2. What We DO NOT Use\\n* **No Marketing Pixels:** We do not use Meta Pixel, Google Analytics tracking scripts, or cross-site tracking cookies.\\n* **No Ad Retargeting:** Your financial persona is yours alone. We do not sell your behavioral data to ad agencies.\\n\\nBy using the app, you consent to the use of these essential session states required for the core functionality of the FinAnalyze dashboard.\'\'\')'''

app_replace = '''def render_privacy_policy():
    if st.button("Return to Application", key="back_from_privacy"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Privacy Policy")
    st.markdown(\'\'\'**Effective Date: June 2026**\\n\\n**1. Data Collection and Zero-Storage Architecture**\\nFinAnalyze employs an ephemeral data processing model. Financial statements (PDF/CSV) uploaded to the platform are parsed in-memory strictly for real-time analysis. We do not persistently store raw transaction logs, bank account numbers, or routing details on our servers. Upon session termination, all uploaded artifacts are immediately purged.\\n\\n**2. Artificial Intelligence and Third-Party APIs**\\nTo facilitate advanced financial profiling, we utilize secure external APIs. Only anonymized, aggregated numerical parameters are transmitted for processing. No Personally Identifiable Information (PII) is utilized for training third-party machine learning models.\\n\\n**3. Cryptographic Security**\\nUser authentication is secured via industry-standard hashing protocols (Bcrypt). Platform administrators do not have access to plaintext user passwords.\\n\\n**4. Data Retention and User Rights**\\nUsers retain full control over their historical analysis logs and may request complete account deletion via our Support channels at any time.\'\'\')

def render_terms():
    if st.button("Return to Application", key="back_from_terms"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Terms of Service")
    st.markdown(\'\'\'**Effective Date: June 2026**\\n\\n**1. Acceptance of Terms**\\nBy accessing the FinAnalyze platform, you agree to be bound by these Terms of Service. This platform is designed strictly for educational and analytical modeling.\\n\\n**2. Nature of Service and Limitations**\\nFinAnalyze utilizes K-Means clustering and predictive algorithms to simulate financial trajectories. These outputs are automated estimations and do not constitute certified financial, tax, or investment advice. Users should consult registered financial advisors before making critical financial decisions.\\n\\n**3. User Obligations**\\nUsers are required to ensure that uploaded documents are appropriately redacted. Do not upload documents containing highly sensitive, unredacted credentials during this prototype phase. You are responsible for maintaining the confidentiality of your authentication credentials.\\n\\n**4. Limitation of Liability**\\nWhile we strive for high analytical accuracy, financial markets are subject to volatility. FinAnalyze and its developers hold no liability for financial losses or discrepancies arising from reliance on the platform's automated projections.\'\'\')

def render_cookie():
    if st.button("Return to Application", key="back_from_cookie"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Cookie and Session Policy")
    st.markdown(\'\'\'**1. Session State Management**\\nFinAnalyze does not utilize traditional tracking cookies. Instead, we rely on native framework session states to maintain secure authentication and seamless navigation across the dashboard modules.\\n\\n**2. Essential Functionality**\\nThese session states are strictly necessary. They preserve user interface preferences (such as theme selection) and temporarily retain analytical inputs to prevent data loss during module transitions.\\n\\n**3. Exclusivity of Tracking**\\nWe do not deploy marketing pixels, third-party analytics trackers, or cross-site tracking mechanisms. User session data is confined entirely to the active application lifecycle and is not monetized or shared with external advertising entities.\'\'\')'''

if app_target in app_content:
    app_content = app_content.replace(app_target, app_replace)
    with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("app.py updated successfully")
else:
    print("Failed to find target in app.py")
