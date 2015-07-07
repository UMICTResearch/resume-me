import os, datetime
from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for, jsonify, \
    send_from_directory
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)
from jinja2 import TemplateNotFound
from werkzeug import secure_filename

import models
from constants import *
from resumeme.libs.User import User
import random, string

resume = Blueprint('resume', __name__, template_folder='templates')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@resume.route('/resumes')
@login_required
def resumes():
    templateData = {
        'resumes': models.Resume.objects.order_by("-last_updated")
    }
    return render_template('resume/index.html', **templateData)


@resume.route("/resume/create", methods=["GET", "POST"])
@login_required
def admin_entry_create():
    if request.method == "POST":
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

            resume = models.Resume()
            resume.title = request.form.get('title', '')
            resume.content = request.form.get('content')
            resume.file_upload = filename

            # associate note to currently logged in user
            resume.user = current_user.get_mongo_doc()
            resume.save()

            return redirect('/resume/%s' % resume.id)

    else:
        template_data = {
            'title': 'Create New Resume Version',
            'resume': None
        }
        return render_template('resume/edit.html', **template_data)


@resume.route("/resume/<resume_id>/edit", methods=["GET", "POST"])
@login_required
def admin_entry_edit(resume_id):
    # get single document returned
    resume = models.Resume.objects().with_id(resume_id)

    if resume:
        if resume.user.id != current_user.id:
            return "Sorry you do not have permission to edit this resume"

        if request.method == "POST":
            resume.title = request.form.get('title', '')
            resume.content = request.form.get('content')

            resume.save()

            flash('resume has been updated')

        template_data = {
            'title': 'Edit resume',
            'resume': resume
        }

        return render_template('resume/edit.html', **template_data)

    else:
        return "Unable to find entry %s" % resume_id


@resume.route('/resume/<resume_id>')
def entry_page(resume_id):
    # get class resumes entry with matching slug
    resume = models.Resume.objects().with_id(resume_id)

    if resume:
        templateData = {
            'resume': resume
        }
        return render_template('resume/view.html', **templateData)

    else:
        return "not found"


@resume.route('/uploads/<filename>')
@login_required
def upload_serve(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
