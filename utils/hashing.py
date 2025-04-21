import bcrypt

# Hashing the password for the first time (Used during Signup)
def get_hash_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

# Verifying the password (used during login)
def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(
        plain_text_password.encode('utf-8'), 
        hashed_password.encode('utf-8')
    )