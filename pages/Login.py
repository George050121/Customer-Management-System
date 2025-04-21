# Login Page
import streamlit as st
from utils.db_utils import run_query, GetUsernamePasswordQuery
from utils.hashing import check_password

# -----------------------------
# Sidebar navigation design
# -----------------------------
if st.session_state.logged_in:
    # Redirect to home page
    st.switch_page('main.py')
    
else:
    st.sidebar.page_link('main.py', label='Home')
    st.sidebar.page_link('pages/Login.py', label='Login')
    st.sidebar.page_link('pages/Signup.py', label='Sign Up')

# -----------------------------
# Login page
# -----------------------------
st.title("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    results = run_query(GetUsernamePasswordQuery, (username,))
    if results:
        dbPassword = results[0]['UserPassword']
        if (check_password(password, dbPassword)):
            st.session_state["toast_message_logged_in"] = "✅ Successfully logged in!"
            st.session_state.user_info = results[0]
            st.session_state.logged_in = True
            st.switch_page('main.py')
        else:
            st.error('❌ Incorrect username or password!')
    else: 
        st.error('❌ Incorrect username or password!')
