from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField, PasswordField, DateField, IntegerField, SubmitField, ValidationError
from wtforms.validators import EqualTo, DataRequired, Length, NumberRange
from src.models import User

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        if User.query.filter(User.phone == phone.data).first():
            raise ValidationError('Phone number already exists')



class LoginForm(FlaskForm):
    phone = IntegerField('Phone Number', validators=[DataRequired(), NumberRange(min=1000000000, max=9999999999)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=100)])
    submit = SubmitField('Login')