import sys

# Update dashboard.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Replace the render functions
start_funcs = dash_content.find('def render_privacy_policy():')
end_funcs = dash_content.find('def show_dashboard(user):')

new_funcs = '''def render_privacy_policy():
    if st.button("⬅️ Return to App", key="back_from_privacy"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Privacy Policy")
    st.markdown("Welcome to **FinAnalyze**. Your privacy is our top priority. We do not store your raw bank statements or account numbers. We use secure session states and API endpoints (like Groq) strictly for generating your financial personality profile. Data is wiped after your session ends.")

def render_terms():
    if st.button("⬅️ Return to App", key="back_from_terms"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Terms of Service")
    st.markdown("By using **FinAnalyze**, you agree that this tool is for educational and profiling purposes only and does not constitute professional financial advice. All K-Means clustering insights are automated estimations.")

def render_cookie():
    if st.button("⬅️ Return to App", key="back_from_cookie"):
        st.session_state['app_mode'] = 'dashboard'
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Cookie Policy")
    st.markdown("We strictly use session-based states (similar to essential cookies) to maintain your active session, keep your Galixo dark theme preferences active, and ensure smooth navigation. No tracking cookies are deployed.")

'''

if start_funcs != -1 and end_funcs != -1:
    dash_content = dash_content[:start_funcs] + new_funcs + dash_content[end_funcs:]
else:
    print('Could not find existing render functions.')

# Replace routing logic
routing_start = dash_content.find("    if 'app_mode' not in st.session_state:")
if routing_start == -1:
    # Fallback to the known old logic start
    routing_start = dash_content.find("    if app_mode == 'landing':")
    # Actually wait, let's search for "    app_mode = st.session_state.get('app_mode', 'landing')"
    app_mode_line = dash_content.find("    app_mode = st.session_state.get('app_mode', 'landing')")
    if app_mode_line != -1:
        routing_start = app_mode_line
        
routing_end = dash_content.find("    elif app_mode == 'landing':")
if routing_end == -1:
    routing_end = dash_content.find("    if app_mode == 'landing':")

new_routing = '''    if 'app_mode' not in st.session_state:
        st.session_state['app_mode'] = 'dashboard'

    if st.session_state['app_mode'] == 'privacy':
        render_privacy_policy()
        return # or st.stop()
    elif st.session_state['app_mode'] == 'terms':
        render_terms()
        return # or st.stop()
    elif st.session_state['app_mode'] == 'cookie':
        render_cookie()
        return # or st.stop()

    app_mode = st.session_state['app_mode']

    if app_mode == 'landing':
'''

if routing_start != -1 and routing_end != -1:
    # Need to trim correctly so we don't duplicate `if app_mode == 'landing':`
    end_replace_idx = dash_content.find(":", routing_end) + 1
    dash_content = dash_content[:routing_start] + new_routing + dash_content[end_replace_idx:]
    print("Replaced routing successfully")
else:
    print('Could not find existing routing logic.')

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash_content)


# Update utils.py
with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'r', encoding='utf-8') as f:
    utils_content = f.read()

utils_buttons_start = utils_content.find('        st.markdown("<h4 style=\\'color: #fff; margin-bottom: 20px; font-size: 1.1rem;\\'>Legal</h4>", unsafe_allow_html=True)')
utils_buttons_end = utils_content.find('    with c4:')

new_buttons = '''        st.markdown("**Legal**")
        with st.container():
            st.markdown('<div class="footer-link">', unsafe_allow_html=True)
            if st.button("Privacy Policy", key="footer_btn_privacy", use_container_width=True):
                st.session_state['app_mode'] = 'privacy'
                st.rerun()
            if st.button("Terms of Service", key="footer_btn_terms", use_container_width=True):
                st.session_state['app_mode'] = 'terms'
                st.rerun()
            if st.button("Cookie Policy", key="footer_btn_cookie", use_container_width=True):
                st.session_state['app_mode'] = 'cookie'
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

'''

if utils_buttons_start != -1 and utils_buttons_end != -1:
    utils_content = utils_content[:utils_buttons_start] + new_buttons + utils_content[utils_buttons_end:]
    with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\utils.py', 'w', encoding='utf-8') as f:
        f.write(utils_content)
    print('Successfully updated utils.py')
else:
    print('Could not find utils.py button logic.')

