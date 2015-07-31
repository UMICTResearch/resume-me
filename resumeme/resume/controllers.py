import os, datetime, time
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify, \
    send_from_directory
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from werkzeug import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import models
from constants import *
from resumeme.libs.User import User

resume = Blueprint('resume', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@resume.route('/resumes')
@login_required
def resumes():
    templateData = {
        'resumes': models.Resume.objects.order_by("-last_updated")
    }
    return render_template('resume/index.html', **templateData)


@resume.route("/resume/create", methods=["GET", "POST"])
@login_required
def resume_create():
    if request.method == "POST":
        file = request.files['file']

        if file and allowed_file(file.filename):
            timestamp = int(time.time())
            timestamp = str(timestamp)

            filename = secure_filename(file.filename)
            filename = timestamp + '.' + filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            resume = models.Resume()
            resume.title = request.form.get('title', '')
            resume.content = request.form.get('content')
            resume.file_upload = filename

            # associate note to currently logged in user
            resume.user = current_user.get_mongo_doc()
            resume.save()

            flash('Your resume has been successfully created')
            return redirect('/resume/%s' % resume.id)
        else:
            resume = models.Resume()
            resume.title = request.form.get('title', '')
            resume.content = request.form.get('content')
            template_data = {
                'title': 'Create New Resume',
                'resume': resume,
                'view': False
            }
            flash('Please select the correct file type. Allowed: pdf and txt')
            return render_template('resume/edit.html', **template_data)

    template_data = {
        'title': 'Create New Resume',
        'resume': None,
        'view': False
    }
    return render_template('resume/edit.html', **template_data)


@resume.route("/resume/<resume_id>/edit", methods=["GET", "POST"])
@login_required
def edit_resume(resume_id):
    # get single document returned
    resume = models.Resume.objects().with_id(resume_id)

    if resume and resume.lock is False:
        if resume.user.id != current_user.id:
            return "Sorry you do not have permission to edit this resume"

        if request.method == "POST":
            file = request.files['file']

            timestamp = int(time.time())
            timestamp = str(timestamp)

            resume.title = request.form.get('title', '')
            resume.content = request.form.get('content')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = timestamp + '.' + filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                resume.file_upload = filename
                resume.save()
                flash('Your resume has been successfully updated')
                return redirect('/resume/%s' % resume.id)
            else:
                flash('Please select the correct file type. Allowed: pdf and txt')


        template_data = {
            'title': 'Edit resume',
            'resume': resume,
            'view': True
        }

        return render_template('resume/edit.html', **template_data)

    else:
        flash("Editing this entry not allowed. Please create a new one.")
        return redirect('resume/create')


@resume.route('/resume/<resume_id>')
def resume_view(resume_id):
    # get class resumes entry with matching slug
    resume = models.Resume.objects().with_id(resume_id)

    if resume:
        templateData = {
            'resume': resume
        }
        return render_template('resume/view.html', **templateData)

    else:
        return render_template('404.html')


@resume.route('/uploads/<filename>')
@login_required
def upload_serve(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@resume.errorhandler(413)
def upload_limit(error):
    template_data = {
        'title': 'Create New Resume',
        'resume': None
    }
    flash('The file size exceeds the limit allowed. Please upload a resume which is lesser than 1 MB')
    return render_template('resume/edit.html', **template_data)
