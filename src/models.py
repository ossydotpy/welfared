from src import db
from src.utils import generate_pw_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, first_name, last_name, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.password = generate_pw_hash(password)

    def get_id(self):
        return self._id


    def __str__(self) -> str:
        return f'{self.first_name[0].upper()}. {self.last_name.upper()}'
