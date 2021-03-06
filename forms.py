from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired , Email , Length


class UserForm(FlaskForm):
    username = StringField('username' ,validators = [InputRequired() ,  Length(max = 20)])
    first_name = StringField('First name' ,validators = [InputRequired(), Length(max = 30)])
    last_name = StringField('Last name' ,validators = [InputRequired(), Length(max = 30)])
    password = PasswordField('Password' ,validators = [InputRequired()])
    email = StringField('Email' , validators=[InputRequired(),Email(message='someone use it or twrong typed!') , Length(max = 50)])




class loginForm(FlaskForm):
    username = StringField('username' ,validators = [InputRequired() ,  Length(max = 20)])
    password = PasswordField('Password' ,validators = [InputRequired()])



class FeedbackForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )






