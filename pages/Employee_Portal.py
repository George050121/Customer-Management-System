import streamlit as st
from utils.db_utils import run_query, query, DeleteQuery, UpdateQuery

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
# Employee Portal (button layout demonstration only, no search function implemented)
# -----------------------------

st.title('Employee Portal')

if not st.session_state.logged_in:
    st.error("Please log in to access the Employee Portal.")
else:
    st.title("Employee Portal")
    st.write("This page is for employee operations (e.g., search). Currently, it only demonstrates button layout.")
    if st.button("Employee Operation Example Button"):
        st.info("Button clicked, but functionality not yet implemented.")