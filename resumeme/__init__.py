import os

from flask import Flask, render_template, request, redirect
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.mail import Mail

# Create and name Flask app
app = Flask("ResumeMeApp")

# database connection
app.config['MONGODB_SETTINGS'] = {
    'HOST': os.environ.get('MONGOLAB_URI'), 'DB': 'resumemetest'}
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

# Adding Mail Support
# email server
app.config.update(
    MAIL_SERVER='smtp.mandrillapp.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME='umichictresearch@gmail.com',
    MAIL_PASSWORD='syknj9Tp5IR41t0CKN8w9w',
    DEFAULT_MAIL_SENDER='umichictresearch@gmail.com'
)
mail = Mail(app)

# File upload settings
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf'}

app.config['MAX_CONTENT_LENGTH'] = 0.99 * 1024 * 1024

# ALLOWED_EXTENSIONS = set(['txt', 'pdf'])
