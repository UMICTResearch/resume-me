# -*- coding: utf-8 -*-
import collections
from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required, login_user, logout_user, confirm_login, fresh_login_required
from resumeme.accounts import models as usermodels
from resumeme.resume import models as resumemodels
from resumeme.feedback import models as feedbackmodels

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin')
def admin_home():
    if is_admin():
        resumes = resumemodels.Resume.objects.order_by("created")
        users = usermodels.User.objects
        feedbacks = feedbackmodels.Feedback.objects.order_by("last_updated")

        volunteer = 0
        jobseeker = 0

        role_collection = dict()
        sources = []

        for user in users:
            sources.append(user.source.encode("utf-8"))

            if user.role == 'jobseeker':
                jobseeker += 1
                try:
                    role_collection[user.timestamp.year, user.timestamp.month - 1, user.timestamp.day].append(
                        'jobseeker')
                except KeyError:
                    role_collection[user.timestamp.year, user.timestamp.month - 1, user.timestamp.day] = ['jobseeker']
            elif user.role == 'volunteer':
                volunteer += 1
                try:
                    role_collection[user.timestamp.year, user.timestamp.month - 1, user.timestamp.day].append(
                        'volunteer')
                except KeyError:
                    role_collection[user.timestamp.year, user.timestamp.month - 1, user.timestamp.day] = ['volunteer']

        # Number of volunteers vs jobseekers
        usertypes = {}

        for key, value in role_collection.items():
            count = dict(collections.Counter(value))
            if key not in usertypes:
                usertypes[key] = []
                usertypes[key].append(count)
            else:
                usertypes[key].append(count)

        sortedusertypes = collections.OrderedDict(sorted(usertypes.items(), key=lambda x: x[0]))

        sources_dict = collections.Counter(sources)

        # Start resumes vs feedback - created
        resumecreated = {}
        for resume in resumes:
            try:
                resumecreated[resume.created.year, resume.created.month - 1, resume.created.day].append(1)
            except KeyError:
                resumecreated[resume.created.year, resume.created.month - 1, resume.created.day] = [1]

        for k, v in resumecreated.iteritems():
            resumecreated[k] = sum(v)

        sortedresumecreated = collections.OrderedDict(sorted(resumecreated.items(), key=lambda x: x[0]))

        feedbackcreated = {}
        for feedback in feedbacks:
            try:
                feedbackcreated[
                    feedback.last_updated.year, feedback.last_updated.month - 1, feedback.last_updated.day].append(1)
            except KeyError:
                feedbackcreated[
                    feedback.last_updated.year, feedback.last_updated.month - 1, feedback.last_updated.day] = [
                    1]

        for k, v in feedbackcreated.iteritems():
            feedbackcreated[k] = sum(v)

        sortedfeedbackcreated = collections.OrderedDict(sorted(feedbackcreated.items(), key=lambda x: x[0]))
        # End resumes vs feedback - created

        # start total resumes and feedbacks
        # resume
        totalsortedresume = collections.OrderedDict(sorted(resumecreated.items(), key=lambda x: x[0]))

        resumecreatedlist = []

        for k in sorted(resumecreated):
            resumecreatedlist.append(k)

        rescounter = 0
        for k in totalsortedresume.iterkeys():
            if rescounter != 0:
                totalsortedresume[k] += totalsortedresume[resumecreatedlist[rescounter - 1]]
            rescounter += 1

        # feedback
        totalsortedfeedback = collections.OrderedDict(sorted(feedbackcreated.items(), key=lambda x: x[0]))

        feedbackcreatedlist = []

        for k in sorted(feedbackcreated):
            feedbackcreatedlist.append(k)

        feedcounter = 0
        for k in totalsortedfeedback.iterkeys():
            if feedcounter != 0:
                totalsortedfeedback[k] += totalsortedfeedback[feedbackcreatedlist[feedcounter - 1]]
            feedcounter += 1
        # end total resumes and feedbacks

        templateData = {
            'resumes': resumes,
            'users': users,
            'feedbacks': feedbacks,
            'vcount': volunteer,
            'jcount': jobseeker,
            'sources': sources_dict,
            'usertypes': sortedusertypes,
            'resumecreated': sortedresumecreated,
            'feedbackcreated': sortedfeedbackcreated,
            'totalsortedresume': totalsortedresume,
            'totalsortedfeedback': totalsortedfeedback
        }
        return render_template('admin/admin.html', **templateData)
    else:
        return redirect('/')


def is_admin():
    user_obj = usermodels.User.objects.with_id(current_user.id)
    if user_obj.isAdmin:
        return True
