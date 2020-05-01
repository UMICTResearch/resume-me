
from flask import Blueprint, render_template, request, flash, redirect, get_flashed_messages, message_flashed, session, current_app
from flask_login import (current_user, login_required, login_user)
from mongoengine import Q as db_query
from mongoengine import ValidationError
from datetime import datetime
from threading import Timer
from resumeme.libs.User import User
from resumeme.utils.controllers import send_mail
from bson.objectid import ObjectId
import urllib
import math

import models
import constants as CONSTANTS
import utils
import time
import logging 
mturk = Blueprint('mturk', __name__, template_folder='templates')

#Create and configure
logger = logging.getLogger('Create_HIT')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('create_hit_wsgi.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
# logger.addHandler(ch)
logger.addHandler(fh)

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
    assignment_id = request.args.get('assignmentId', '')
    worker_id = request.args.get('workerId', '')
    hit_id = request.args.get('hitId', '')
    submit_hit_url = request.args.get('turkSubmitTo', '')


    # Login as mturk volunteer
    userObj = User()
    user = userObj.get_by_username("mturk")

    # Create a new mturk volunteer account if the account does not exist
    if not user:
        user = register_mturk()
    login_user(user, remember="no")

    if request.method == "GET":
	print(hit_id)
        resume_id = models.boto3_client.get_hit(
            HITId=hit_id
        )['HIT']['RequesterAnnotation']
        resume_id = ObjectId(resume_id)
        resume = models.Resume.objects().with_id(resume_id)
        if resume != None:
            # Default
            template_data = {
                'title': 'Give Feedback',
                'content': None,
                'resume': resume,
            }
            return render_template('mturk/edit.html', **template_data)
        else:
            return render_template('no_resume.html')
    else:
        resume_id = request.form.get('resume_id')
        resume = models.Resume.objects().with_id(resume_id)

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

            feedback.resume = resume

            feedback.first_section.name = CONSTANTS.FIRST_SECTION
            feedback.first_section.rating = request.form.get('rating_1')
            feedback.first_section.content = request.form.get('content_1')
            feedback.second_section.name = CONSTANTS.SECOND_SECTION
            feedback.second_section.rating = request.form.get('rating_2')
            feedback.second_section.content = request.form.get('content_2')
            feedback.third_section.name = CONSTANTS.THIRD_SECTION

            feedback.first_section.name = CONSTANTS.FIRST_SECTION
            feedback.first_section.rating = request.form.get('rating_1')
            feedback.first_section.content = request.form.get('content_1')
            feedback.second_section.name = CONSTANTS.SECOND_SECTION
            feedback.second_section.rating = request.form.get('rating_2')
            feedback.second_section.content = request.form.get('content_2')
            feedback.third_section.name = CONSTANTS.THIRD_SECTION
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

            # associate feedback to resume owner
            feedback.user = feedback.resume.user
            feedback.save()

            # push feedback onto resume feedback_list reference list
            resume.update(push__feedback_list=feedback)
            resume.update(last_reviewed=datetime.utcnow())
            resume.update(posted=False)
            resume.update(lock=True)

            url_para = 'workerId=' + worker_id + '&assignmentId=' + assignment_id + '&hitId=' + 'hit_id' + '&turkSubmitTo=' + submit_hit_url

            return redirect('/mturk/%s/%s/%s?%s' % (feedback.resume.id, feedback.id, state, url_para))

        except ValidationError as e:
            print "Error:", e
            flash('Fill out all fields')
            template_data = {
                'title': 'Give Feedback',
                'content': None,
                'resume': resume
            }
            return render_template('mturk/edit.html', **template_data)


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

        return render_template('mturk/view.html', **templateData)

    else:
        return render_template('404.html')


def mturk_approve_HIT():
    response = models.boto3_client.list_reviewable_hits()
    HITs = response['HITs']
    for HIT in HITs:
        resume_id = HIT['RequesterAnnotation']
        resume_id = ObjectId(resume_id)
        resume = models.Resume.objects().with_id(resume_id)
	if resume.posted:
	    continue

	assignments = models.boto3_client.list_assignments_for_hit(
            HITId=HIT['HITId'],
        )['Assignments']
	assignment = assignments[0]

        accepted = assignment['AcceptTime']
        duration = resume.last_reviewed - accepted.replace(tzinfo=None) + accepted.utcoffset()
        resume.update(complete_time=duration.total_seconds() + 60)

        models.boto3_client.approve_assignment(AssignmentId=assignment['AssignmentId'])
	models.boto3_client.delete_hit(HITId=HIT['HITId'])

    
def mturk_post_HIT():
    resume_list = models.Resume.objects(
        db_query(posted=False) & db_query(lock=False)
    )
    # resume_list = resume_list[:20]
    count = 0
    for resume in resume_list:
        if (datetime.now()-resume.last_reviewed).seconds > 3600:
            resume.update(posted=True)
            count += 1
    #logger.info(str(count))
    for resume in resume_list:
        if (datetime.now()-resume.last_reviewed).seconds > 3600:
            response = models.boto3_client.create_hit(
                MaxAssignments=1,
                LifetimeInSeconds=60,
                AssignmentDurationInSeconds=300,
                Reward='0.06',
                Title='review-me',
                Keywords='resume, review, rate',
                Description='Please review resume, rate it and give feedback',
                Question=CONSTANTS.EXTERNAL_QUESTION,
                RequesterAnnotation=str(resume.id),
                QualificationRequirements=CONSTANTS.WORKER_REQUIREMENTS,
            )
    	    #logger.info(str(resume.id))
     	

def mturk_check_status():
    response = models.boto3_client.list_hits()
    num_hits = response['NumResults']
    for HIT in response['HITs']:
	print('')
	print(HIT['HITId'])
        print(HIT['HITStatus'])
	print(HIT['CreationTime'])
        assignments = models.boto3_client.list_assignments_for_hit(
            HITId=HIT['HITId'],
        )['Assignments']
        for assignment in assignments:
            print(assignment['AssignmentStatus'])
	    print(assignment['AcceptTime'])
	    print(assignment['SubmitTime'])
	    print(assignment['Deadline'])

def mturk_clean_HIT():
    """
    For each reviewable HIT,
    approve all submitted assignments, and delete HIT.
    Note: some HITs expire and don't have any assignment.
    """
    response = models.boto3_client.list_reviewable_hits()
    HITs = response['HITs']
    for HIT in HITs:
	print(HIT['HITId'])
        assignments = models.boto3_client.list_assignments_for_hit(
            HITId=HIT['HITId'],
            AssignmentStatuses=['Submitted'],
        )['Assignments']
        for assignment in assignments:
            models.boto3_client.approve_assignment(
                AssignmentId=assignment['AssignmentId'],
            )
        models.boto3_client.delete_hit(
            HITId=HIT['HITId']
        )

def mturk_clean_all_HIT():
    """
    For each reviewable HIT,
    approve all submitted assignments, and delete HIT.
    Note: some HITs expire and don't have any assignment.
    """
    response = models.boto3_client.list_hits()
    HITs = response['HITs']
    for HIT in HITs:
        print(HIT['HITId'])
	if HIT['HITStatus'] == 'Assignable':
            assignments = models.boto3_client.list_assignments_for_hit(
            	HITId=HIT['HITId'],
                AssignmentStatuses=['Submitted'],
            )['Assignments']
            for assignment in assignments:
                models.boto3_client.approve_assignment(
                    AssignmentId=assignment['AssignmentId'],
                )
            models.boto3_client.delete_hit(
                HITId=HIT['HITId']
            )


    
def mturk_revive_resume():
    """
    If some resume is posted as HIT but not completed
    within lifetime of HIT, we will need to manually set
    such a resume back to postable
    """
    response = models.boto3_client.list_reviewable_hits()
    HITs = response['HITs']
    for HIT in HITs:
        resume_id = HIT['RequesterAnnotation']
        resume_id = ObjectId(resume_id)
        resume = models.Resume.objects().with_id(resume_id)
        if resume.lock == False:
            resume.update(posted=False)
            models.boto3_client.delete_hit(HITId=HIT['HITId'])

def mturk_unassignable():
    response = models.boto3_client.list_hits(
        MaxResults=5
    )
    HITs = response['HITs']
    for HIT in HITs:
        resume_id = HIT['RequesterAnnotation']
        resume_id = ObjectId(resume_id)
	#logger.info(str(resume_id))

def mturk_check():
	#mturk_post_HIT()
	#mturk_approve_HIT()
	#mturk_revive_resume()
	#mturk_clean_all_HIT()
	mturk_check_status()

def mturk_report():
	balance = models.boto3_client.get_account_balance()['AvailableBalance']
	if float(balance) < float(90):
		bal = str(int(math.ceil(float(balance))))
		msg = 'MTurk balance is lower than $' + bal
		with models.app.app_context():
			send_mail(msg, "umichictresearch@gmail.com", 'notify_balance', balance=balance)

            
@mturk.record
def add_mturk_job(state):
    state.app.scheduler.add_job(func=mturk_check, trigger="interval", seconds=10)
    state.app.scheduler.add_job(func=mturk_report, trigger="interval",
days=1)
    #state.app.scheduler._logger=logger
