import pprint

from flask import current_app, Blueprint, render_template, abort, request, flash, redirect, url_for
from flask.ext.login import (current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required)

from resumeme.libs.User import User
from resumeme.accounts import models as usermodels
from resumeme.resume import models as resumemodels
from resumeme.feedback import models as feedbackmodels

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin')
def admin_home():
    if is_admin():
        # resumes = resumemodels.Resume.objects.order_by("-last_updated")
        # for resume in resumes:
            # user = models.User.get_mongo_doc(resume.user)
            # userObj = User()
            # user = userObj.get_mongo_doc()
            # print user
            # print resume.user
            # pprint.pprint(globals())
            # pprint.pprint(locals())
            # userObj = User()
            # username = userObj.get_by_id(resume.user)
        templateData = {
            'resumes': resumemodels.Resume.objects.order_by("-last_updated"),
            'users': usermodels.User.objects,
            'feedbacks': feedbackmodels.Feedback.objects
        }
        return render_template('admin/admin.html', **templateData)
    else:
        return redirect('/')


def is_admin():
    user_obj = usermodels.User.objects.with_id(current_user.id)
    if user_obj.isAdmin:
        return True
