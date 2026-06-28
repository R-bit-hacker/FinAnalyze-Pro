import sys
import os

# 1. Update utils.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'r', encoding='utf-8') as f:
    utils_content = f.read()

utils_content = utils_content.replace(
    "st.session_state['app_mode'] = 'privacy'",
    "st.session_state['page'] = 'privacy'"
)
utils_content = utils_content.replace(
    "st.session_state['app_mode'] = 'terms'",
    "st.session_state['page'] = 'terms'"
)
utils_content = utils_content.replace(
    "st.session_state['app_mode'] = 'cookie'",
    "st.session_state['page'] = 'cookie'"
)

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'w', encoding='utf-8') as f:
    f.write(utils_content)

# 2. Update dashboard.py (remove the injected render functions and routing)
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'r', encoding='utf-8') as f:
    dash_content = f.read()

start_funcs = dash_content.find('def render_privacy_policy():')
if start_funcs != -1:
    end_funcs = dash_content.find('def show_dashboard(user):')
    if end_funcs != -1:
        dash_content = dash_content[:start_funcs] + dash_content[end_funcs:]

start_route = dash_content.find("    if 'app_mode' not in st.session_state:")
if start_route != -1:
    end_route = dash_content.find("    # --- CUSTOM CSS INJECTION ---")
    if end_route != -1:
        dash_content = dash_content[:start_route] + dash_content[end_route:]

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash_content)


# 3. Update app.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'r', encoding='utf-8') as f:
    app_content = f.read()

render_funcs = """

def render_privacy_policy():
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
    st.markdown("We strictly use session-based states (similar to essential cookies) to maintain your active session, keep your Galixo dark theme preferences active, and ensure smooth navigation. No tracking cookies are deployed.")

# --- ROUTING LOGIC ---
"""

# Inject render functions above # --- ROUTING LOGIC ---
app_content = app_content.replace("# --- ROUTING LOGIC ---", render_funcs)

# Now fix the shadowing issue. Move OTHER PAGES to the top of ROUTING LOGIC
other_pages_block = """
# 4. OTHER PAGES
elif st.session_state['page'] == 'about': show_navbar(); show_about_page()
elif st.session_state['page'] == 'contact': show_navbar(); show_contact_page()
elif st.session_state['page'] == 'privacy': show_navbar(); show_privacy_page()
elif st.session_state['page'] == 'demo': show_navbar(); show_demo_page()
"""
app_content = app_content.replace(other_pages_block, "")

new_routing_block = """
# 0. OTHER PAGES (Highest Priority to avoid shadowing)
if st.session_state['page'] == 'about': show_navbar(); show_about_page()
elif st.session_state['page'] == 'contact': show_navbar(); show_contact_page()
elif st.session_state['page'] == 'demo': show_navbar(); show_demo_page()
elif st.session_state['page'] == 'privacy': render_privacy_policy()
elif st.session_state['page'] == 'terms': render_terms()
elif st.session_state['page'] == 'cookie': render_cookie()

# 1. LANDING PAGE
elif st.session_state['page'] == 'landing':
"""

app_content = app_content.replace("# 1. LANDING PAGE\nif st.session_state['page'] == 'landing':", new_routing_block)

# If they click return and are logged in, they go to dashboard page, but wait, dashboard page is just 'landing' while logged in? No, `page` isn't used for logged in normally, it just falls back to the user condition. But if page is set to 'dashboard', the first ifs won't match, and it will fall down to the `elif st.session_state['user']:` which is exactly what we want!

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\app.py', 'w', encoding='utf-8') as f:
    f.write(app_content)

print("Fix applied successfully.")
