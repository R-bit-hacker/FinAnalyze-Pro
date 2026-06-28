import sys
import re

# 1. Update utils.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'r', encoding='utf-8') as f:
    utils_content = f.read()

# Remove the active legal view renderer from utils.py
utils_content = re.sub(r'    # --- ACTIVE LEGAL VIEW RENDERER ---.*?    # --- FOOTER STYLES ---', '    # --- FOOTER STYLES ---', utils_content, flags=re.DOTALL)

# Update the buttons to set app_mode
utils_content = re.sub(
    r"st\.session_state\['active_legal_view'\] = 'Privacy Policy'",
    r"st.session_state['app_mode'] = 'privacy'",
    utils_content
)
utils_content = re.sub(
    r"st\.session_state\['active_legal_view'\] = 'Terms of Service'",
    r"st.session_state['app_mode'] = 'terms'",
    utils_content
)
utils_content = re.sub(
    r"st\.session_state\['active_legal_view'\] = 'Cookie Policy'",
    r"st.session_state['app_mode'] = 'cookie'",
    utils_content
)

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'w', encoding='utf-8') as f:
    f.write(utils_content)


# 2. Update dashboard.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'r', encoding='utf-8') as f:
    dash_content = f.read()

legal_funcs = """
def render_privacy_policy():
    if st.button("⬅️ Return to App", key="back_priv"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown('''
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 class="gradient-text" style="font-size: 3rem; margin-top: 20px;">Privacy Policy</h1>
        <p style="color: #888; font-size: 1.1rem;">Your data security is our top priority. Last Updated: January 2026</p>
    </div>
    <div style="padding: 20px; border-left: 4px solid #00f260; background: rgba(0,242,96,0.05); margin-bottom: 30px;">
        <h3 style="display:flex; align-items:center; gap:10px; margin:0; color: white;">The Short Version</h3>
        <p style="color: #ccc; line-height: 1.7; font-size: 1.05rem; margin-top: 10px; margin-bottom:0;">
            We strictly process financial data (income, expenses, savings) to power our AI model analysis. 
            Uploaded financial statements are parsed ephemerally and never permanently stored. Your passwords are cryptographically hashed (bcrypt), and we <b>never</b> sell your data to third parties.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown('''
        <div class="glass-card">
            <h3 style="color: white;">1. Data We Collect</h3>
            <ul style="color: #aaa; line-height: 1.8; margin-top: 15px;">
                <li><b>Account Info:</b> Name, Email (for secure login).</li>
                <li><b>Financial Statements:</b> PDF bank statements uploaded are temporarily processed in-memory.</li>
                <li><b>Financial Inputs:</b> Transactional metrics extracted solely for accurate profiling.</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown('''
        <div class="glass-card">
            <h3 style="color: white;">2. How We Use It</h3>
            <ul style="color: #aaa; line-height: 1.8; margin-top: 15px;">
                <li>To run the automated K-Means Clustering algorithm.</li>
                <li>To generate unbiased, data-driven financial personas.</li>
                <li>To provide personalized 10-year wealth compounding advice.</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>Common Questions</h2><br>", unsafe_allow_html=True)
    with st.expander("Is my financial data connected to my real bank account?"):
        st.write("No. FinAnalyze operates purely on manually entered data and standalone PDF statement uploads. We intentionally do not use Plaid or any direct API connections to your actual bank accounts for maximum security.")
    with st.expander("How secure is my password?"):
        st.write("Very secure. We use industry-standard bcrypt hashing. Even our database administrators cannot see your actual password.")
    with st.expander("Can I delete my data?"):
        st.write("Yes. Send a request through the Contact page, and our system will permanently wipe your analytical history and user record from our secure servers.")

def render_terms():
    if st.button("⬅️ Return to App", key="back_terms"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown('''
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 class="gradient-text" style="font-size: 3rem; margin-top: 20px;">Terms of Service</h1>
        <p style="color: #888; font-size: 1.1rem;">Governing the use of the FinAnalyze Platform</p>
    </div>
    <div class="glass-card">
        <h3 style="color: white;">1. Platform Utilization & AI Insights</h3>
        <p style="color:#aaa; line-height: 1.6;">FinAnalyze utilizes an automated K-Means clustering engine to evaluate financial behavior. The AI-generated insights, including your financial persona and 10-year wealth projections, are provided strictly for educational and analytical purposes. They do not constitute certified financial, legal, or investment advice.</p>
        <br>
        <h3 style="color: white;">2. Data Processing & Credentials</h3>
        <p style="color:#aaa; line-height: 1.6;">Our system processes transactional data to fuel its AI models. However, FinAnalyze maintains a strict policy of non-storage regarding actual bank credentials. Your uploaded financial statements are parsed ephemerally; we extract numerical heuristics via our LLM pipeline and immediately discard the source document to ensure maximum operational security.</p>
        <br>
        <h3 style="color: white;">3. User Responsibilities</h3>
        <p style="color:#aaa; line-height: 1.6;">By leveraging our platform, you agree to provide redacted or dummy statements as advised during this prototype phase. You are responsible for maintaining the confidentiality of your account password, while we maintain industry-standard encryption for your analytical results.</p>
        <br>
        <h3 style="color: white;">4. Service Limitations & Liability</h3>
        <p style="color:#aaa; line-height: 1.6;">FinAnalyze is provided on an "as-is" basis. We do not guarantee the absolute predictive accuracy of the 10-year Wealth Forecaster or the Stress Tester modules, as market conditions and inflation are inherently volatile. We reserve the right to suspend accounts that attempt to reverse-engineer or abuse the platform's API endpoints.</p>
    </div>
    ''', unsafe_allow_html=True)

def render_cookie():
    if st.button("⬅️ Return to App", key="back_cookie"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown('''
    <div style="text-align: center; margin-bottom: 50px;">
        <h1 class="gradient-text" style="font-size: 3rem; margin-top: 20px;">Cookie Policy</h1>
        <p style="color: #888; font-size: 1.1rem;">Transparent tracking and session management.</p>
    </div>
    <div class="glass-card" style="margin-bottom: 20px;">
        <h3 style="color: white; margin-top:0;">What are Cookies?</h3>
        <p style="color:#aaa; margin-top: 10px;">Cookies are microscopic data packets stored on your device that enable our application to maintain seamless session states. They ensure you don't lose your progress during deep financial analysis across multiple dashboard modules.</p>
    </div>
    <div class="glass-card">
        <h3 style="color: white;">How FinAnalyze Leverages Cookies</h3>
        <ul style="color:#aaa; line-height:1.8;">
            <li><b>Session & Authentication:</b> We deploy strictly necessary cookies to authenticate your user profile and securely bridge the gap between your client-side dashboard and our AI processing endpoints. Without these, the login functionality would fail.</li>
            <li><b>UI State Persistence:</b> We utilize session-based cookies to remember interface preferences, such as maintaining the 'Galixo' dark theme, retaining slider inputs in the Stress Tester, and tracking your active navigation tabs.</li>
            <li><b>Zero Third-Party Tracking:</b> Unlike ad-tech platforms, we process exactly zero tracking cookies. Your financial data and browsing habits never leave our highly secure ecosystem. We do not use Google Analytics or Meta Pixels.</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

"""

# Insert functions before show_dashboard
if "def show_dashboard(" in dash_content:
    dash_content = dash_content.replace("def show_dashboard(", legal_funcs + "\ndef show_dashboard(")

# Insert routing logic inside show_dashboard
route_logic = """
    if app_mode == 'landing':
"""
new_route_logic = """
    if app_mode == 'privacy':
        render_privacy_policy()
        return
    elif app_mode == 'terms':
        render_terms()
        return
    elif app_mode == 'cookie':
        render_cookie()
        return
    elif app_mode == 'landing':
"""
dash_content = dash_content.replace(route_logic, new_route_logic)

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Refactor completed.")
