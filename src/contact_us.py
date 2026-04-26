import streamlit as st
from utils import show_footer, get_icon, scroll_to_top

def show_contact_page():
    # --- AUTO SCROLL TO TOP ---
    scroll_to_top()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 1.5], gap="large")
    
    with c1:
        st.markdown('<h1 class="gradient-text">Get in Touch</h1>', unsafe_allow_html=True)
        st.markdown("<p style='color:#aaa; font-size:1.1rem;'>Have questions or found a bug? We are here to help.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Corrected Indentation string
        html_card = f"""
<div class="glass-card" style="padding: 30px;">
    <div style="display:flex; align-items:center; gap: 20px; margin-bottom: 30px;">
        {get_icon('mail', '#00c6ff', 28)}
        <div>
            <div style="font-size: 0.8rem; color: #666; letter-spacing: 1px; font-weight: 600;">EMAIL US</div>
            <div style="color: white; font-size: 1.1rem;">rubaisha1705@gmail.com</div>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap: 20px;">
        {get_icon('phone', '#00c6ff', 28)}
        <div>
            <div style="font-size: 0.8rem; color: #666; letter-spacing: 1px; font-weight: 600;">CALL US</div>
            <div style="color: white; font-size: 1.1rem;">0309-0139836</div>
        </div>
    </div>
</div>
"""
        st.markdown(html_card, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"<h3 style='margin-bottom: 20px;'>{get_icon('edit', '#fff')} Send a Message</h3>", unsafe_allow_html=True)
        with st.form("contact_form", clear_on_submit=True):
            st.text_input("Name", placeholder="Your Name")
            st.text_input("Email", placeholder="john@example.com")
            st.text_area("Message", placeholder="How can we help you?", height=150)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.form_submit_button("SEND MESSAGE", use_container_width=True):
                st.toast("Message sent successfully!", icon="✅")

    st.markdown("<br><br><h3 style='text-align:center;'>Our Locations</h3><br>", unsafe_allow_html=True)
    o1, o2, o3 = st.columns(3)
    
    def office_card(city, address):
        return f"""<div class="glass-card" style="text-align:center; padding: 20px;"><h4 style="color:white; margin:0;">{city}</h4><p style="font-size:0.9rem; color:#aaa; margin-top: 10px;">{address}</p></div>"""

    with o1: st.markdown(office_card("Lahore - HQ", "3rd Floor, Arfa Tower"), unsafe_allow_html=True)
    with o2: st.markdown(office_card("Islamabad", "NSTP, NUST H-12 Campus"), unsafe_allow_html=True)
    with o3: st.markdown(office_card("Karachi", "Regus, Bahria Complex III"), unsafe_allow_html=True)

    show_footer()