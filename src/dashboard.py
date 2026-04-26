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
            if st.button("RUN ANALYSIS", type="primary"):
                with st.spinner("AI Engine is analyzing your data..."):
                    try:
                        # 1. Load Models
                        kmeans, scaler, pca = load_models()
                        
                        if kmeans is None:
                            st.error("Could not load AI models. Please check your models folder.")
                        else:
                            # 2. Prepare Data for Prediction
                            # Humein wahi features dene hain jo model training ke waqt diye thay
                            # Based on your input: inc, exp, sav, dbt, needs, wants
                            input_data = np.array([[inc, exp, sav, dbt, needs, wants]])
                            
                            # Scaling and PCA
                            scaled_data = scaler.transform(input_data)
                            pca_data = pca.transform(scaled_data)
                            
                            # Prediction
                            cluster = kmeans.predict(pca_data)[0]
                            
                            # Cluster to Persona Mapping (Standard for FinAnalyze)
                            persona_map = {0: "Smart Saver", 1: "Wealth Builder", 2: "Big Spender", 3: "Budget Challenger"}
                            p_name = persona_map.get(cluster, "Balanced Spender")
                            
                            # Get AI Advice
                            advice = get_ai_advice(p_name, inc, sav)
                            
                            # Save to Local DB (History)
                            save_analysis_to_db(user['id'], inc, exp, sav, dbt, p_name)
                            st.toast("Analysis Complete!")

                            # Update State
                            st.session_state['report'] = {
                                'inc': inc, 'exp': exp, 'sav': sav, 'dbt': dbt, 
                                'persona': p_name, 'needs': needs, 'wants': wants, 
                                'advice': advice
                            }
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"Analysis Failed: {e}")

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

            # Metrics display
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.metric("Income", f"{rep['inc']:,}")
            with m2: st.metric("Savings", f"{rep['sav']:,}")
            with m3: st.metric("Expenses", f"{rep['exp']:,}")
            with m4: st.metric("Debt", f"{rep['dbt']:,}")

            # Charts and Advice display (Functionality preserved)
            c1, c2 = st.columns(2)
            with c1:
                fig_combo = go.Figure()
                fig_combo.add_trace(go.Bar(x=['Needs', 'Wants', 'Savings'], y=[rep['needs'], rep['wants'], rep['sav']], name='You', marker_color=COLOR_SAVINGS))
                st.plotly_chart(fig_combo, use_container_width=True)
            
            with c2:
                fig_donut = px.pie(names=['Needs', 'Wants', 'Savings', 'Debt'], values=[rep['needs'], rep['wants'], rep['sav'], rep['dbt']], hole=0.6)
                st.plotly_chart(fig_donut, use_container_width=True)

            st.subheader("Strategic Recommendations")
            for advice in rep['advice']:
                st.info(advice)

    # === TAB 2: HISTORY ===
    with tab_hist:
        history_data = get_user_history(user['id'])
        if history_data:
            df_hist = pd.DataFrame(history_data, columns=['Income', 'Expense', 'Savings', 'Debt', 'Persona', 'Date'])
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
        else:
            st.info("No history found.")