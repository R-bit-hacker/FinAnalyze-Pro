import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

def show_admin_panel(user):
    # --- SECURITY GATE ---
    if user.get('role') != 'admin':
        st.error("⛔ ACCESS DENIED: This area is restricted to Administrators only.")
        return

    # --- HEADER ---
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="margin-bottom:0; font-weight:800;">Admin Console</h2>
            <p style="color:#888; font-size:0.9rem;">System Overview & User Management</p>
        </div>
        <div>
             <span style="background: #FF4560; color:white; padding: 6px 15px; border-radius:20px; font-size:0.75rem; font-weight:bold;">GOD MODE</span>
        </div>
    </div>
    <hr style="border-color: rgba(255,255,255,0.1);">
    """, unsafe_allow_html=True)
    
    # --- FETCH DATA ---
    with st.spinner("Fetching system data..."):
        try:
            res = requests.get(f"{API_URL}/get-all-users")
            if res.status_code == 200:
                users = res.json()['users']
                df = pd.DataFrame(users)
            else:
                st.error("❌ Failed to fetch users from server.")
                return
        except:
            st.error("🔌 Backend Server is Offline.")
            return

    # --- METRICS (TOP ROW) ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px;"><h3>{len(df)}</h3><p style="color:#aaa; font-size:0.8rem;">Total Users</p></div>""", unsafe_allow_html=True)
    with m2:
        admins = len(df[df['role'] == 'admin'])
        st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px; border:1px solid #00E396;"><h3>{admins}</h3><p style="color:#aaa; font-size:0.8rem;">Admins</p></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="glass-card" style="text-align:center; padding:15px; border:1px solid #00c6ff;"><h3>Active</h3><p style="color:#aaa; font-size:0.8rem;">System Status</p></div>""", unsafe_allow_html=True)

    # --- ADVANCED INTERACTIVE DATA EDITOR ---
    st.markdown("### 🗃️ Interactive User Database")
    st.caption("✨ **TIPS:** Double-click any cell to **Edit**. Select a row and press Delete/Backspace to **Remove**. Click the '+' icon at the bottom to **Add** a new user. You MUST provide a unique Username and Email.")
    
    # Form ki zaroorat nahi, data_editor apna state khud manage karta hai
    edited_df = st.data_editor(
        df[['id', 'username', 'email','name', 'role', 'phone']], 
        use_container_width=True,
        num_rows="dynamic", # Yeh naye rows add karne aur delete karne ki ijazat deta hai
        key="user_editor",
        disabled=["id"],    # ID change nahi kar sakte kyunke wo database handle karta hai
        column_config={
            "id": st.column_config.NumberColumn("ID", disabled=True),
            "role": st.column_config.SelectboxColumn(
                "Role",
                help="User Permission Level",
                width="small",
                options=["user", "admin"],
                required=True,
            ),
            "username": st.column_config.TextColumn("User ID", required=True),
            "name": st.column_config.TextColumn("Full Name"),
            "email": st.column_config.TextColumn("Email", required=True),
            "phone": st.column_config.TextColumn("Contact"),
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BATCH SAVE BUTTON ---
    if st.button("💾 Save All Changes to Database", type="primary", use_container_width=True):
        
        # Get changes from session state
        changes = st.session_state["user_editor"]
        payload = {"added": [], "edited": [], "deleted": []}

        # 1. Process Deletes
        for row_idx in changes.get("deleted_rows", []):
            user_id = int(df.iloc[row_idx]['id'])
            payload["deleted"].append(user_id)

        # 2. Process Edits
        for row_idx, edits in changes.get("edited_rows", {}).items():
            user_id = int(df.iloc[int(row_idx)]['id'])
            edit_obj = {"id": user_id}
            if "username" in edits: edit_obj["username"] = edits["username"]
            if "name" in edits: edit_obj["name"] = edits["name"]
            if "email" in edits: edit_obj["email"] = edits["email"]
            if "role" in edits: edit_obj["role"] = edits["role"]
            if "phone" in edits: edit_obj["phone"] = edits["phone"]
            payload["edited"].append(edit_obj)

        # 3. Process Adds
        for added_row in changes.get("added_rows", []):
            #username = added_row.get("username", f"user_{pd.Timestamp.now().strftime('%S%f')}")
            email = added_row.get("email")
            username = added_row.get("username")

            if not username or not email:
                st.error("⚠️ Username and Email are strictly required for new users!")
                return
            
            payload["added"].append({
                "username": username,
                "email": email,
                "name": added_row.get("name", ""),
                "role": added_row.get("role", "user"),
                "phone": added_row.get("phone", "")
            })

        # Send API Request if there are any changes
        if payload["added"] or payload["edited"] or payload["deleted"]:
            with st.spinner("Applying changes securely..."):
                try:
                    resp = requests.post(f"{API_URL}/batch-update-users", json=payload)
                    if resp.status_code == 200:
                        st.success("""✅ **User Successfully Added to Database!** 🔑 **Action Required:** Please notify the user manually (via email or chat) that their account is active. 👉 Their default password is **123456**. Advise them to update it from the 'Edit Profile' section upon first login for security reasons.""")
                        st.rerun() # Refresh to show new IDs and clean data
                    else:
                        err = resp.json().get('detail', 'Unknown error')
                        st.error(f"❌ Operation Failed: {err}")
                except Exception as e:
                    st.error(f"🔌 Connection Error: {e}")
        else:
            st.info("ℹ️ No changes were made to save.")