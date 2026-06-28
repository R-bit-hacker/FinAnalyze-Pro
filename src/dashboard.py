import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np
import PyPDF2
# Direct ML import
from ml_logic import load_models, get_ai_advice, calculate_finscore, get_future_growth_verdict, parse_bank_statement_with_llm
from utils import save_analysis_to_db, get_user_history, get_icon 

def show_dashboard(user):
    # --- AUTO-REDIRECT SHADOW STATE FIX ---
    if st.session_state.get('redirect_to_overview'):
        st.session_state['current_page'] = 'Overview / Dashboard'
        st.session_state['redirect_to_overview'] = False

    # --- CUSTOM CSS INJECTION ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    /* Hide Streamlit Artifacts */
    #MainMenu {visibility: hidden;} 
    footer {visibility: hidden;} 
    header {visibility: hidden;} 
    .block-container {padding-top: 1rem;}

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp, [data-testid="stSidebar"] {
        background-color: #030305;
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    @keyframes float {
        0% {transform: translateY(0px);}
        50% {transform: translateY(-8px);}
        100% {transform: translateY(0px);}
    }
    @keyframes pulseGlow {
        0% {box-shadow: 0 0 10px rgba(138, 43, 226, 0.4);}
        50% {box-shadow: 0 0 25px rgba(138, 43, 226, 0.8), 0 0 10px rgba(0, 210, 255, 0.5);}
        100% {box-shadow: 0 0 10px rgba(138, 43, 226, 0.4);}
    }

    .fade-in-up {
        animation: fadeInUp 0.8s ease-out forwards;
        opacity: 0;
    }
    .delay-0 { animation-delay: 0s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-4 { animation-delay: 0.4s; }

    .float-anim {
        animation: float 4s ease-in-out infinite;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #8a2be2, #00d2ff);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: transform 0.2s, box-shadow 0.2s;
        animation: pulseGlow 2s infinite;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        color: #ffffff;
    }
    
    /* Glowing Glassmorphism Cards */
    .saas-card {
        background: rgba(20, 20, 30, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(138, 43, 226, 0.3);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.1);
        transition: all 0.3s ease;
    }
    .saas-card:hover {
        transform: scale(1.03) !important;
        border: 1px solid rgba(138, 43, 226, 0.8);
        box-shadow: 0 0 30px rgba(138, 43, 226, 0.4);
    }
    
    .header-title {
        font-weight: 700;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #b066ff, #00d2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .text-muted {
        color: #8c8c9e;
    }
    .text-success {
        color: #00ffcc;
    }
    .text-primary {
        color: #00d2ff;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional Colors
    COLOR_INCOME = "#10b981" # Emerald Green
    COLOR_EXPENSE = "#ef4444" # Red
    COLOR_SAVINGS = "#8b5cf6" # Purple
    COLOR_DEBT = "#f59e0b" # Amber
    COLOR_IDEAL = "#2563eb" # Tech Blue

    if not st.session_state.get('dashboard_launched', False):
        st.markdown('''
            <style>
                [data-testid="stSidebar"] {display: none;}
                [data-testid="collapsedControl"] {display: none;}
            </style>
        ''', unsafe_allow_html=True)
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 8, 1])
        with c2:
            st.markdown(f"""
            <div style="text-align: center;">
                <h1 class="header-title fade-in-up delay-0" style="font-size: 4rem; line-height: 1.1; margin-bottom: 20px;">Master Your Financial Future with AI</h1>
                <p class="text-muted fade-in-up delay-2" style="font-size: 1.2rem; max-width: 700px; margin: 0 auto 40px auto; line-height: 1.6;">
                    Welcome, {user['name']}. Our neural network profiles your spending habits, projects your wealth trajectory, and delivers personalized strategies to accelerate your financial independence.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2, btn_col3 = st.columns([3, 2, 3])
            with btn_col2:
                if st.button("Launch App ➔", use_container_width=True):
                    st.session_state['dashboard_launched'] = True
                    st.rerun()
            
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                st.markdown("""
                <div class="fade-in-up delay-4">
                    <div class="float-anim">
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <h3 style="color: #00d2ff; margin-top: 0; font-weight: 700;">AI Profiler</h3>
                            <p class="text-muted" style="margin-bottom: 0;">Our K-Means clustering algorithm maps your unique financial DNA against millions of data points to identify your precise spending persona.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with fc2:
                st.markdown("""
                <div class="fade-in-up delay-4">
                    <div class="float-anim">
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <h3 style="color: #b066ff; margin-top: 0; font-weight: 700;">Wealth Forecaster</h3>
                            <p class="text-muted" style="margin-bottom: 0;">Predictive analytics engine that compounds your current cash flow to visualize your 10-year financial trajectory.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with fc3:
                st.markdown("""
                <div class="fade-in-up delay-4">
                    <div class="float-anim">
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <h3 style="color: #00ffcc; margin-top: 0; font-weight: 700;">Smart Categorizer</h3>
                            <p class="text-muted" style="margin-bottom: 0;">Instantly parse raw PDF bank statements. Our LLM pipeline securely categorizes your lifestyle and essential expenses.</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        # Header
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 30px;">
            <div>
                <h2 class="header-title" style="margin-bottom:0;">FinAnalyze Enterprise</h2>
                <p class="text-muted" style="font-size:0.9rem; margin-top:5px;">Analysis Dashboard for <b>{user['name']}</b></p>
            </div>
            <div style="text-align:right;">
                 <span style="background: #2563eb; color:white; padding: 6px 15px; border-radius:6px; font-size:0.75rem; font-weight:600; letter-spacing: 1px;">PRO PLAN</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = "Overview / Dashboard"

        menu = st.sidebar.radio("Main Menu", ["Overview / Dashboard", "New Analysis", "Future Projections", "Robo-Advisor", "History Log"], key="current_page")
        
        st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.sidebar.button("⬅️ Back to Home"):
            st.session_state['dashboard_launched'] = False
            st.rerun()

        if menu == "Overview / Dashboard":
            if st.session_state.get('report') is None:
                st.markdown("""
                <div class="saas-card" style="text-align: center; margin-top: 50px;">
                    <h3 class="header-title">Welcome to FinAnalyze</h3>
                    <p class="text-muted" style="max-width: 600px; margin: 20px auto; line-height: 1.6;">
                        Our platform leverages advanced machine learning models to profile your financial behavior, project your wealth accumulation, and deliver highly personalized strategic recommendations.
                    </p>
                    <p class="text-muted" style="margin-bottom: 30px;">To begin generating your insights, please navigate to <b>New Analysis</b> in the sidebar.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                rep = st.session_state['report']
                st.markdown("<h3 class='header-title'>Executive Summary</h3><br>", unsafe_allow_html=True)
                
                # Executive Summary Layout
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"""
                    <div class="saas-card" style="height: 100%;">
                        <p class="text-muted" style="text-transform: uppercase; font-size: 0.8rem; margin-bottom: 10px; font-weight: 600;">Current Persona</p>
                        <h2 class="text-primary" style="margin: 0; font-weight: 800;">{rep['persona']}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    # Calculate 10-year projection quickly for overview
                    current_sav = rep['sav']
                    monthly_sav = max(0, rep['inc'] - rep['exp'])
                    monthly_rate = 0.12 / 12
                    months = 120
                    fv_principal = current_sav * ((1 + monthly_rate) ** months)
                    fv_contributions = monthly_sav * (((1 + monthly_rate) ** months - 1) / monthly_rate) if monthly_rate > 0 else monthly_sav * months
                    proj_10 = fv_principal + fv_contributions
                    
                    st.markdown(f"""
                    <div class="saas-card" style="height: 100%;">
                        <p class="text-muted" style="text-transform: uppercase; font-size: 0.8rem; margin-bottom: 10px; font-weight: 600;">10-Year Projected Wealth</p>
                        <h2 class="text-success" style="margin: 0; font-weight: 800;">PKR {proj_10:,.0f}</h2>
                    </div>
                    """, unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""
                    <div class="saas-card" style="height: 100%;">
                        <p class="text-muted" style="text-transform: uppercase; font-size: 0.8rem; margin-bottom: 10px; font-weight: 600;">Monthly Cash Flow</p>
                        <p style="margin: 0; color: #fff;">Income: PKR {rep['inc']:,}</p>
                        <p style="margin: 0; color: #fff;">Expenses: PKR {rep['exp']:,}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br><h4 class='header-title'>Recent Profile Analysis</h4>", unsafe_allow_html=True)
                
                # --- PREMIUM FINSCORE GAUGE CHART ---
                fin_score, fin_status = calculate_finscore(rep['inc'], rep['exp'], rep['sav'], rep['dbt'])
                status_color = COLOR_INCOME if fin_score >= 650 else (COLOR_DEBT if fin_score >= 500 else COLOR_EXPENSE)
                if fin_score >= 750: status_color = COLOR_SAVINGS

                st.markdown(f"""
                <div class="saas-card" style="margin-bottom: 30px; padding-bottom:0;">
                    <h4 style="text-align: center; color: #a3a3a3; font-weight: 600; margin-bottom: -15px;">Proprietary FinScore</h4>
                """, unsafe_allow_html=True)

                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = fin_score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    number = {'font': {'size': 50, 'color': status_color, 'weight': 'bold'}},
                    title = {'text': f"<br><span style='font-size:1.2rem; color:#a3a3a3'>Status: </span><span style='font-size:1.2rem; color:{status_color};'>{fin_status}</span>"},
                    gauge = {
                        'axis': {'range': [300, 850], 'tickwidth': 1, 'tickcolor': "#444", 'tickfont': dict(color="#a3a3a3")},
                        'bar': {'color': "rgba(255,255,255,0.8)", 'thickness': 0.15},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 0,
                        'steps': [
                            {'range': [300, 500], 'color': f"rgba(239, 68, 68, 0.2)"}, 
                            {'range': [500, 650], 'color': f"rgba(245, 158, 11, 0.2)"}, 
                            {'range': [650, 750], 'color': f"rgba(16, 185, 129, 0.2)"}, 
                            {'range': [750, 850], 'color': f"rgba(139, 92, 246, 0.4)"} 
                        ],
                        'threshold': {
                            'line': {'color': status_color, 'width': 4},
                            'thickness': 0.75,
                            'value': fin_score
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", 
                    plot_bgcolor="rgba(0,0,0,0)", 
                    height=280, 
                    margin=dict(t=30, b=10, l=10, r=10)
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                c4, c5 = st.columns(2)
                with c4:
                    fig_combo = go.Figure()
                    fig_combo.add_trace(go.Bar(x=['Needs', 'Wants', 'Savings'], y=[rep['needs'], rep['wants'], rep['sav']], name='You', marker_color=COLOR_SAVINGS))
                    fig_combo.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color='#a3a3a3'))
                    st.plotly_chart(fig_combo, use_container_width=True)
                
                with c5:
                    fig_donut = px.pie(names=['Needs', 'Wants', 'Savings', 'Debt'], values=[rep['needs'], rep['wants'], rep['sav'], rep['dbt']], hole=0.6, color_discrete_sequence=[COLOR_EXPENSE, COLOR_DEBT, COLOR_SAVINGS, COLOR_INCOME])
                    fig_donut.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)", 
                        plot_bgcolor="rgba(0,0,0,0)", 
                        font=dict(color='#a3a3a3'),
                        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
                        margin=dict(t=20, b=20, l=0, r=0)
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)

                st.markdown("<h4 class='header-title' style='margin-top: 30px;'>Strategic Recommendations</h4>", unsafe_allow_html=True)
                if rep.get('advice_error'):
                    st.error(f"Error fetching AI recommendations: {rep['advice_error']}")
                else:
                    st.markdown(f"<div class='saas-card'>{rep['advice']}</div>", unsafe_allow_html=True)

        elif menu == "New Analysis":
            st.markdown("<h3 class='header-title'>Data Entry Interface</h3>", unsafe_allow_html=True)
            
            input_method = st.radio("Select Input Method:", ["Manual Entry", "Upload Bank Statement (CSV / PDF)"], horizontal=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            inc = exp = sav = dbt = needs = wants = 0
            ready_to_analyze = False
            
            if input_method == "Manual Entry":
                c1, c2 = st.columns(2)
                inc = c1.number_input("Monthly Income (PKR)", 0, 10000000, 100000, step=5000)
                exp = c2.number_input("Monthly Expenses (PKR)", 0, 10000000, 50000, step=5000)
                
                c3, c4 = st.columns(2)
                sav = c3.number_input("Total Savings (PKR)", 0, 10000000, 20000, step=5000)
                dbt = c4.number_input("Outstanding Debt (PKR)", 0, 10000000, 0, step=5000)
                
                st.markdown("<br><p class='text-muted' style='font-weight:600;'>Spending Breakdown</p>", unsafe_allow_html=True)
                needs = st.slider("Essentials (Rent, Food, Bills)", 0, int(inc) if inc>0 else 100000, int(inc*0.5))
                wants = st.slider("Lifestyle (Shopping, Outings)", 0, int(inc) if inc>0 else 100000, int(inc*0.3))
                
                ready_to_analyze = st.button("Execute Analysis", type="primary")

            elif input_method == "Upload Bank Statement (CSV / PDF)":
                st.info("Upload your bank statement. Our Natural Language Processing engine will securely parse and categorize your expenses.")
                st.caption("Privacy Notice: As this is a prototype, please upload redacted or dummy statements. Do not upload documents with sensitive PII.")
                
                with st.expander("View Supported Formats"):
                    st.markdown("""
                    **CSV Support**: Requires a `Description` and an `Amount` column.
                    
                    **PDF Support**: Standard PDF statement. The AI engine will scan and extract all outgoing transactions.
                    """)
                
                uploaded_file = st.file_uploader("Select Bank Statement (CSV / PDF)", type=['csv', 'pdf'])
                
                if uploaded_file:
                    needs_total = 0
                    wants_total = 0
                    extraction_success = False
                    
                    if uploaded_file.name.endswith('.csv'):
                        try:
                            df_csv = pd.read_csv(uploaded_file)
                            df_csv.columns = df_csv.columns.str.lower()
                            
                            if 'description' in df_csv.columns and 'amount' in df_csv.columns:
                                needs_keywords = ['electric', 'rent', 'grocery', 'hospital', 'pharmacy', 'utility', 'kelectric', 'sui gas', 'school', 'fee', 'supermarket', 'mart', 'bill']
                                wants_keywords = ['netflix', 'steam', 'foodpanda', 'cinema', 'shopping', 'kfc', 'mcdonalds', 'daraz', 'restaurant', 'spotify', 'dine-in', 'cafe', 'game', 'entertainment']
                                
                                for index, row in df_csv.iterrows():
                                    desc = str(row['description']).lower()
                                    try:
                                        amt = float(row['amount'])
                                    except:
                                        continue
                                    
                                    is_need = any(kw in desc for kw in needs_keywords)
                                    is_want = any(kw in desc for kw in wants_keywords)
                                    
                                    if is_want: wants_total += amt
                                    elif is_need: needs_total += amt
                                    else: needs_total += amt
                                extraction_success = True
                            else:
                                st.error("Validation Error: CSV must contain 'Description' and 'Amount' columns.")
                        except Exception as e:
                            st.error(f"Error reading CSV: {e}")
                            
                    elif uploaded_file.name.endswith('.pdf'):
                        with st.spinner("Processing document via NLP engine..."):
                            try:
                                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                                raw_text = ""
                                for page in pdf_reader.pages:
                                    text = page.extract_text()
                                    if text:
                                        raw_text += text + "\n"
                                        
                                needs_total, wants_total = parse_bank_statement_with_llm(raw_text)
                                extraction_success = True
                            except Exception as e:
                                st.error(f"Failed to parse PDF: {e}")
                    
                    if extraction_success:
                        needs = needs_total
                        wants = wants_total
                        exp = needs + wants
                        
                        st.success("Categorization Engine complete.")
                        st.markdown(f"""
                        <div class="saas-card" style="border-left: 4px solid {COLOR_SAVINGS}; margin-bottom: 20px;">
                            <h4 style="margin:0; color:white;">Extracted Summary</h4>
                            <ul style="color:#a3a3a3; margin-top:10px; font-size: 1.1rem;">
                                <li><b>Essentials:</b> PKR {needs:,.0f}</li>
                                <li><b>Lifestyle:</b> PKR {wants:,.0f}</li>
                            </ul>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<p class='text-muted'>Please complete the required financial parameters below to finalize processing.</p>", unsafe_allow_html=True)
                        
                        c1, c2, c3 = st.columns(3)
                        inc = c1.number_input("Monthly Income (PKR)", 0, 10000000, 100000, step=5000)
                        sav = c2.number_input("Total Savings (PKR)", 0, 10000000, 20000, step=5000)
                        dbt = c3.number_input("Outstanding Debt (PKR)", 0, 10000000, 0, step=5000)
                        
                        ready_to_analyze = st.button("Execute Analysis", type="primary")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- ML ANALYSIS BLOCK ---
            if ready_to_analyze:
                with st.spinner("Executing machine learning prediction pipelines..."):
                    try:
                        kmeans, scaler, pca, cluster_mapping = load_models()
                        if kmeans is None or scaler is None or cluster_mapping is None:
                            st.error("System Error: ML models unavailable.")
                        else:
                            savings_rate = sav / inc if inc > 0 else 0
                            debt_to_income_ratio = dbt / inc if inc > 0 else 0
                            expense_ratio = exp / inc if inc > 0 else 0
                            lifestyle_ratio = wants / (needs + 1)

                            features = np.array([[inc, exp, savings_rate, debt_to_income_ratio, wants, needs, 0, 0, expense_ratio, lifestyle_ratio]])
                            scaled_data = scaler.transform(features)
                            cluster = int(kmeans.predict(scaled_data)[0])
                            
                            p_name = cluster_mapping.get(str(cluster), "Balanced Spender")
                            
                            try:
                                advice = get_ai_advice(p_name, inc, sav)
                                advice_error = None
                            except Exception as e:
                                advice_error = str(e)
                                advice = ""
                                
                            save_analysis_to_db(user['id'], inc, exp, sav, dbt, p_name)

                            st.session_state['report'] = {
                                'inc': inc, 'exp': exp, 'sav': sav, 'dbt': dbt, 
                                'persona': p_name, 'needs': needs, 'wants': wants, 
                                'advice': advice,
                                'advice_error': advice_error
                            }
                            st.session_state['redirect_to_overview'] = True
                            st.rerun()
                    except Exception as e:
                        st.error(f"Analysis process failed: {str(e)}")

        elif menu == "History Log":
            history_data = get_user_history(user['id'])
            if history_data:
                df_hist = pd.DataFrame(history_data, columns=['Income', 'Expense', 'Savings', 'Debt', 'Persona', 'Date'])
                df_hist['Date'] = pd.to_datetime(df_hist['Date'])
                df_hist = df_hist.sort_values(by='Date')

                st.markdown("<h3 class='header-title'>Transaction History</h3>", unsafe_allow_html=True)
                st.dataframe(df_hist, use_container_width=True, hide_index=True)

                st.markdown("<br><h3 class='header-title'>Savings Trajectory</h3>", unsafe_allow_html=True)
                
                fig_trajectory = px.area(
                    df_hist, 
                    x='Date', 
                    y='Savings', 
                    markers=True,
                    color_discrete_sequence=[COLOR_SAVINGS] 
                )
                
                fig_trajectory.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#a3a3a3'),
                    xaxis_title="Date",
                    yaxis_title="Savings",
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                fig_trajectory.update_xaxes(showgrid=False)
                fig_trajectory.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                
                st.plotly_chart(fig_trajectory, use_container_width=True)
                
            else:
                st.info("System has no recorded history for this user.")

        elif menu == "Robo-Advisor":
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px;">
                <h3 class="header-title" style="margin:0;">Robo-Advisor Interface</h3>
                <span style="background: rgba(139, 92, 246, 0.2); color: #8b5cf6; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid #8b5cf6; font-weight:600;">BETA</span>
            </div>
            <p class="text-muted" style="margin-bottom: 20px;">Utilize automated strategic modeling to validate your financial targets.</p>
            """, unsafe_allow_html=True)
            
            current_inc = (st.session_state.get('report') or {}).get('inc', 100000)
            current_exp = (st.session_state.get('report') or {}).get('exp', 60000)
            current_sav = (st.session_state.get('report') or {}).get('sav', 0)
            
            if st.session_state.get('report') is None:
                st.warning("Data Dependency Error: Please execute a 'New Analysis' to establish baseline income and expenditure vectors.")
            else:
                with st.form("goal_planner_form"):
                    gc1, gc2 = st.columns(2)
                    goal_name = gc1.text_input("Target Objective", placeholder="e.g., Enterprise Server, Real Estate")
                    target_amount = gc2.number_input("Target Amount (PKR)", min_value=1000, value=250000, step=10000)
                    
                    gc3, gc4 = st.columns(2)
                    months = gc3.slider("Timeline (Months)", min_value=1, max_value=60, value=12)
                    allocated_savings = gc4.number_input("Current Allocated Capital (PKR)", min_value=0, value=0, step=5000)
                    
                    plan_btn = st.form_submit_button("Generate Strategy", type="primary", use_container_width=True)
                    
                if plan_btn:
                    if not goal_name:
                        st.error("Validation Error: Target Objective is required.")
                    else:
                        from ml_logic import robo_advisor_plan
                        
                        req_monthly, advice, status_color = robo_advisor_plan(
                            target_amount, months, allocated_savings, current_inc, current_exp
                        )
                        
                        advice = advice.replace("```html", "").replace("```", "").strip()
                        
                        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
                        
                        st.html(f"""
                        <div class="saas-card" style="border-top: 4px solid {status_color}; text-align: center;">
                            <p style="color: #a3a3a3; text-transform: uppercase; letter-spacing: 1px; font-size: 0.85rem; margin-bottom: 5px;">Strategic Blueprint For</p>
                            <h2 style="color: white; margin-top: 0; font-weight: 800;">{goal_name}</h2>
                            
                            <div style="margin: 30px 0;">
                                <p style="color: #a3a3a3; margin-bottom: 5px;">Required Monthly Capital Allocation</p>
                                <h1 style="color: {status_color}; font-size: 3rem; margin: 0; font-weight: 800;">PKR {req_monthly:,.0f}</h1>
                                <p style="color: #666; font-size: 0.9rem;">over a {months}-month period</p>
                            </div>
                            
                            <div style="background: rgba(0,0,0,0.2); padding: 20px; border-radius: 8px; border-left: 4px solid {status_color}; text-align: left;">
                                <h4 style="margin: 0 0 10px 0; color: white;">Algorithmic Verdict</h4>
                                <p style="margin: 0; color: #d4d4d4; font-weight: 400; line-height: 1.6;">{advice}</p>
                            </div>
                        </div>
                        """)  
                        
        elif menu == "Future Projections":
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:10px;">
                <h3 class="header-title" style="margin:0;">Wealth Forecasting Module</h3>
                <span style="background: rgba(37, 99, 235, 0.2); color: #2563eb; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid #2563eb; font-weight:600;">ENTERPRISE</span>
            </div>
            <p class="text-muted" style="margin-bottom: 20px;">Run compounding predictive models on your current trajectory.</p>
            """, unsafe_allow_html=True)

            
            forecast_mode = st.radio('Forecast Mode', ['Standard Projection', 'Stress-Test Simulator'], horizontal=True, label_visibility='collapsed')

            if forecast_mode == 'Standard Projection':
                if st.session_state.get('report') is None:
                    st.warning("Data Dependency Error: Baseline analytics required. Run 'New Analysis' first.")
                else:
                    rep = st.session_state['report']
                    current_sav = rep['sav']
                    monthly_sav = rep['inc'] - rep['exp']
                    
                    if monthly_sav < 0:
                        monthly_sav = 0
                        st.info("System Notice: Expenditures exceed income. Monthly allocation defaulted to 0 PKR for projection integrity.")
                    
                    annual_rate = 0.12
                    monthly_rate = annual_rate / 12
                    
                    years = np.arange(0, 11)
                    projected = []
                    
                    for y in years:
                        months = y * 12
                        fv_principal = current_sav * ((1 + monthly_rate) ** months)
                        if monthly_rate > 0:
                            fv_contributions = monthly_sav * (((1 + monthly_rate) ** months - 1) / monthly_rate)
                        else:
                            fv_contributions = monthly_sav * months
                            
                        projected.append(fv_principal + fv_contributions)
                        
                    df_proj = pd.DataFrame({
                        'Year': years,
                        'Projected Capital': projected
                    })
                    
                    fig_proj = px.area(
                        df_proj, 
                        x='Year', 
                        y='Projected Capital', 
                        markers=True,
                        color_discrete_sequence=[COLOR_INCOME] 
                    )
                    fig_proj.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#a3a3a3'),
                        margin=dict(l=0, r=0, t=30, b=0)
                    )
                    fig_proj.update_xaxes(showgrid=False, tickvals=years)
                    fig_proj.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                    
                    st.plotly_chart(fig_proj, use_container_width=True)
                    
                    y5_val = projected[5]
                    y10_val = projected[10]
                    
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown(f"""
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <p style="color: #a3a3a3; margin:0; font-size: 0.85rem; text-transform: uppercase; font-weight:600;">5-Year Milestone</p>
                            <h2 style="color: {COLOR_INCOME}; margin: 10px 0; font-weight:800;">PKR {y5_val:,.0f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with pc2:
                        st.markdown(f"""
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <p style="color: #a3a3a3; margin:0; font-size: 0.85rem; text-transform: uppercase; font-weight:600;">10-Year Milestone</p>
                            <h2 style="color: {COLOR_SAVINGS}; margin: 10px 0; font-weight:800;">PKR {y10_val:,.0f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    with st.spinner("Executing Groq cloud inference..."):
                        try:
                            verdict = get_future_growth_verdict(current_sav, monthly_sav, projected[1], y5_val, y10_val, annual_rate)
                            st.markdown(f"""
                            <div class="saas-card" style="border-left: 4px solid {COLOR_INCOME};">
                                <h4 class="header-title" style="margin-top:0;">Predictive Analysis Summary</h4>
                                <div style="color:#d4d4d4; line-height: 1.6; font-size: 1.05rem;">{verdict}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        except Exception as e:
                            st.error(f"Inference failure: {e}")
            elif forecast_mode == 'Stress-Test Simulator':

                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:10px;">
                    <h3 class="header-title" style="margin:0;">What-If Stress Tester</h3>
                    <span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 3px 10px; border-radius: 6px; font-size: 0.75rem; border: 1px solid #ef4444; font-weight:600;">SIMULATOR</span>
                </div>
                <p class="text-muted" style="margin-bottom: 20px;">Stress test your financial resilience against inflation and major life events.</p>
                """, unsafe_allow_html=True)
                
                # Fetch defaults
                rep = st.session_state.get('report') or {}
                def_sav = rep.get('sav', 0)
                def_inc = rep.get('inc', 0)
                def_exp = rep.get('exp', 0)
                def_monthly = max(0, def_inc - def_exp)
                
                with st.form("stress_tester_form"):
                    sc1, sc2 = st.columns(2)
                    init_sav = sc1.number_input("Initial Savings (PKR)", min_value=0, value=int(def_sav), step=10000)
                    monthly_cont = sc2.number_input("Monthly Contribution (PKR)", min_value=0, value=int(def_monthly), step=5000)
                    
                    sc3, sc4 = st.columns(2)
                    ret_rate = sc3.slider("Expected Annual Return (%)", 1.0, 20.0, 12.0, step=0.5)
                    inf_rate = sc4.slider("Expected Inflation Rate (%)", 0.0, 20.0, 8.0, step=0.5)
                    
                    life_events = [
                        'None',
                        'Buy a Car in Year 3 (-1,500,000 PKR)',
                        'Medical Emergency in Year 5 (-500,000 PKR)',
                        'Job Loss in Year 7 (0 PKR contribution for 12 months)'
                    ]
                    selected_event = st.selectbox("Major Life Event", life_events)
                    
                    run_sim = st.form_submit_button("Run Simulation", type="primary", use_container_width=True)
                    
                if run_sim:
                    months = 120
                    ideal_wealth = []
                    real_wealth = []
                    
                    curr_ideal = init_sav
                    curr_real = init_sav
                    
                    ideal_monthly_rate = (ret_rate / 100.0) / 12.0
                    net_annual_rate = (ret_rate - inf_rate) / 100.0
                    real_monthly_rate = net_annual_rate / 12.0
                    
                    for m in range(1, months + 1):
                        # Ideal Growth
                        curr_ideal = curr_ideal * (1 + ideal_monthly_rate) + monthly_cont
                        
                        # Real Growth (with events)
                        current_monthly_cont = monthly_cont
                        
                        if selected_event == 'Job Loss in Year 7 (0 PKR contribution for 12 months)':
                            if 73 <= m <= 84:  # Year 7 is months 73-84
                                current_monthly_cont = 0
                                
                        curr_real = curr_real * (1 + real_monthly_rate) + current_monthly_cont
                        
                        if m == 36 and selected_event == 'Buy a Car in Year 3 (-1,500,000 PKR)':
                            curr_real -= 1500000
                        if m == 60 and selected_event == 'Medical Emergency in Year 5 (-500,000 PKR)':
                            curr_real -= 500000
                            
                        ideal_wealth.append(curr_ideal)
                        real_wealth.append(curr_real)
                        
                    # Visualization
                    df_sim = pd.DataFrame({
                        'Month': list(range(1, months + 1)),
                        'Ideal Growth': ideal_wealth,
                        'Real Purchasing Power': real_wealth
                    })
                    
                    fig_sim = px.area(
                        df_sim, 
                        x='Month', 
                        y=['Ideal Growth', 'Real Purchasing Power'],
                        color_discrete_sequence=[COLOR_INCOME, COLOR_EXPENSE]
                    )
                    
                    fig_sim.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='#a3a3a3'),
                        legend=dict(
                            orientation='h', 
                            yanchor='bottom', 
                            y=-0.2, 
                            xanchor='center', 
                            x=0.5,
                            title=None
                        ),
                        margin=dict(t=30, b=0, l=0, r=0)
                    )
                    fig_sim.update_xaxes(showgrid=False)
                    fig_sim.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.plotly_chart(fig_sim, use_container_width=True)
                    
                    # Metric Cards
                    mc1, mc2 = st.columns(2)
                    with mc1:
                        st.markdown(f"""
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <p style="color: #a3a3a3; margin:0; font-size: 0.85rem; text-transform: uppercase; font-weight:600;">Ideal 10-Year Wealth</p>
                            <h2 style="color: {COLOR_INCOME}; margin: 10px 0; font-weight:800;">PKR {ideal_wealth[-1]:,.0f}</h2>
                        </div>
                        """, unsafe_allow_html=True)
                    with mc2:
                        st.markdown(f"""
                        <div class="saas-card" style="text-align: center; height: 100%;">
                            <p style="color: #a3a3a3; margin:0; font-size: 0.85rem; text-transform: uppercase; font-weight:600;">Real Value (After Stress)</p>
                            <h2 style="color: {COLOR_EXPENSE}; margin: 10px 0; font-weight:800;">PKR {real_wealth[-1]:,.0f}</h2>
                        </div>
                        """, unsafe_allow_html=True)

