import streamlit as st

st.set_page_config(
    page_title="Home Page"
)

# -----------------------------
# Initialize session_state variables
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "users" not in st.session_state:
    # Simulate preset accounts (Super Admin and Admin)
    st.session_state.users = {
        "superadmin": {
            "username": "superadmin",
            "password": "password",
            "email": "superadmin@example.com",
            "phone": "1234567890",
            "role": "Super Admin",
        },
        "admin": {
            "username": "admin",
            "password": "admin",
            "email": "admin@example.com",
            "phone": "1234567891",
            "role": "Admin",
        },
    }
if "pending_users" not in st.session_state:
    st.session_state.pending_users = []
if "employees" not in st.session_state:
    # Although the search function is not implemented, pre-define some employee data
    st.session_state.employees = [
        {"name": "John Doe", "email": "johndoe@example.com", "phone": "1112223333"},
        {"name": "Jane Smith", "email": "janesmith@example.com", "phone": "4445556666"},
    ]

st.title("Welcome to the Company Portal")

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
else:
    st.sidebar.page_link('main.py', label='Home')
    st.sidebar.page_link('pages/Login.py', label='Login')
    st.sidebar.page_link('pages/Signup.py', label='Sign Up')

# -----------------------------
# Logout function: only logs out, does not delete account
# -----------------------------
def logout():
    st.session_state.logged_in = False
    st.session_state.user_info = {}
    st.success("Successfully logged out!")
    try:
        st.experimental_rerun()
    except AttributeError:
        pass

# -----------------------------
# Home page
# -----------------------------
if st.session_state.logged_in:
    st.write(f"Current logged in user: **{st.session_state.user_info.get('UserName',)}** "
                f"({st.session_state.user_info.get('role', '')})")
    if "toast_message_logged_in" in st.session_state:
        st.toast(st.session_state["toast_message_logged_in"])
        del st.session_state["toast_message_logged_in"] # Remove the saved message to not be used when not needed
    if st.button("Logout"):
        logout()
        st.session_state["toast_message_logged_out"] = "Successfully logged out"
        st.switch_page('main.py')
else:
    if "toast_message_logged_out" in st.session_state:
        st.toast(st.session_state["toast_message_logged_out"])
        del st.session_state["toast_message_logged_out"] # Remove the saved message to not be used when not needed
    st.write("Please use the sidebar to login or sign up.")