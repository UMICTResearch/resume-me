from bson import json_util
from logger import Slogger as logger
from random import shuffle
from dateutil import parser
import turk_utils as turk
from datetime import date, datetime, timedelta
import pytz
import task_utils

MIN_TASK_TIME = 10  # seconds

from dbclient import db, client

logr = logger('pcbc-mturk-%s' % __name__)

use_sandbox = True
fixed_task_config = {
    'use_sandbox': use_sandbox,
    'createTime': datetime.now(pytz.utc),
    'port': 4999 if use_sandbox else 5000,
}

comment_task_config = {
    'task_type': 'comment_task',
    'title': 'Give your feedback on a resume.',
    'experiment_name': 'mvp',
    'max_assignments': 3,
    'incentive': 0.16,
}


def upload_resume(data):
    # creates record in mongo for resume upload and then creates a HIT
    if client:
        res = 'test'
        try:
            d2 = {}
            d2['filename'] = data['filename']
            d2['email_id'] = data['email_id']
            res = db.resumes.insert(d2)
            logr.plog("Resume record inserted successfully. filename: %s, res: %s" % (data['filename'], res),
                      class_name='upload_resume', data=data)
            d2['_id'] = res

            task_config = {}
            task_config.update(fixed_task_config)
            task_config.update(comment_task_config)
            task_config['taskid'] = "%s_%s" % (comment_task_config['experiment_name'], task_config['task_type'])
            # now create a new HIT
            taskd = task_utils.create_task(task_config, [d2])
            task_doc = taskd
            task_id = taskd['_id']
            logr.plog("Task started: %s, email_id: %s" % (task_doc['_id'], d2['email_id']), class_name='upload_resume')
        except Exception as e:
            logr.plog("Couldnt push the response to DB. Exceptions: %s" % e, class_name='upload_resume', data=data)
            raise
            return {'id': 'FAILED!'}
    else:
        logr.plog("Couldn't connect to MongoDB. Please check the connection.", class_name='upload_resume', data=data)
    return {'res': taskd}


def add_to_bad_response(data, reason=''):
    # verification question test failed
    data.update({'reason': reason})
    db.bad_votes.insert(data)
    # add assignment_count of the hit and task
    hitd = db.hits.find_and_modify({'hitId': data['hitId']},
                                   {
                                       '$inc': {'additional_assignments': 1}
                                   },
                                   new=True)
    # add assignment
    res = turk.extend_hit_assignments(data['hitId'], 1)
    logr.plog("HIT successfully extended: %s, result is: %s" % (data['hitId'], res), class_name='add_to_bad_response',
              data=data)
    # reject assignment
    # res = turk.reject_assignment(data['assignmentId'])
    # logr.plog("Assignment successfully rejected: %s, result is: %s"%(data['hitId'],res), class_name='add_to_bad_response', data=data)
    return {'id': 'FAILED!', 'reason': 'Verification failed!'}


def verify_submission(data):
    return True
    # if (data['endTime']- parser.parse(data['startTime'])).seconds<=MIN_RATING_TASK_TIME:
    #     add_to_bad_response(data, 'TaskDuration')
    #     logr.plog("Task duration was too short. AssignmentId: %s"%data['assignmentId'], class_name='verify', data=data)
    #     return False
    # else:
    #     for i in range(1,int(data.get('n',3))+1):
    #         if data['message%i_id'%i] == 'verification_question':
    #             ver_likely_rating = float(data.get('message%i_rating_Likely'%i, 5))
    #             if ver_likely_rating>3.5:
    #                 add_to_bad_response(data, 'FailedVerification')
    #                 logr.plog("Verification test failed. AssignmentId: %s"%data['assignmentId'], class_name='verify', data=data)
    #                 return False
    # return True


def get_no_of_comments(data):
    for i in range(1, 100):
        if 'message%s_id' % i not in data:
            return i - 1


def submit_comments(data):
    # reads the data and pushes it to the mongodb
    n = get_no_of_comments(data)
    logr.plog("Found messages: %s" % n, class_name='submit', data=data)
    if client:
        res = 'test'
        try:
            hitId = data['hitId']
            task_id = data['task_id']
            assignmentId = data['assignmentId']
            messages = []
            if verify_submission(data):
                for i in range(1, n + 1):
                    d2 = {}
                    d2['filename'] = data['filename']
                    d2['email_id'] = data['email_id']
                    if data['message%i_id' % i] != 'verification_question':
                        message_id = data['message%i_id' % i]
                        message_desc = data['message%i_desc' % i]
                        message_text = data['message%i_text' % i]
                        messages.append({'id': message_id, 'desc': message_desc, 'text': message_text})
            try:
                res = db.comments.find_and_modify(d2,
                                                  {'$addToSet': {'comments': {'assignment_id': assignmentId,
                                                                              'worker_id': data['workerId'],
                                                                              'hitId': hitId,
                                                                              'task_id': task_id,
                                                                              'messages': messages,
                                                                              'use_sandbox': data['use_sandbox']}
                                                                 }
                                                   },
                                                  upsert=True, new=True)
                logr.plog("Comments inserted successfully. AssignmentId: %s" % data['assignmentId'],
                          class_name='submit', data=data)
            except Exception as e:
                logr.plog("Bad submission. AssignmentId: %s. Exception: %s" % (assignmentId, e), class_name='submit',
                          data=data)

        except Exception as e:
            logr.plog("Couldnt push the response to DB. Exceptions: %s" % e, class_name='submit', data=data)
            raise
            return {'id': 'FAILED!'}
    else:
        logr.plog("Couldn't connect to MongoDB. Please check the connection.", class_name='submit', data=data)
    return {'res': res}
