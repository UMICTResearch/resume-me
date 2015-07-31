import models
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import *
from flask.ext.mongoengine.wtf.orm import validators

user_form = model_form(models.User, exclude=['password'])


# Signup Form created from user_form
class SignupForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


# Login form will provide a Password field (WTForm form field)
class LoginForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired()])


# Password Forgot Form
class ForgotPasswordForm(user_form):
    email = StringField('Email', validators=[validators.DataRequired()])


# Password Reset Form
class ResetPasswordForm(user_form):
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')


# Change Role Form
class ChangeRoleForm(user_form):
    role = SelectField('role', validators=[validators.DataRequired()])
