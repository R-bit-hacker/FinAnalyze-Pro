import streamlit as st
from utils import show_footer, get_icon, scroll_to_top

def show_demo_page():
    scroll_to_top()
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center;">
        <span style="color:#00c6ff; font-weight:bold; letter-spacing:1px;">PRODUCT TOUR</span>
        <h1 class="gradient-text" style="font-size: 3rem;">How FinAnalyze Works</h1>
        <p style="color: #888; font-size: 1.1rem;">A simple 3-step process to financial clarity.</p>
    </div>
    <br><br>
    """, unsafe_allow_html=True)

    # --- STEP 1 ---
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #00c6ff;">
            <h2 style="color:white;">01. Input Data</h2>
            <p style="color:#aaa;">Enter your basic financial details securely. We ask for:</p>
            <ul style="color:#aaa;">
                <li>Monthly Income</li>
                <li>Expenses & Savings</li>
                <li>Debt Liabilities</li>
            </ul>
            <p style="color:#00c6ff; font-size:0.9rem;">{get_icon('lock', '#00c6ff', 16)} Data is encrypted.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        # Placeholder for visual
        st.markdown(f"""
        <div style="padding:40px; text-align:center; background:rgba(255,255,255,0.02); border-radius:20px; border:1px dashed #333;">
            {get_icon('edit', '#666', 60)}
            <p style="color:#666; margin-top:10px;">User Input Form Interface</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- STEP 2 ---
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown(f"""
        <div style="padding:40px; text-align:center; background:rgba(255,255,255,0.02); border-radius:20px; border:1px dashed #333;">
            {get_icon('bulb', '#666', 60)}
            <p style="color:#666; margin-top:10px;">AI Processing Engine</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #00f260;">
            <h2 style="color:white;">02. AI Processing</h2>
            <p style="color:#aaa;">Our K-Means Clustering algorithm analyzes your data points against thousands of profiles to determine your unique <b>Financial Persona</b>.</p>
            <ul style="color:#aaa;">
                <li>Identifies Spending Patterns</li>
                <li>Benchmarks against 50/30/20 Rule</li>
                <li>Detects Risk Factors</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- STEP 3 ---
    c1, c2 = st.columns([1, 1], gap="large")
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #ff0844;">
            <h2 style="color:white;">03. Get Insights</h2>
            <p style="color:#aaa;">Receive a comprehensive dashboard with visualization and actionable advice tailored to you.</p>
            <ul style="color:#aaa;">
                <li>Interactive Charts</li>
                <li>Savings Trajectory</li>
                <li>Personalized AI Recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="padding:40px; text-align:center; background:rgba(255,255,255,0.02); border-radius:20px; border:1px dashed #333;">
            {get_icon('dashboard', '#666', 60)}
            <p style="color:#666; margin-top:10px;">Final Dashboard View</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # CTA
    st.markdown("""
    <div style="text-align:center;">
        <h2>Ready to see your report?</h2>
        <br>
    </div>
    """, unsafe_allow_html=True)
    
    col_center = st.columns([1, 1, 1])
    with col_center[1]:
        if st.button("CREATE ACCOUNT", type="primary", use_container_width=True):
            st.session_state['page'] = 'auth'
            st.rerun()

    show_footer()