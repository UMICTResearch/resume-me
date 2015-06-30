import os

from flask import Flask, render_template, request, redirect
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment


# Create and name Flask app
app = Flask("FlaskCustomApp")

# database connection
app.config['MONGODB_SETTINGS'] = {
    'HOST': os.environ.get('MONGOLAB_URI'), 'DB': 'ratatouille'}
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
