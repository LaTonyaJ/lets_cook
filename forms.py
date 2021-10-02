from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired


class SignUp(FlaskForm):

    first_name = StringField('First Name', validators=[
        validators.Length(min=1, max=30), InputRequired()])

    last_name = StringField('Last Name', validators=[
                            validators.Length(min=1, max=30), InputRequired()])

    username = StringField('Username', validators=[
        validators.Length(min=1, max=30), InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])


class Login(FlaskForm):

    username = StringField('Username', validators=[
                           InputRequired(), validators.Length(min=1, max=30)])

    password = PasswordField('Password', validators=[InputRequired()])
