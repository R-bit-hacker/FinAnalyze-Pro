import streamlit as st
from utils import show_footer, get_icon, scroll_to_top

def show_privacy_page():
    # --- AUTO SCROLL TO TOP ---
    scroll_to_top()

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 50px;">
        {get_icon('lock', '#00f260', 50)}
        <h1 class="gradient-text" style="font-size: 3rem; margin-top: 20px;">Privacy Policy</h1>
        <p style="color: #888; font-size: 1.1rem;">Your data security is our top priority. Last Updated: January 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
<div style="padding: 20px; border-left: 4px solid #00f260; background: rgba(0,242,96,0.05); margin-bottom: 30px;">
    <h3 style="display:flex; align-items:center; gap:10px; margin:0; color: white;">The Short Version</h3>
    <p style="color: #ccc; line-height: 1.7; font-size: 1.05rem; margin-top: 10px; margin-bottom:0;">
        We only collect financial data (income, expenses, savings) to generate your AI persona. 
        Your passwords are hashed (bcrypt). We <b>never</b> sell your data to third parties.
    </p>
</div>
""", unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: white;">1. Data We Collect</h3>
    <ul style="color: #aaa; line-height: 1.8; margin-top: 15px;">
        <li><b>Account Info:</b> Name, Email (for login).</li>
        <li><b>Financial Inputs:</b> Income, Expense, Savings, Debt numbers solely for analysis.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
        
    with c2:
        st.markdown("""
<div class="glass-card">
    <h3 style="color: white;">2. How We Use It</h3>
    <ul style="color: #aaa; line-height: 1.8; margin-top: 15px;">
        <li>To run the K-Means Clustering algorithm.</li>
        <li>To provide personalized financial advice.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br><h2 style='text-align:center;'>Common Questions</h2><br>", unsafe_allow_html=True)

    with st.expander("Is my financial data connected to my real bank account?"):
        st.write("No. FinAnalyze operates on data you manually enter. We do not have access to your actual bank accounts.")
        
    with st.expander("How secure is my password?"):
        st.write("Very secure. We use industry-standard bcrypt hashing. Even our developers cannot see your actual password.")
        
    with st.expander("Can I delete my data?"):
        st.write("Yes. Send a request through the Contact page, and we will permanently wipe your data from our servers.")

    show_footer()