import streamlit as st

# -----------------------------
# Sidebar navigation design
# -----------------------------
if st.session_state.logged_in:
    st.sidebar.page_link('main.py', label='Home')
    st.sidebar.page_link('pages/Employee_Portal.py', label='Employee Portal')
    if st.session_state.user_info.get("role") in ["Admin", "Super Admin"]:
        st.sidebar.page_link('pages/Admin_Panel.py', label='Admin Panel')
    if st.session_state.user_info.get("role") == "Super Admin":
        st.sidebar.page_link('pages/Super_Admin_Panel.py', label='Super Admin Panel')
# If not logged in and trying to access this page get redirected to login
else:
    st.switch_page('pages/Login.py')

# -----------------------------
# Super Admin Panel
# -----------------------------
if not st.session_state.logged_in or st.session_state.user_info.get("role") != "Super Admin":
    st.error("You do not have permission to access this page.")
else:
    st.title("Super Admin Panel")
    # Module 1: Upgrade Default Users to Admin
    st.write("### Upgrade Default Users to Admin")
    default_users = [user for user in st.session_state.users.values() if user["role"] == "Default User"]
    if "toast_message_user_upgrade" in st.session_state:
        st.toast(st.session_state["toast_message_user_upgrade"])
        del st.session_state["toast_message_user_upgrade"]
    if "toast_message_admin_demote" in st.session_state:
        st.toast(st.session_state["toast_message_admin_demote"])
        del st.session_state["toast_message_admin _demote"]
    if "toast_message_admin_removal" in st.session_state:
        st.toast(st.session_state["toast_message_admin_removal"])
        del st.session_state["toast_message_admin_removal"]
    if default_users:
        for idx, user in enumerate(default_users):
            st.write(f"**Username:** {user['username']} | **Email:** {user['email']}")
            if st.button(f"Upgrade {user['username']}", key=f"upgrade_{idx}"):
                user["role"] = "Admin" # Replace with SQL statement to change status
                st.session_state["toast_message_user_upgrade"] = f"✅ User {user['username']} has been upgraded to Admin!." 
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Default Users available for upgrade.")
    # Module 2: Display all Admin accounts with options to demote or delete
    st.write("### Admin Account Operations")
    admins = [user for user in st.session_state.users.values() if user["role"] == "Admin"]
    if admins:
        for idx, user in enumerate(admins):
            st.write(f"**Username:** {user['username']} | **Email:** {user['email']}")
            if st.button(f"Demote {user['username']}", key=f"demote_{idx}"):
                user["role"] = "Default User" # Make SQL script to change role of user
                st.session_state["toast_message_admin_demote"] = f"User {user['username']} has been demoted to Default User!"
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
            if st.button(f"Delete {user['username']}", key=f"delete_{idx}"):
                del st.session_state.users[user["username"]] # Make SQL script to delete user from database
                st.session_state["toast_message_admin_removal"] = f"User {user['username']} has been delted!!"
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Admin users available.")