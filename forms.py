from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nickname = StringField("Nickname", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    submit = SubmitField("Submit")



class SignupForm(LoginForm):
    email = EmailField("Email", [DataRequired()])
    submit = SubmitField("Sign up")



































































