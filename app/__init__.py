#
# Copyright SIG - June 2015
#

import os
import sys

from flask import Flask, url_for, request, session, redirect, render_template, make_response, current_app, jsonify, \
    send_from_directory
from logger import logger
from dbclient import db, client
from urllib2 import urlopen
from functools import update_wrapper, wraps

app = Flask(__name__)
app.config.from_object('config')


########################
# Configure Secret Key #
########################
def install_secret_key(app, filename='secret_key'):
    """Configure the SECRET_KEY from a file
    in the instance directory.

    If the file does not exist, print instructions
    to create it from a shell with a random key,
    then exit.
    """
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        print('Error: No secret key. Create it with:')
        full_path = os.path.dirname(filename)
        if not os.path.isdir(full_path):
            print('mkdir -p {filename}'.format(filename=full_path))
        print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        sys.exit(1)


if not app.config['DEBUG']:
    install_secret_key(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def support_jsonp(f):
    """Wraps JSONified output for JSONP"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f().data) + ')'
            return app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)

    return decorated_function


def get_header_ip():
    if request.headers.get("REMOTE_ADDR"):
        return request.headers.get('REMOTE_ADDR')
    else:
        return request.remote_addr


def record_actions(session):
    # logr.plog("Data: "+ json.dumps(session, default=json_util.default), class_name='action')
    # find task_type and operation

    # logr.plog("Request is by %s."%(get_header_ip()), class_name='record_actions')
    session['__name__'] = __name__
    session['worker_ip'] = get_header_ip()
    if client:
        try:
            res = db.operations.insert(session)
            logr.plog("Successfully pushed a response to MongoDB. Document _id is %s." % res,
                      class_name='record_actions')
        except Exception as e:
            logr.plog("Couldnt push the response to DB. Exceptions: %s" % e, class_name='record_actions')
    else:
        logr.plog("Couldn't connect to MongoDB. Please check the connection.", class_name='record_actions')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
