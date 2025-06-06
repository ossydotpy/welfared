from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.fields import SelectField


class CreateWelfareGroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Group Description', validators=[Length(max=200)])
    submit = SubmitField('Create Group')


class CreateGroupMemberForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    group = SelectField('Group', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Add Member')