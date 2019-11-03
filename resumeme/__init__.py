import os
import time
import atexit
import logging
import boto3

from config import ENV
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail

# Create and name Flask app
app = Flask("ResumeMeApp")

# database connection
app.config['MONGODB_SETTINGS'] = {
    'HOST': os.environ.get('MONGOLAB_URI'), 'DB': 'test'}
app.config['SECRET_KEY'] = 'This string will be replaced'

app.debug = os.environ.get('DEBUG', True)

db = MongoEngine(app)  # connect MongoEngine with Flask App
app.session_interface = MongoEngineSessionInterface(db)  # sessions w/ mongoengine

# Flask BCrypt will be used to salt the user password
flask_bcrypt = Bcrypt(app)

# Adding Bootstrap Support
bootstrap = Bootstrap(app)

# Adding momentjs support
moment = Moment(app)

# Associate Flask-Login manager with current app
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize scheduler
app.scheduler = BackgroundScheduler()
app.scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: app.scheduler.shutdown())

# Set up log for apscheduler task
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# Create Boto3 session and client
boto3_session = boto3.Session()
boto3_client = boto3_session.client(
    'mturk',
    endpoint_url=
        'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
        if ENV == 'dev' else
        'https://mturk-requester.us-east-1.amazonaws.com',
)

# Adding Mail Support
# email server
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='sig.umsi@gmail.com',
    MAIL_PASSWORD='SocialInnovationsGroup',
    DEFAULT_MAIL_SENDER='sig.umsi@gmail.com'
)
mail = Mail(app)

app.config['MAX_CONTENT_LENGTH'] = 0.99 * 1024 * 1024


# Application wide Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400
