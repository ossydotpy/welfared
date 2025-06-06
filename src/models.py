from src import db
from src.utils import generate_pw_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    groups = db.relationship(
        'Group',
        back_populates='owner',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __init__(self, first_name, last_name, phone, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.password = generate_pw_hash(password)

    def get_id(self):
        return self._id

    def __str__(self) -> str:
        return f'{self.first_name[0].upper()}. {self.last_name.upper()}'


class Group(db.Model):
    __tablename__ = 'group'

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    owner = db.relationship('User', back_populates='groups')

    welfare_payment = db.relationship(
        'WelfarePayment',
        uselist=False,
        back_populates='group',
        cascade='all, delete-orphan'
    )

    members = db.relationship(
        'GroupMember',
        back_populates='group',
        cascade='all, delete-orphan',
        lazy=True
    )

    def __init__(self, name, owner_id, logo=None, description=None):
        self.name = name
        self.owner_id = owner_id
        self.logo = logo
        self.description = description


class GroupMember(db.Model):
    __tablename__ = 'group_member'

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group._id'), nullable=False)

    group = db.relationship('Group', back_populates='members')

    welfare_payment_transactions = db.relationship(
        'WelfarePaymentTransaction',
        back_populates='group_member',
        cascade='all, delete-orphan',
        lazy=True
    )


class WelfarePayment(db.Model):
    __tablename__ = 'welfare_payment'

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group._id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.String, default='monthly', nullable=False)
    last_paid_date = db.Column(db.Date, nullable=True)
    next_due_date = db.Column(db.Date, nullable=True)

    group = db.relationship('Group', back_populates='welfare_payment')

    transactions = db.relationship(
        'WelfarePaymentTransaction',
        back_populates='welfare_payment',
        cascade='all, delete-orphan',
        lazy=True
    )


class WelfarePaymentTransaction(db.Model):
    __tablename__ = 'welfare_payment_transaction'

    _id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    welfare_payment_id = db.Column(db.Integer, db.ForeignKey('welfare_payment._id'), nullable=False)
    group_member_id = db.Column(db.Integer, db.ForeignKey('group_member._id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)

    welfare_payment = db.relationship('WelfarePayment', back_populates='transactions')
    group_member = db.relationship('GroupMember', back_populates='welfare_payment_transactions')
