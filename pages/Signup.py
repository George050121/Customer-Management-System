import streamlit as st
from utils.db_utils import run_query, GetUsernamePasswordQuery, AddUserQuery
from utils.hashing import get_hash_password

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
# Simulated SMS sending function
# -----------------------------
def send_sms(phone_number):
    # Only simulate SMS sending prompt
    st.info(f"Simulating SMS confirmation to {phone_number}...")

# -----------------------------
# Sign Up page
# -----------------------------
st.title("Sign Up")
new_username = st.text_input("Choose Username", key="signup_username")
new_password = st.text_input("Choose Password", type="password", key="signup_password")
new_email = st.text_input("Email", key="signup_email")
new_phone = st.text_input("Phone Number", key="signup_phone")

if st.button("Sign Up"):
    if not new_email.strip():
        st.error("❌ Email is required.")
        st.stop()
    elif not new_username.strip():
        st.error("❌ Username is required.")
        st.stop()
    elif not new_password.strip():
        st.error("❌ Password is required.")
        st.stop()
        
    results = run_query(GetUsernamePasswordQuery, (new_username,))
    print(results)
    if results:
            st.error("❌ Username already exists, please choose another.")
            st.stop()
            
    # send_sms(new_phone)  # Simulate SMS confirmation
    # Hash password
    new_password = get_hash_password(new_password)

    # New users are set as Default User, pending admin approval
    addResults = run_query(AddUserQuery, 
                            (new_username, new_email, new_phone, new_password))
    if addResults:
        # Make a table in mysql that will have pending users and append them to this session state
        # DO this on home page so that it is set up by default
        st.success("✅ Registration successful! Your account is pending admin approval.")
    else:
            st.error("❌ Unable to create account, please try again.")