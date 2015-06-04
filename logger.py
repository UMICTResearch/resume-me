#
# Copyright SIG - June 2015
#

from datetime import datetime
import pytz
import os
from pprint import pprint
import sys
from dbclient import client, db


class Slogger(object):
    def __init__(self, module_name):
        self.module_name = module_name
        print 'logger initiated for %s' % self.module_name

    def plog(self, log_str, class_name='', data={}):
        # pprint('[%s||%s] %s' % (str(ddatetime.now(pytz.utc)), class_name, log_str))
        # self.LOGFILE.write('[' + str(ddatetime.now(pytz.utc)) + '||' + class_name + '] ' + str(log_str) + '\n')
        time = datetime.now(pytz.utc)

        str1 = '%s | %s | %s | %s \n' % (time, self.module_name, class_name, log_str)
        print str1
        if client:
            try:
                rec = {'time': time, 'mudule_name': self.module_name, 'class_name': class_name,
                       'description': log_str, 'data': data}
                db.log.insert(rec)
            except:
                print 'Problem in pushing to mongodb'
        sys.stdout.flush()
        return str1


class logger(Slogger):
    def __init__(self, logdir, fname, insertDate=False):
        self.module_name = fname

        self.start_time = datetime.now(pytz.utc)

        # check if the log dir path exists
        if not os.path.exists(logdir):
            os.mkdir(logdir)

        if insertDate:
            self.LOGFILE_PATH = os.path.join(logdir, fname + '.' + str(ddatetime.now(pytz.utc)) + '.log')
        else:
            self.LOGFILE_PATH = os.path.join(logdir, fname + '.log')
        self.LOGFILE = open(self.LOGFILE_PATH, 'a+')
        print 'logfile initiated at : ' + self.LOGFILE_PATH

        # print 'connecting to redis'
        # self.rc = redis.StrictRedis(host=REDIS_SERVER_URL, port=REDIS_PORT, db=0)

    def log(self, log_str, class_name=''):
        # print '[%s||%s] %s' % (str(ddatetime.now(pytz.utc)), class_name, log_str)
        self.LOGFILE.write('[' + str(ddatetime.now(pytz.utc)) + '||' + class_name + '] ' + str(log_str) + '\n')

    """This method is for pretty printing the log
    """

    def plog(self, log_str, class_name='', data={}):
        time = datetime.now(pytz.utc)

        str1 = '%s | %s | %s | %s \n' % (time, self.module_name, class_name, log_str)
        print str1
        if client:
            try:
                rec = {'time': time, 'mudule_name': self.module_name, 'class_name': class_name,
                       'description': log_str, 'data': data}
                db.log.insert(rec)
            except:
                print 'Problem in pushing to mongodb'
        sys.stdout.flush()
        self.LOGFILE.write(str1)
        self.LOGFILE.flush()
