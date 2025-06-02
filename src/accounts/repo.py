from src import app, db
from src.models import User
from src.utils import check_pw_hash
from flask_login import login_user, logout_user


def register(first_name: str, last_name: str, phone: str, password: str) -> None:
    if User.query.filter_by(phone=phone).first():
        raise ValueError("Phone number already registered")

    user = User(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        password=password
    )
    print(user)
    db.session.add(user)
    db.session.commit()


def login(phone: str, password: str) -> None:
    user = User.query.filter_by(phone=phone).first()
    if not user or not check_pw_hash(password, user.password):
        raise ValueError('Invalid credentials')
    login_user(
        user=user
    )

def logout():
    pass