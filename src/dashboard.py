import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
from utils import save_analysis_to_db, get_user_history, get_icon

# API URL
API_URL = "http://127.0.0.1:8000"

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
            
            # --- 🚀 CONNECTED TO BACKEND ---
            if st.button("RUN ANALYSIS", type="primary"):
                with st.spinner("Connecting to AI Engine..."):
                    try:
                        # Prepare Payload
                        payload = {
                            "income": inc, "expenses": exp, "savings": sav, 
                            "debt": dbt, "needs": needs, "wants": wants
                        }
                        
                        # CALL API
                        response = requests.post(f"{API_URL}/predict", json=payload)
                        
                        if response.status_code == 200:
                            data = response.json()
                            p_name = data['persona']
                            advice = data['advice']
                            
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
                        else:
                            st.error(f"Server Error: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")

        else:
            # --- RESULTS VIEW (Same Visuals) ---
            rep = st.session_state['report']
            col_head, col_btn = st.columns([8, 2])
            with col_head: st.subheader("Financial DNA Report")
            with col_btn: 
                if st.button("RESET"): st.session_state['report'] = None; st.rerun()

            # 1. Hero Card
            st.markdown(f"""
            <div style="background: radial-gradient(circle at top right, #1a1a1a, #000000); padding: 40px; border-radius: 24px; text-align: center; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
                <p style="color: #666; margin:0; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Identified Persona</p>
                <h1 style="font-size: 3rem; margin: 15px 0; color: white; font-weight: 800; letter-spacing: -1px;">{rep['persona']}</h1>
            </div>
            """, unsafe_allow_html=True)

            # 2. Metrics
            def metric_card(label, value, color="#fff"):
                return f"""<div class="glass-card" style="text-align:center; padding: 25px 15px;"><div style="color:#aaa; font-size:0.75rem; letter-spacing:1px;">{label}</div><div style="font-size:1.6rem; font-weight:700; color:{color}; margin-top:8px;">{value}</div></div>"""
            
            m1, m2, m3, m4 = st.columns(4)
            with m1: st.markdown(metric_card("Income", f"{rep['inc']:,}"), unsafe_allow_html=True)
            with m2: st.markdown(metric_card("Savings", f"{rep['sav']:,}", COLOR_SAVINGS), unsafe_allow_html=True)
            with m3: st.markdown(metric_card("Expenses", f"{rep['exp']:,}", COLOR_EXPENSE), unsafe_allow_html=True)
            with m4: st.markdown(metric_card("Debt", f"{rep['dbt']:,}", COLOR_DEBT), unsafe_allow_html=True)

            # 3. Charts
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### Cash Flow vs. Benchmark")
                fig_combo = go.Figure()
                fig_combo.add_trace(go.Bar(x=['Needs', 'Wants', 'Savings'], y=[rep['needs'], rep['wants'], rep['sav']], name='You', marker_color=COLOR_SAVINGS))
                fig_combo.add_trace(go.Scatter(x=['Needs', 'Wants', 'Savings'], y=[rep['inc']*0.5, rep['inc']*0.3, rep['inc']*0.2], name='Ideal Rule', mode='lines+markers', line=dict(color=COLOR_INCOME, width=3)))
                fig_combo.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Outfit"}, height=350, margin=dict(t=40, b=20, l=10, r=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_combo, use_container_width=True)
            
            with c2:
                st.markdown("##### Spending Distribution")
                fig_donut = px.pie(names=['Needs', 'Wants', 'Savings', 'Debt'], values=[rep['needs'], rep['wants'], rep['sav'], rep['dbt']], hole=0.6, color_discrete_sequence=[COLOR_IDEAL, COLOR_EXPENSE, COLOR_SAVINGS, COLOR_DEBT])
                fig_donut.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Outfit"}, height=350, margin=dict(t=40, b=20, l=10, r=10), showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.1))
                st.plotly_chart(fig_donut, use_container_width=True)

            # 4. Advice
            st.subheader("Strategic Recommendations")
            for advice in rep['advice']:
                st.markdown(f"""<div class="glass-card" style="border-left: 4px solid {COLOR_SAVINGS}; padding: 20px; margin-bottom: 15px;"><div style="display:flex; gap:10px; align-items:center;">{get_icon('bulb', COLOR_SAVINGS, 20)}<p style="margin:0; font-size: 1rem; color: #e0e0e0; line-height:1.6;">{advice}</p></div></div>""", unsafe_allow_html=True)

    # === TAB 2: HISTORY ===
    with tab_hist:
        st.markdown(f"#### {get_icon('history', '#fff')} Transaction Log", unsafe_allow_html=True)
        history_data = get_user_history(user['id'])
        if history_data:
            df_hist = pd.DataFrame(history_data, columns=['Income', 'Expense', 'Savings', 'Debt', 'Persona', 'Date'])
            st.dataframe(df_hist, use_container_width=True, hide_index=True)
            st.markdown("### Savings Trajectory")
            fig_hist = px.area(df_hist, x='Date', y='Savings', title="", color_discrete_sequence=[COLOR_SAVINGS])
            fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No history found.")