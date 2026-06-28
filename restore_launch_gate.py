import sys

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'r', encoding='utf-8') as f:
    dash_content = f.read()

# Replace condition
dash_content = dash_content.replace(
    "if st.session_state.get('app_mode') == 'landing':",
    "if not st.session_state.get('dashboard_launched', False):"
)

# Replace launch button action
dash_content = dash_content.replace(
    "st.session_state['app_mode'] = 'dashboard'",
    "st.session_state['dashboard_launched'] = True"
)

# Replace back button action
dash_content = dash_content.replace(
    "st.session_state['app_mode'] = 'landing'",
    "st.session_state['dashboard_launched'] = False"
)

with open(r'c:\Users\DELL\Desktop\Financial_Profiler_FYP\src\dashboard.py', 'w', encoding='utf-8') as f:
    f.write(dash_content)

print("Dashboard launch logic restored.")
