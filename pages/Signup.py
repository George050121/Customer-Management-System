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
    if new_username in st.session_state.users:
        st.error("Username already exists, please choose another.")
    else:
        send_sms(new_phone)  # Simulate SMS confirmation
        # New users are set as Default User, pending admin approval
        new_user = {
            "username": new_username,
            "password": new_password,
            "email": new_email,
            "phone": new_phone,
            "role": "Default User",
        }
        # Make a table in mysql that will have pending users and append them to this session state
        # DO this on home page so that it is set up by default
        st.session_state.pending_users.append(new_user)
        st.success("Registration successful! Your account is pending admin approval.")