# Login Page
import streamlit as st

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
    user = st.session_state.users.get(username)
    if user and user["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user_info = user
        # Display message that will tell the user they logged in on home page
        st.session_state["toast_message_logged_in"] = "✅ Successfully logged in!"
        st.switch_page('main.py')
    else:
        st.error("Incorrect username or password.")
