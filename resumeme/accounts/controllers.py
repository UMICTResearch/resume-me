# -*- coding: utf-8 -*-

import os, datetime, time
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from resumeme import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

import forms
from resumeme.libs.User import User
from resumeme.utils.controllers import send_mail
from resumeme.accounts import models
from resumeme.feedback import models

accounts = Blueprint('accounts', __name__, template_folder='templates')


@accounts.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)

        if user and flask_bcrypt.check_password_hash(user.password, request.form["password"]) and user.is_active():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember):
                return redirect('/feedback')

        else:
            flash("Username or Password Incorrect")
            current_app.logger.error('Username or Password Incorrect')
            return redirect('/login')

    loginForm = forms.LoginForm(csrf_enabled=True)
    templateData = {

        'form': loginForm

    }

    return render_template("/accounts/login.html", **templateData)


@accounts.route("/register-consent", methods=["GET", "POST"])
def consent():
    if request.method == "POST":
        if request.form['consent'] == 'Continue':
            consentCheck = 'accept-consent'
            return redirect('/register/' + consentCheck)
        else:
            return redirect("/")

    return render_template("/accounts/consent.html")


#
# user registration.
#
@accounts.route("/register/<consentCheck>", methods=["GET", "POST"])
def register(consentCheck):
    if consentCheck == 'accept-consent':
        registerForm = forms.SignupForm(request.form, csrf_enabled=True)
        current_app.logger.info(request.form)
        host_url = request.url_root

        if request.method == 'POST' and registerForm.validate() is False:
            current_app.logger.info(registerForm.errors)
            flash('Registration Error - Please Retry')

        elif request.method == 'POST' and registerForm.validate():
            email = request.form['email']
            username = request.form['username']
            role = request.form['role']
            location = request.form['location']
            source = request.form['source']
            sourceoptional = request.form['sourceoptional']

            # generate password hash
            password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

            # prepare User
            user = User(email, username, password_hash, role, location, source, sourceoptional)

            try:
                user.save()
                if login_user(user, remember="no"):
                    send_mail('Your registration was successful', email, 'welcome', user=user, url=host_url)
                    if user.role == 'jobseeker':
                        return redirect('/resume/create')
                    else:
                        return redirect('/feedback')
                else:
                    flash("unable to log you in")
                    return redirect('/register')

            except:
                flash('Registration Error')
                current_app.logger.error('Registration Error')

        templateData = {

            'form': registerForm

        }

        return render_template("/accounts/register.html", **templateData)

    else:
        return redirect("/register-consent")


#
# user registration.
#
@accounts.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    """View function that handles a forgotten password request."""
    forgotPasswordForm = forms.ForgotPasswordForm(request.form, csrf_enabled=True)

    host_url = request.url_root

    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)

        if user and user.is_active():
            send_reset_password_instructions(user, host_url)
            flash("Please check your mail for password reset instructions")
            return render_template("/accounts/forgot_password_notification.html")
        else:
            flash('Email Not Registered')
            current_app.logger.error('Email Not Registered')
            return redirect('/register')

    templateData = {

        'form': forgotPasswordForm

    }

    return render_template("/accounts/forgot_password.html", **templateData)


@accounts.route("/accounts/<token>", methods=["GET", "POST"])
def reset_password(token):
    resetPasswordForm = forms.ResetPasswordForm(request.form, csrf_enabled=True)
    s = Serializer(current_app.config['SECRET_KEY'])
    _id = s.loads(token)

    user = models.User.objects.with_id(_id)

    if request.method == 'POST' and resetPasswordForm.validate() is False:
        current_app.logger.info(resetPasswordForm.errors)
        flash('Passwords should match')

    elif request.method == 'POST' and resetPasswordForm.validate():
        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

        # update user password
        user.update(password=password_hash)

        send_mail('Password Reset Notice', user.email, 'reset_notice', user=user)

        flash('Your Password has been successfully changed.')
        return redirect('/login')

    templateData = {

        'form': resetPasswordForm

    }

    return render_template("/accounts/reset_password.html", **templateData)


@accounts.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = models.User.objects.with_id(current_user.id)

    if request.method == "POST" and "role" in request.form:
        user.update(role=request.form['role'])

        return redirect('/profile')

    if user.role == 'jobseeker':
        _role = "Job Seeker"
    else:
        _role = "Volunteer"

    changeRoleForm = forms.ChangeRoleForm(csrf_enabled=True)
    templateData = {

        'form': changeRoleForm,
        'user': user,
        'role': _role

    }

    return render_template("/accounts/profile.html", **templateData)


@accounts.route("/logout")
@login_required
def logout():
    logout_user()
    # flash("Logged out.")
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@login_manager.user_loader
def load_user(id):
    if id is None:
        redirect('/login')
    user = User()
    user.get_by_id(id)
    if user.is_active():
        return user
    else:
        return None


def send_reset_password_instructions(user, host_url):
    """Sends the reset password instructions email for the specified user.

    :param user: The user to send the instructions to
    """
    token = generate_reset_password_token(user)

    send_mail('Review-me password reset', user.email, 'reset_instructions', user=user, reset_link=token,
              url=host_url)


def generate_reset_password_token(user, expiration=1000):
    """Generates a unique reset password token for the specified user.

    :param user: The user to work with
    """

    set_serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
    return set_serializer.dumps(str(user.id))
