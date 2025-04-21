import streamlit as st
from utils.db_utils import run_query, query, DeleteQuery, UpdateQuery

# -----------------------------
# Registered User Setup
# -----------------------------
st.session_state.users = run_query(query, (4,1))

# -----------------------------
# Sidebar navigation design
# -----------------------------
if st.session_state.logged_in:
    st.sidebar.page_link('main.py', label='Home')
    st.sidebar.page_link('pages/Employee_Portal.py', label='Employee Portal')
    if st.session_state.user_info.get("TypeID") in [2, 3]:
        st.sidebar.page_link('pages/Admin_Panel.py', label='Admin Panel')
    if st.session_state.user_info.get("TypeID") == 3:
        st.sidebar.page_link('pages/Super_Admin_Panel.py', label='Super Admin Panel')
# If not logged in and trying to access this page get redirected to login
else:
    st.switch_page('pages/Login.py')

# -----------------------------
# Admin Panel
# -----------------------------
st.title('Admin Panel')

if not st.session_state.logged_in or st.session_state.user_info.get("TypeID") not in [2, 3]:
    st.error("You do not have permission to access this page.")
else:
    # Pop up messages when users are approved or removed
    st.write("### Pending Registration Approvals")
    pending_users = [user for user in st.session_state.users if user["TypeID"] == 4]
    if "toast_message_user_approval" in st.session_state:
        st.toast(st.session_state["toast_message_user_approval"])
        del st.session_state["toast_message_user_approval"]
    if "toast_message_user_removal" in st.session_state:
        st.toast(st.session_state["toast_message_user_removal"])
        del st.session_state["toast_message_user_removal"]
    # Module: Pending Registration Approvals
    if pending_users:
        for idx, pending in enumerate(pending_users):
            st.write(f"**Username:** {pending['UserName']} | **Email:** {pending['UserEmail']} | **Phone Number:** {pending['PhoneNumber']}")
            if st.button(f"Approve {pending['UserName']}", key=f"approve_{idx}"):
                results = run_query(UpdateQuery, (1, pending['UserID']))
                if (results):
                    st.session_state["toast_message_user_approval"] = f"✅ User {pending['UserName']} has been approved!"
                else:
                    st.session_state["toast_message_user_approval"] = f"❌ User {pending['UserName']} was not able to be approved!"
                try:
                    st.rerun()
                except AttributeError:
                    pass
            if st.button(f"Deny {pending['UserName']}", key=f"deny_{idx}"):
                results = run_query(DeleteQuery, (pending['UserID'],))
                if (results):
                    st.session_state["toast_message_user_approval"] = f"✅ User {pending['UserName']} successfully denied!"
                else:
                    st.session_state["toast_message_user_approval"] = f"❌ User {pending['UserName']} was not able to be denied!"
                try:
                    st.rerun()
                except AttributeError:
                    pass
    else:
        st.write("No pending users.")
    # New Module: Display all Default Users with option to delete account
    st.write("### Approved Default User Accounts")
    default_users = [user for user in st.session_state.users if user["TypeID"] == 1]
    if default_users:
        for idx, user in enumerate(default_users):
            st.write(f"**Username:** {user['UserName']} | **Email:** {user['UserEmail']}")
            if st.button(f"Delete Account {user['UserName']}", key=f"delete_default_{idx}"):
                results = run_query(DeleteQuery, (user["UserID"],))
                if results:
                    st.session_state["toast_message_user_removal"] = f"✅ User {user['UserName']} was successfully deleted!"
                else:
                    st.session_state["toast_message_user_removal"] = f"❌ User {user['UserName']} was unable to be deleted!"
                try:
                    st.switch_page("pages/Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Default Users available.")