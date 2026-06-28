import sys

# Update utils.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'r', encoding='utf-8') as f:
    utils_content = f.read()

utils_target = '''    with c3:
        st.markdown("**Legal**")
        if st.button("Privacy Policy", key="footer_btn_privacy", use_container_width=True):
            st.session_state['page'] = 'privacy'
            st.rerun()
        if st.button("Terms of Service", key="footer_btn_terms", use_container_width=True):
            st.session_state['page'] = 'terms'
            st.rerun()
        if st.button("Cookie Policy", key="footer_btn_cookie", use_container_width=True):
            st.session_state['page'] = 'cookie'
            st.rerun()'''

utils_replace = '''    with c3:
        st.markdown("<h4 style='color: #fff; margin-bottom: 20px; font-size: 1.1rem;'>Legal</h4>", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="footer-link">', unsafe_allow_html=True)
            if st.button("Privacy Policy", key="footer_btn_privacy"):
                st.session_state['page'] = 'privacy'
                st.rerun()
            if st.button("Terms of Service", key="footer_btn_terms"):
                st.session_state['page'] = 'terms'
                st.rerun()
            if st.button("Cookie Policy", key="footer_btn_cookie"):
                st.session_state['page'] = 'cookie'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)'''

if utils_target in utils_content:
    utils_content = utils_content.replace(utils_target, utils_replace)
    with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'w', encoding='utf-8') as f:
        f.write(utils_content)
    print("utils.py updated")
else:
    print("Failed to find target in utils.py")


# Update app.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

app_target = '''def render_privacy_policy():
    if st.button("⬅️ Return to App", key="back_from_privacy"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Privacy Policy")
    st.markdown("Welcome to **FinAnalyze**. Your privacy is our top priority. We do not store your raw bank statements or account numbers. We use secure session states and API endpoints (like Groq) strictly for generating your financial personality profile. Data is wiped after your session ends.")

def render_terms():
    if st.button("⬅️ Return to App", key="back_from_terms"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Terms of Service")
    st.markdown("By using **FinAnalyze**, you agree that this tool is for educational and profiling purposes only and does not constitute professional financial advice. All K-Means clustering insights are automated estimations.")

def render_cookie():
    if st.button("⬅️ Return to App", key="back_from_cookie"):
        st.session_state['page'] = 'landing' if st.session_state.get('user') is None else 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Cookie Policy")
    st.markdown("We strictly use session-based states (similar to essential cookies) to maintain your active session, keep your Galixo dark theme preferences active, and ensure smooth navigation. No tracking cookies are deployed.")'''

app_replace = '''def render_privacy_policy():
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

if app_target in app_content:
    app_content = app_content.replace(app_target, app_replace)
    with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("app.py updated")
else:
    print("Failed to find target in app.py")
