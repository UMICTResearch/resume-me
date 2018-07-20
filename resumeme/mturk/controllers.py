from flask import Blueprint, render_template, request, flash, redirect, get_flashed_messages, message_flashed
from flask.ext.login import (current_user, login_required, login_user)
from mongoengine import Q as db_query
from mongoengine import ValidationError
from datetime import datetime
from threading import Timer
from resumeme.libs.User import User

import models
import constants as CONSTANTS
import utils
import time

mturk = Blueprint('mturk', __name__, template_folder='templates')

def register_mturk():
    email = 'mturk@review-me.com'
    username = 'mturk'
    password = ''
    role_initial = ''
    role = ''
    location = ''
    source = ''
    sourceoptional = ''

    user = User(email, username, password, role_initial, role, location, source, sourceoptional)
    user.save()

    return user


# List of Resume or Feedback seen based on role
#
@mturk.route('/mturk', methods=["GET", "POST"])
def mturk_feedback_main():

    # Get the assignment_id from url parameter
    # assignmentId is ASSIGNMENT_ID_NOT_AVAILABLE in preview mode
    assignment_id = request.args.get('assignmentId', 'None')

    # Login as mturk volunteer
    userObj = User()
    user = userObj.get_by_username("mturk")

    # Create a new mturk volunteer account if the account does not exist
    if not user:
        user = register_mturk()
    login_user(user, remember="no")

    resume_id = ''

    user_resume_list = models.Resume.objects(
        db_query(lock=False)
        )

    if len(user_resume_list) != 0:

        for resume in user_resume_list:

            # Check if timedelta between the current time and the last-reviewed time is already over one hour
            if (datetime.now()-resume.last_reviewed).seconds > 3600:
                resume_requested = resume
                resume_id = resume.id
                break
            else:
                continue

        if resume_id == '':
            # No resume is avialable
            return render_template('no_resume.html')

        current_resume = models.Resume.objects().with_id(resume_id)

        if request.method == "POST":

            current_id = request.form.get('resume_id')
            current_resume = models.Resume.objects().with_id(current_id)

            if current_resume.lock is False:
                try:
                    # Tells the feedback display page that the feedback was freshly created and saved.
                    state = "saved"
                    created = datetime.now()

                    feedback = models.Feedback()
                    feedback.last_updated = created

                    feedback.first_section = models._Section()
                    feedback.second_section = models._Section()
                    feedback.third_section = models._Section()
                    feedback.fourth_section = models._Section()
                    feedback.fifth_section = models._Section()

                    feedback.resume = current_resume

                    feedback.first_section.name = CONSTANTS.FIRST_SECTION
                    feedback.first_section.rating = request.form.get('rating_1')
                    feedback.first_section.content = request.form.get('content_1')
                    feedback.second_section.name = CONSTANTS.SECOND_SECTION
                    feedback.second_section.rating = request.form.get('rating_2')
                    feedback.second_section.content = request.form.get('content_2')
                    feedback.third_section.name = CONSTANTS.THIRD_SECTION
                    feedback.third_section.rating = request.form.get('rating_3')
                    feedback.third_section.content = request.form.get('content_3')
                    feedback.fourth_section.name = CONSTANTS.FOURTH_SECTION
                    feedback.fourth_section.rating = request.form.get('rating_4')
                    feedback.fourth_section.content = request.form.get('content_4')
                    feedback.fifth_section.name = CONSTANTS.FIFTH_SECTION
                    feedback.fifth_section.rating = request.form.get('rating_5')
                    feedback.fifth_section.content = request.form.get('content_5')

                    feedback.validate()

                    feedback.resume.update(lock=True)

                    # associate feedback to resume owner
                    feedback.user = feedback.resume.user

                    feedback.save()


                    # push feedback onto resume feedback_list reference list
                    models.Resume.objects(id=resume_id).update_one(push__feedback_list=feedback)
                    current_resume.save()

                    return redirect('/mturk/%s/%s/%s' % (feedback.resume.id, feedback.id, state))

                except ValidationError as e:
                    print "Error:", e
                    flash('Fill out all fields')
                    template_data = {
                        'title': 'Give Feedback',
                        'content': None,
                        'resume': models.Resume.objects().with_id(resume_id)
                    }
                    return render_template('mturk/edit.html', **template_data)

            elif current_resume.lock is True:
                # Resume has been reviewed
                return render_template('404.html')

        else:
            # Default
            template_data = {
                'title': 'Give Feedback',
                'content': None,
                'resume': models.Resume.objects().with_id(resume_id)
            }

            # Update the last_reviewed timestamp
            # No update in preview mode
            if assignment_id != "ASSIGNMENT_ID_NOT_AVAILABLE":
                current_resume.update(last_reviewed = datetime.now())

            return render_template('mturk/edit.html', **template_data)

    else:
        # No resume is avialable
        return render_template('no_resume.html')

@mturk.route('/mturk/<resume_id>/<feedback_id>/<state>')
def mturk_entry_page(resume_id, feedback_id, state="view"):
    # get class resume entry with matching slug
    resume = models.Resume.objects().with_id(resume_id)
    feedback = models.Feedback.objects().with_id(feedback_id)

    if resume and feedback:
        # Display this only when the feedback is freshly saved and not when it is just being viewed.
        if state == "saved":
            flash('Feedback has been saved')

        else:
            feedback.viewed = True
            feedback.save()

        templateData = {
            'title': 'Your Feedback',
            'resume': resume,
            'feedback': feedback
        }

        return render_template('feedback/view.html', **templateData)

    else:
        return render_template('404.html')
