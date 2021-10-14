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

    password = PasswordField('Password', validators=[
                             InputRequired(), validators.Length(min=8, message='Password must contain a minimum of 8 characters')])


class Login(FlaskForm):

    username = StringField('Username', validators=[
                           InputRequired(), validators.Length(min=1, max=30)])

    password = PasswordField('Password', validators=[InputRequired()])


class Filter(FlaskForm):

    category = StringField('Filter By:', render_kw={
                           "placeholder": "Category"}, validators=[validators.Length(max=30)])
