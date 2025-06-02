from src import bcrypt

def generate_pw_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_pw_hash(password, hash):
    return bcrypt.check_password_hash(hash, password)
