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
# Admin Panel
# -----------------------------
st.title('Admin Panel')

if not st.session_state.logged_in or st.session_state.user_info.get("role") not in ["Admin", "Super Admin"]:
    st.error("You do not have permission to access this page.")
else:
    # Pop up messages when users are approved or removed
    st.write("### Pending Registration Approvals")
    if "toast_message_user_approval" in st.session_state:
        st.toast(st.session_state["toast_message_user_approval"])
        del st.session_state["toast_message_user_approval"]
    if "toast_message_user_removal" in st.session_state:
        st.toast(st.session_state["toast_message_user_removal"])
        del st.session_state["toast_message_user_removal"]
    # Module: Pending Registration Approvals
    if st.session_state.pending_users:
        for idx, pending in enumerate(st.session_state.pending_users):
            st.write(f"**Username:** {pending['username']} | **Email:** {pending['email']} | **Phone Number:** {pending['phone']}")
            if st.button(f"Approve {pending['username']}", key=f"approve_{idx}"):
                st.session_state.users[pending["username"]] = pending
                st.session_state.pending_users.pop(idx)
                st.session_state["toast_message_user_approval"] = f"✅ User {pending['username']} has been approved!"
                try:
                    st.rerun()
                except AttributeError:
                    pass
    else:
        st.write("No pending users.")
    # New Module: Display all Default Users with option to delete account
    st.write("### Approved Default User Accounts")
    default_users = [user for user in st.session_state.users.values() if user["role"] == "Default User"]
    if default_users:
        for idx, user in enumerate(default_users):
            st.write(f"**Username:** {user['username']} | **Email:** {user['email']}")
            if st.button(f"Delete Account {user['username']}", key=f"delete_default_{idx}"):
                del st.session_state.users[user["username"]]
                st.session_state["toast_message_user_removal"] = f"❌ User {user['username']} has been deleted!"
                try:
                    st.switch_page("pages/Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Default Users available.")