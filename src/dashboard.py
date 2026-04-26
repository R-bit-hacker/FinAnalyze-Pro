import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import numpy as np
# Direct ML import
from ml_logic import load_models, get_ai_advice
from utils import save_analysis_to_db, get_user_history, get_icon 

def show_dashboard(user):
    # Header
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="margin-bottom:0; font-weight:800;">Analysis Hub</h2>
            <p style="color:#888; font-size:0.9rem;">Overview for <b>{user['name']}</b></p>
        </div>
        <div style="text-align:right;">
             <span style="background: linear-gradient(90deg, #00c6ff, #0072ff); color:white; padding: 6px 15px; border-radius:20px; font-size:0.75rem; font-weight:bold;">PRO PLAN</span>
        </div>
    </div>
    <hr style="border-color: rgba(255,255,255,0.1);">
    """, unsafe_allow_html=True)
    
    # Colors
    COLOR_INCOME = "#00E396"
    COLOR_EXPENSE = "#FF4560"
    COLOR_SAVINGS = "#775DD0"
    COLOR_DEBT = "#FEB019"
    COLOR_IDEAL = "#008FFB"

    tab_new, tab_hist = st.tabs(["New Analysis", "History Log"])

    # === TAB 1: NEW ANALYSIS ===
    with tab_new:
        if st.session_state.get('report') is None:
            st.markdown(f"#### {get_icon('edit', '#fff')} Enter Financial Data", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            inc = c1.number_input("Monthly Income (PKR)", 0, 10000000, 100000, step=5000)
            exp = c2.number_input("Monthly Expenses (PKR)", 0, 10000000, 50000, step=5000)
            
            c3, c4 = st.columns(2)
            sav = c3.number_input("Total Savings (PKR)", 0, 10000000, 20000, step=5000)
            dbt = c4.number_input("Outstanding Debt (PKR)", 0, 10000000, 0, step=5000)
            
            st.markdown("<br><p style='color:#ccc;'>Spending Breakdown</p>", unsafe_allow_html=True)
            needs = st.slider("Essentials (Rent, Food, Bills)", 0, int(inc) if inc>0 else 100000, int(inc*0.5))
            wants = st.slider("Lifestyle (Shopping, Outings)", 0, int(inc) if inc>0 else 100000, int(inc*0.3))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- 🚀 DIRECT ML ANALYSIS (FIXED) ---
            # --- 🚀 DIRECT ML ANALYSIS (FIXED) ---
            if st.button("RUN ANALYSIS", type="primary"):
                with st.spinner("AI Engine is analyzing your data..."):
                    try:
                        # 1. Load Models
                        kmeans, scaler, pca = load_models()
                        
                        if kmeans is None or scaler is None:
                            st.error("AI Models not found.")
                        else:
                            # 2. Calculate Missing Ratios (Training data ke format ke mutabiq)
                            savings_rate = sav / inc if inc > 0 else 0
                            debt_to_income_ratio = dbt / inc if inc > 0 else 0
                            expense_ratio = exp / inc if inc > 0 else 0
                            lifestyle_ratio = wants / (needs + 1)

                            # 3. Prepare Data for Prediction (Exact 10 features in correct order)
                            features = np.array([[
                                inc,                  # monthly_income
                                exp,                  # monthly_expense_total
                                savings_rate,         # savings_rate
                                debt_to_income_ratio, # debt_to_income_ratio
                                wants,                # discretionary_spending (wants)
                                needs,                # essential_spending (needs)
                                0,                    # investment_amount
                                0,                    # transaction_count
                                expense_ratio,        # expense_ratio
                                lifestyle_ratio       # lifestyle_ratio
                            ]])
                            
                            # 4. Scaling
                            scaled_data = scaler.transform(features)
                            
                            # 🚨 5. FIX: Predict on scaled_data (10 features), NOT pca_data
                            cluster = int(kmeans.predict(scaled_data)[0])
                            
                            # Cluster to Persona Mapping
                            # Cluster to Persona Mapping
                            persona_map = {
                                0: "Budget Challenger",
                                1: "Big Spender",
                                2: "Wealth Builder",
                                3: "Smart Saver"
                            }
                            p_name = persona_map.get(cluster, "Balanced Spender")

                            if cluster == 2 and expense_ratio >= 0.80:
                                p_name = "Big Spender"
                            
                            # Get AI Advice
                            advice = get_ai_advice(p_name, inc, sav)
                            
                            # Save to Local DB (History)
                            save_analysis_to_db(user['id'], inc, exp, sav, dbt, p_name)

                            # Update State
                            st.session_state['report'] = {
                                'inc': inc, 'exp': exp, 'sav': sav, 'dbt': dbt, 
                                'persona': p_name, 'needs': needs, 'wants': wants, 
                                'advice': advice
                            }
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"Analysis failed: {str(e)}")

        else:
            # --- RESULTS VIEW (No changes here, remains working) ---
            rep = st.session_state['report']
            col_head, col_btn = st.columns([8, 2])
            with col_head: st.subheader("Financial DNA Report")
            with col_btn: 
                if st.button("RESET"): st.session_state['report'] = None; st.rerun()

            # Hero Card
            st.markdown(f"""
            <div style="background: radial-gradient(circle at top right, #1a1a1a, #000000); padding: 40px; border-radius: 24px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;">
                <p style="color: #666; margin:0; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Identified Persona</p>
                <h1 style="font-size: 3rem; margin: 15px 0; color: white; font-weight: 800; letter-spacing: -1px;">{rep['persona']}</h1>
            </div>
            """, unsafe_allow_html=True)

            # Metrics display (Glass Cards Styling)
            m1, m2, m3, m4 = st.columns(4)
            
            # Helper function to generate identical glass cards
            def metric_card(title, value, color="white"):
                return f"""
                <div class="glass-card" style="text-align:center; padding: 25px 15px; display: flex; flex-direction: column; justify-content: center; height: 100%;">
                    <p style="color:#888; font-size:0.85rem; margin-bottom:10px; text-transform: uppercase; letter-spacing: 1px;">{title}</p>
                    <h2 style="color:{color}; margin:0; font-weight: 700; font-size: 1.8rem;">{value:,}</h2>
                </div>
                """

            with m1: st.markdown(metric_card("Income", rep['inc'], "white"), unsafe_allow_html=True)
            with m2: st.markdown(metric_card("Savings", rep['sav'], COLOR_SAVINGS), unsafe_allow_html=True)
            with m3: st.markdown(metric_card("Expenses", rep['exp'], COLOR_EXPENSE), unsafe_allow_html=True)
            with m4: st.markdown(metric_card("Debt", rep['dbt'], COLOR_DEBT), unsafe_allow_html=True)

            # Charts and Advice display (Functionality preserved)
            c1, c2 = st.columns(2)
            with c1:
                fig_combo = go.Figure()
                fig_combo.add_trace(go.Bar(x=['Needs', 'Wants', 'Savings'], y=[rep['needs'], rep['wants'], rep['sav']], name='You', marker_color=COLOR_SAVINGS))
                st.plotly_chart(fig_combo, use_container_width=True)
            
            with c2:
                fig_donut = px.pie(names=['Needs', 'Wants', 'Savings', 'Debt'], values=[rep['needs'], rep['wants'], rep['sav'], rep['dbt']], hole=0.6)
                st.plotly_chart(fig_donut, use_container_width=True)

            st.markdown("<h3 style='margin-top: 30px; margin-bottom: 20px;'>Strategic Recommendations</h3>", unsafe_allow_html=True)
            for advice in rep['advice']:
                # Custom Glass Card for Recommendations (Matching Image 2)
                st.markdown(f"""
                <div style="background: rgba(20, 20, 30, 0.6); border: 1px solid rgba(119, 93, 208, 0.3); border-radius: 15px; padding: 18px 25px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); transition: transform 0.2s;">
                    <div style="display: flex; align-items: center; justify-content: center; opacity: 0.9;">
                        {get_icon('bulb', COLOR_SAVINGS, 22)}
                    </div>
                    <div style="color: #e0e0e0; font-size: 0.95rem; font-weight: 300; letter-spacing: 0.3px;">
                        {advice}
                    </div>
                </div>
                """, unsafe_allow_html=True)

   # === TAB 2: HISTORY ===
    with tab_hist:
        history_data = get_user_history(user['id'])
        if history_data:
            # Dataframe banayein
            df_hist = pd.DataFrame(history_data, columns=['Income', 'Expense', 'Savings', 'Debt', 'Persona', 'Date'])
            
            # 1. Date ko proper time format mein convert karein aur sort karein taake chart theek se bane
            df_hist['Date'] = pd.to_datetime(df_hist['Date'])
            df_hist = df_hist.sort_values(by='Date')

            # 2. Pehle Table show karein
            st.markdown("### 🕒 Transaction Log")
            st.dataframe(df_hist, use_container_width=True, hide_index=True)

            # 3. Phir "Savings Trajectory" Chart banayein
            st.markdown("<br>### 📈 Savings Trajectory", unsafe_allow_html=True)
            
            # Plotly Express Area Chart
            fig_trajectory = px.area(
                df_hist, 
                x='Date', 
                y='Savings', 
                markers=True,
                color_discrete_sequence=[COLOR_SAVINGS] # Purple color jo aapki theme ka hissa hai
            )
            
            # Chart ko Dark Theme ke hisaab se style karein (jaise aapki image mein hai)
            fig_trajectory.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#aaa'),
                xaxis_title="Date",
                yaxis_title="Savings",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            fig_trajectory.update_xaxes(showgrid=False)
            fig_trajectory.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            
            # Chart ko Streamlit par render karein
            st.plotly_chart(fig_trajectory, use_container_width=True)
            
        else:
            st.info("No history found.")