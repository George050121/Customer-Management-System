# 1_home.py
import streamlit as st

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

# -----------------------------
# Simulated SMS sending function
# -----------------------------
def send_sms(phone_number):
    # Only simulate SMS sending prompt
    st.info(f"Simulating SMS confirmation to {phone_number}...")

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
# Sidebar navigation design
# -----------------------------
st.sidebar.title("Navigation")
pages = ["Home", "Login", "Sign Up", "Employee Portal"]
if st.session_state.logged_in:
    if st.session_state.user_info.get("role") in ["Admin", "Super Admin"]:
        pages.append("Admin Panel")
    if st.session_state.user_info.get("role") == "Super Admin":
        pages.append("Super Admin Panel")
page = st.sidebar.radio("Navigate to", pages)

# -----------------------------
# Home page
# -----------------------------
if page == "Home":
    st.title("Welcome to the Company Portal")
    if st.session_state.logged_in:
        st.write(f"Current logged in user: **{st.session_state.user_info.get('username', '')}** "
                 f"({st.session_state.user_info.get('role', '')})")
        if st.button("Logout"):
            logout()
    else:
        st.write("Please use the sidebar to login or sign up.")

# -----------------------------
# Login page
# -----------------------------
elif page == "Login":
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = st.session_state.users.get(username)
        if user and user["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user_info = user
            st.success("Login successful!")
        else:
            st.error("Incorrect username or password.")

# -----------------------------
# Sign Up page
# -----------------------------
elif page == "Sign Up":
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
            st.session_state.pending_users.append(new_user)
            st.success("Registration successful! Your account is pending admin approval.")

# -----------------------------
# Employee Portal (button layout demonstration only, no search function implemented)
# -----------------------------
elif page == "Employee Portal":
    if not st.session_state.logged_in:
        st.error("Please log in to access the Employee Portal.")
    else:
        st.title("Employee Portal")
        st.write("This page is for employee operations (e.g., search). Currently, it only demonstrates button layout.")
        if st.button("Employee Operation Example Button"):
            st.info("Button clicked, but functionality not yet implemented.")

# -----------------------------
# Admin Panel
# -----------------------------
elif page == "Admin Panel":
    if not st.session_state.logged_in or st.session_state.user_info.get("role") not in ["Admin", "Super Admin"]:
        st.error("You do not have permission to access this page.")
    else:
        st.title("Admin Panel")
        # Module: Pending Registration Approvals
        st.write("### Pending Registration Approvals")
        if st.session_state.pending_users:
            for idx, pending in enumerate(st.session_state.pending_users):
                st.write(f"**Username:** {pending['username']} | **Email:** {pending['email']} | **Phone Number:** {pending['phone']}")
                if st.button(f"Approve {pending['username']}", key=f"approve_{idx}"):
                    st.session_state.users[pending["username"]] = pending
                    st.success(f"User {pending['username']} has been approved!")
                    st.session_state.pending_users.pop(idx)
                    try:
                        st.experimental_rerun()
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
                    st.success(f"User {user['username']} has been deleted!")
                    try:
                        st.experimental_rerun()
                    except AttributeError:
                        pass
        else:
            st.write("No Default Users available.")

# -----------------------------
# Super Admin Panel
# -----------------------------
elif page == "Super Admin Panel":
    if not st.session_state.logged_in or st.session_state.user_info.get("role") != "Super Admin":
        st.error("You do not have permission to access this page.")
    else:
        st.title("Super Admin Panel")
        # Module 1: Upgrade Default Users to Admin
        st.write("### Upgrade Default Users to Admin")
        default_users = [user for user in st.session_state.users.values() if user["role"] == "Default User"]
        if default_users:
            for idx, user in enumerate(default_users):
                st.write(f"**Username:** {user['username']} | **Email:** {user['email']}")
                if st.button(f"Upgrade {user['username']}", key=f"upgrade_{idx}"):
                    user["role"] = "Admin"
                    st.success(f"User {user['username']} has been upgraded to Admin!")
                    try:
                        st.experimental_rerun()
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
                    user["role"] = "Default User"
                    st.success(f"User {user['username']} has been demoted to Default User!")
                    try:
                        st.experimental_rerun()
                    except AttributeError:
                        pass
                if st.button(f"Delete {user['username']}", key=f"delete_{idx}"):
                    del st.session_state.users[user["username"]]
                    st.success(f"User {user['username']} has been deleted!")
                    try:
                        st.experimental_rerun()
                    except AttributeError:
                        pass
        else:
            st.write("No Admin users available.")