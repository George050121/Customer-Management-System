import streamlit as st
from utils.db_utils import run_query

# -----------------------------
# Default / Admin User Setup
# -----------------------------

# SQL Code to get Default Users, and Admin Users
query = ''' 
        SELECT UserID, UserName, UserEmail, TypeID 
        FROM Users
        WHERE TypeID IN (%s, %s)
        '''

# SQL Code to Change Status of User to Admin
UpdateQuery = '''
        UPDATE Users
        SET TypeID = %s
        WHERE UserID = %s;
        '''

# SQL Code to Delete Admin
DeleteQuery =   '''
                DELETE FROM Users
                WHERE UserID = %s;
                '''

st.session_state.users = run_query(query, (1,2))

# -----------------------------
# Sidebar Navigation Design
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
    default_users = [user for user in st.session_state.users if user["TypeID"] == 1]
    if "toast_message_user_upgrade" in st.session_state:
        st.toast(st.session_state["toast_message_user_upgrade"])
        del st.session_state["toast_message_user_upgrade"]
    if "toast_message_admin_demote" in st.session_state:
        st.toast(st.session_state["toast_message_admin_demote"])
        del st.session_state["toast_message_admin_demote"]
    if "toast_message_admin_removal" in st.session_state:
        st.toast(st.session_state["toast_message_admin_removal"])
        del st.session_state["toast_message_admin_removal"]
    if default_users:
        for idx, user in enumerate(default_users):
            st.write(f"**Username:** {user['UserName']} | **Email:** {user['UserEmail']}")
            if st.button(f"Upgrade {user['UserName']}", key=f"upgrade_{idx}"):
                # Query to Update SQL DB with correct User Status (From Default to Admin) 
                results = run_query(UpdateQuery, (2, user['UserID']))
                if (results):
                    st.session_state["toast_message_user_upgrade"] = f"✅ User {user['UserName']} has been upgraded to Admin!" 
                else:
                    st.session_state["toast_message_user_upgrade"] = f"❌ User {user['UserName']} was not able to be upgraded to Admin!" 
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
            if st.button(f"Delete {user['UserName']}", key=f"delete_User_{idx}"):
                # Query to Delete User from the MySQL DB 
                results = run_query(DeleteQuery, (user["UserID"],))
                if (results):
                    st.session_state["toast_message_admin_removal"] = f"✅ User {user['UserName']} has been successfully deleted!"
                else:
                    st.session_state["toast_message_admin_removal"] = f"❌ User {user['UserName']} was unable to be deleted!"
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Default Users available for upgrade.")
    # Module 2: Display all Admin accounts with options to demote or delete
    st.write("### Admin Account Operations")
    admins = [user for user in st.session_state.users if user["TypeID"] == 2]
    if admins:
        for idx, user in enumerate(admins):
            st.write(f"**Username:** {user['UserName']} | **Email:** {user['UserEmail']}")
            if st.button(f"Demote {user['UserName']}", key=f"demote_{idx}"):
                # Query to Update SQL DB with correct User Status (From Admin to Default) 
                results = run_query(UpdateQuery, (1, user["UserID"]))
                if (results):
                    st.session_state["toast_message_admin_demote"] = f"✅ User {user['UserName']} has been successfully demoted to Default User!"
                else: 
                    st.session_state["toast_message_admin_demote"] = f"❌ User {user['UserName']} was not able to be demoted to Default User!"
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
            if st.button(f"Delete {user['UserName']}", key=f"delete_Admin_{idx}"):
                # Query to Delete Admin from the MySQL DB 
                results = run_query(DeleteQuery, (user["UserID"],))
                if (results):
                    st.session_state["toast_message_admin_removal"] = f"✅ User {user['UserName']} has been successfully deleted!"
                else:
                    st.session_state["toast_message_admin_removal"] = f"❌ User {user['UserName']} was unable to be deleted!"
                try:
                    st.switch_page("pages/Super_Admin_Panel.py")
                except AttributeError:
                    pass
    else:
        st.write("No Admin users available.")