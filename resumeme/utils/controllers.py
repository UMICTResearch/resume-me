from flask import current_app, Blueprint, render_template, url_for
from flask.ext.mail import Message
from resumeme import mail

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
