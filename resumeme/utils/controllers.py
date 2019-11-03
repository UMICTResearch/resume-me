from flask import current_app, Blueprint, render_template, flash
from flask_mail import Message
from resumeme import mail
from os import stat
from pwd import getpwuid

utils = Blueprint('utils', __name__, template_folder='templates')

default_sender = 'donot-reply@review-me.us'


def send_mail(subject, recipient, template, **context):
    """Send an email via the Flask-Mail extension.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    :param context: The context to render the template with
    """

    msg = Message(subject, sender=default_sender, recipients=[recipient])

    ctx = ('/email', template)
    msg.body = render_template('%s/%s.txt' % ctx, **context)
    msg.html = render_template('%s/%s.html' % ctx, **context)

    mail.send(msg)


def find_owner(filename):
    """Find the owner of the file and set upload path
    :param filename: name of file
    """

    return getpwuid(stat(filename).st_uid).pw_name


def do_flash(message, category=None):
    """Flash a message depending on the `FLASH_MESSAGES` configuration value

    :param message: The flash message
    :param category: The flash message category
    """
    flash(message, category)
