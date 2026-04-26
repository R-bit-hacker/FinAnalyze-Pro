import streamlit as st
import os
import base64
from utils import show_footer, get_icon, scroll_to_top

def get_img_as_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return ""

def show_about_page():
    # --- AUTO SCROLL TO TOP ---
    scroll_to_top()

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 1s;">
        <h1 class="gradient-text" style="font-size: 3.5rem;">Our Mission</h1>
        <p style="color: #888; font-size: 1.2rem; max-width: 700px; margin: 0 auto;">
            To democratize financial intelligence for the Gen-Z population of Pakistan using cutting-edge AI.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="glass-card" style="height: 250px;">
            <div style="margin-bottom: 15px;">{get_icon('target', '#00f260')}</div>
            <h3 style="color: white;">The Goal</h3>
            <p style="color: #aaa; line-height: 1.6;">
                Financial literacy is rare. We aim to change that by providing a tool that doesn't just track expenses, but understands behavior.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="height: 250px;">
            <div style="margin-bottom: 15px;">{get_icon('chart', '#00c6ff')}</div>
            <h3 style="color: white;">The Technology</h3>
            <p style="color: #aaa; line-height: 1.6;">
                Built on Python, FastAPI, and Scikit-Learn. We use K-Means clustering to benchmark user data against realistic financial profiles.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center; margin-top: 50px;'>The Minds Behind</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    my_pic = os.path.join(base_dir, "data", "me.jpg")
    ayesha_pic = os.path.join(base_dir, "data", "ayesha.jpg")

    img_src_me = f"data:image/jpeg;base64,{get_img_as_base64(my_pic)}" if os.path.exists(my_pic) else "https://cdn-icons-png.flaticon.com/512/4140/4140048.png"
    img_src_ayesha = f"data:image/jpeg;base64,{get_img_as_base64(ayesha_pic)}" if os.path.exists(ayesha_pic) else "https://cdn-icons-png.flaticon.com/512/4140/4140037.png"

    t1, t2 = st.columns(2)
    
    with t1:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 20px;">
            <img src="{img_src_me}" width="120" height="120" style="border-radius: 50%; border: 3px solid #6a11cb; margin-bottom: 15px; object-fit: cover;">
            <h3 style="margin: 0; color: #fff;">Rubaisha Munir</h3>
            <p style="color: #00c6ff; font-weight: bold;">Lead Developer</p>
            <p style="font-size: 0.9rem; color: #ccc;">Full Stack Architecture & AI</p>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 20px;">
            <img src="{img_src_ayesha}" width="120" height="120" style="border-radius: 50%; border: 3px solid #6a11cb; margin-bottom: 15px; object-fit: cover;">
            <h3 style="margin: 0; color: #fff;">Ayesha Nadeem</h3>
            <p style="color: #fff; font-weight: bold;">Data Analyst</p>
            <p style="font-size: 0.9rem; color: #ccc;">Dataset Curation & Research</p>
        </div>
        """, unsafe_allow_html=True)

    show_footer()