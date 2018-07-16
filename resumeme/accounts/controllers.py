# -*- coding: utf-8 -*-

from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from resumeme import login_manager, flask_bcrypt
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import forms
from resumeme.libs.User import User
from resumeme.utils.controllers import send_mail, do_flash
from resumeme.accounts import models
from resumeme.feedback import models
from resumeme.config import *

accounts = Blueprint('accounts', __name__, template_folder='templates')


@accounts.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)

        # print(user.email)
        # print(user.password)
        # print(user.username)
        # print(user.role_initial)
        # print(user.role)
        # print(user.location)

        if user and flask_bcrypt.check_password_hash(user.password, request.form["password"]) and user.is_active():
            remember = request.form.get("remember", "no") == "yes"

            if login_user(user, remember=remember):
                return redirect('/feedback')

        else:
            do_flash(LOGIN_ERROR, "info")

            # current_app.logger.error('Username or Password Incorrect')
            return redirect('/login')

    loginForm = forms.LoginForm(csrf_enabled=True)
    templateData = {

        'form': loginForm

    }

    return render_template("/accounts/login.html", **templateData)


@accounts.route("/register-consent")
def consent():
    return render_template("/accounts/consent.html")


#
# user registration.
#
@accounts.route("/register", methods=["GET", "POST"])
def register():
    registerForm = forms.SignupForm(request.form, csrf_enabled=True)
    current_app.logger.info(request.form)
    host_url = request.url_root

    templateData = {

        'form': registerForm

    }

    if request.method == 'POST' and registerForm.validate() is False:
        current_app.logger.info(registerForm.errors)
        flash_errors(registerForm)

        return render_template("/accounts/register.html", **templateData)
    elif request.method == 'POST' and registerForm.validate():
        email = request.form['email']
        username = request.form['username']
        role_initial = request.form['role']
        role = request.form['role']
        location = request.form['location']
        source = request.form['source']
        sourceoptional = request.form['sourceoptional']

        # generate password hash
        password_hash = flask_bcrypt.generate_password_hash(request.form['password'])

        # prepare User
        user = User(email, username, password_hash, role_initial, role, location, source,
                    sourceoptional)

        userObj = User()
        email_check = userObj.get_by_email(email)
        username_check = userObj.get_by_username(username)

        if email_check:
            if email_check.active:
                do_flash(REGISTRATION_EMAIL_EXISTS, "danger")
            else:
                do_flash(REGISTRATION_INACTIVE, "danger")

                return redirect('/activate')
        elif username_check:
            do_flash(REGISTRATION_UNAME_EXISTS, "danger")
        else:
            try:
                user.save()
                if login_user(user, remember="no"):
                    send_mail('Your registration was successful', email, 'welcome', user=user, url=host_url)

                    if user.role == 'jobseeker':
                        return redirect('/resume/create')
                    else:
                        return redirect('/feedback')
                else:
                    do_flash(REGISTRATION_NOLOGIN, "danger")

                    return redirect('/register')
            except:
                do_flash(REGISTRATION_ERROR, "danger")

    return render_template("/accounts/register.html", **templateData)


#
# user password reset.
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

        if user and user.active:
            send_reset_password_instructions(user, host_url)
            flash("Please check your mail for password reset instructions")
            return render_template("/accounts/forgot_password_notification.html")
        else:
            flash('Email Not Registered')
            current_app.logger.error('Email Not Registered')
            return redirect('/register-consent')

    templateData = {

        'form': forgotPasswordForm

    }

    return render_template("/accounts/forgot_password.html", **templateData)


#
# user account re-activate
#
@accounts.route("/activate", methods=["GET", "POST"])
def activate_account():
    """View function that handles account reactivation request."""
    activateAccountForm = forms.ActivateAccountForm(request.form, csrf_enabled=True)

    host_url = request.url_root

    if request.method == "POST" and "email" in request.form:
        email = request.form["email"]
        userObj = User()
        user = userObj.get_by_email_w_password(email)

        if user and user.active is False:
            send_account_activation_instructions(user, host_url)
            flash("Please check your mail for account activation instructions")
            return render_template("/accounts/activate_notification.html")
        else:
            flash('Email Not Registered')
            current_app.logger.error('Email Not Registered')
            return redirect('/register-consent')

    templateData = {

        'form': activateAccountForm

    }

    return render_template("/accounts/activate.html", **templateData)


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


@accounts.route("/activate/<token>", methods=["GET", "POST"])
def activate_account_request(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    _id = s.loads(token)

    user = models.User.objects.with_id(_id)

    if request.method == 'POST' and user.active is False:
        user.update(active=True)

        flash('Your Account has been reactivated. You may now log in!')

        return redirect('/login')

    return render_template("/accounts/activate_request.html")


@accounts.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = models.User.objects.with_id(current_user.id)

    if request.method == "POST" and "role" in request.form:
        user.update(role=request.form['role'])

        return redirect('/profile')

    elif request.method == "POST" and "deactivate" in request.form:
        user.update(active=False)

        send_mail('Account Deactivation Notice', user.email, 'deactivate_notice', user=user)

        flash("Your account has been successfully deactivated.")
        return redirect('/logout')

    elif request.method == "POST" and "editusername" in request.form:
        if request.form['editusername'].strip() == '':
            flash("Please enter a username")
        else:
            user.update(username=request.form['editusername'])
            flash("Your username has been successfully updated")

        return redirect('/profile')

    if user.role == 'jobseeker':
        _role = "Job Seeker"
    else:
        _role = "Volunteer"

    updateProfile = forms.updateProfileForm(csrf_enabled=True)

    templateData = {

        'form': updateProfile,
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
    token = generate_token(user)

    send_mail('Review-me password reset', user.email, 'reset_instructions', user=user, reset_link=token,
              url=host_url)


def send_account_activation_instructions(user, host_url):
    """Sends the account activation instructions email for the specified user.

    :param user: The user to send the instructions to
    """
    token = generate_token(user)

    send_mail('Review-me Account Re-activation', user.email, 'activate_instructions', user=user, reset_link=token,
              url=host_url)


def generate_token(user, expiration=1000):
    """Generates a unique reset password token for the specified user.

    :param user: The user to work with
    """

    set_serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
    return set_serializer.dumps(str(user.id))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
