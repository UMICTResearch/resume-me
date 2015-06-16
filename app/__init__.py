#
# Copyright SIG - June 2015
#

from datetime import date, datetime, timedelta
import pytz
import sys
import os
from flask import Flask, url_for, request, session, redirect, render_template, make_response, current_app, jsonify, \
    send_from_directory
import ipdb
from dbclient import db, client
from dateutil import parser
import json
# from logger import logger
from logger import Slogger as logger
from urllib2 import urlopen
from functools import update_wrapper, wraps
from bson import json_util
from jinja2 import Environment, PackageLoader
from resupload import helpers
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from werkzeug.contrib.fixers import ProxyFix

from resupload import check_task_status

from werkzeug import secure_filename

logr = logger('pcbc-mturk-%s' % __name__)

UPLOAD_FOLDER = './uploads'
UPLOADED_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

''' Flask Server'''
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['UPLOADED_FOLDER'] = UPLOADED_FOLDER


# env = Environment(loader=PackageLoader('task', 'mvp'))

# app.config.from_object('config')

bootstrap = Bootstrap(app)
moment = Moment(app)

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


@app.route("/action", methods=['GET', 'POST'])
@support_jsonp
def action():
    if request.method == 'POST':
        print request.json
        task_type, operation, data = record_actions(request.json)
        return call_method(task_type, operation, data)
    return jsonify(foo="No post request")


@app.route("/submit", methods=['GET', 'POST'])
@support_jsonp
def submit():
    if request.method == 'POST':
        session = request.json
        record_actions(session)

        experiment_name = session['experiment_name']
        task_type = session['task_type']
        operation = session['operation']
        session['endTime'] = datetime.now(pytz.utc)
        data = session['data']

        response = {'worker_ip': get_header_ip()}
        for item in data:
            if item['name'] != '_id':
                response[item['name']] = item['value']
        # logr.plog("Clean Data: "+ json.dumps(response, default=json_util.default), class_name='submit')
        response['endTime'] = datetime.now(pytz.utc)

        if client:
            try:
                res = db.responses.insert(response)
                logr.plog("Successfully pushed a response to MongoDB. Document _id is %s." % res, class_name='submit')
            except Exception as e:
                logr.plog("Couldnt push the response to DB. Exceptions: %s" % e, class_name='submit')
        else:
            logr.plog("Couldn't connect to MongoDB. Please check the connection.", class_name='submit')

        session['data'] = response
        try:
            job = q.enqueue(check_task_status.doWork, session)
        except Exception as e:
            logr.plog("Problem with reqdis queue. Exceptions: %s" % e, class_name='submit')

        return call_method(operation, response)
    return jsonify(foo="No post request")


def call_method(operation, data):
    try:
        # the module loading can be done in real time by using module import_module. We will have to find a way map experiment_name to module path
        methodToCall = eval(operation)
        res = methodToCall(data)
        logr.plog("Successfully executed method: %s. Results is %s." % (operation, res), class_name='call_method')
        return json_util.dumps({'foo': "Success!", 'result': res})
    except Exception as e:
        logr.plog("Some exception occurred: %s" % e, class_name='call_method')
        raise
        return json_util.dumps({'foo': "Error!"})


@app.route("/")
def index():
    return render_template('home.html')


@app.route('/get_hit', methods=['GET'])
def get_hit():
    assignmentId = request.args.get('assignmentId', 'NoAssignmentId')
    workerId = request.args.get('workerId', 'NoWorkerId')
    hitId = request.args.get('hitId', 'NoHitId')
    startTime = datetime.now(pytz.utc)
    record_actions(
        {'type': 'get_hit', 'workerId': workerId, 'hitId': hitId, 'assignmentId': assignmentId, 'startTime': startTime})

    logr.plog("HIT Requested: %s" % [assignmentId, workerId, hitId, startTime], class_name='get_hit')

    if hitId != 'NoHitId':
        # get requirements for this HIT
        exp = db.hits.find_one({'hitId': hitId})
        if 'requirements' in exp:
            requirements = exp['requirements']
            task_type = exp['task_type']
        else:
            requirements = {}
            logr.plog('Requirements or task_type not found', class_name='get_hit')

        requirements['assignmentId'] = assignmentId
        requirements['hitId'] = hitId
        requirements['workerId'] = workerId
        requirements['startTime'] = startTime

        template = render_template(task_type + '.html')
        html = render_template(task_type + '.html', requirements=requirements)
        return html
    else:
        logr.plog('get hit failed', class_name='get_hit')
    return 'Sorry, some error has occurred.'


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def upload_serve(filename):
    return send_from_directory(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads')), filename)


# entry point
@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    startTime = datetime.now(pytz.utc)
    if request.method == 'POST':
        file = request.files['file']
        email_id = request.form['email_id']
        logr.plog("File upload requested from email_id: %s" % email_id, class_name="upload_resume")

        if file and allowed_file(file.filename):
            extension = file.filename.rsplit('.', 1)[1]
            name = file.filename.rsplit('.', 1)[0]
            modified_filename = "%s_%s.%s" % (name, startTime, extension)
            filename = secure_filename(modified_filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = {'filename': filename, 'email_id': email_id}
            res = helpers.upload_resume(data)
            return redirect(url_for('uploaded_file', email_id=email_id,
                                    filename=filename, hitURL=res['res']['hits'][0]['url']))

    # template = get_template('upload/upload.html')
    # html =
    return render_template('upload/upload.html', requirements={})


@app.route('/uploaded_file', methods=['GET', 'POST'])
def uploaded_file():
    requirements = {}
    requirements['filename'] = request.args.get('filename', 'filename')
    requirements['url'] = request.args.get('hitURL', 'hitURL')
    requirements['email_id'] = request.args.get('email_id', 'email_id')
    return render_template('upload/thanks.html', requirements=requirements)


def submit(data):
    task_type = data['task_type']
    if task_type == 'comment_task':
        return helpers.submit_comments(data)
        # elif task_type=='summarize':
        #     helpers.submit_summarize(data)


@app.route('/get_responses/<filename>')
def get_responses(filename):
    # template = render_template('upload/responses.html')
    requirements = db.comments.find_one({'filename': filename})
    html = render_template('upload/responses.html', requirements=requirements)
    return html


@app.route('/get_ipinfo', methods=['GET'])
@support_jsonp
def get_ipinfo():
    ip = get_header_ip()
    response = json.loads(urlopen('http://ipinfo.io/%s/json' % ip).read())
    return jsonify(response)
