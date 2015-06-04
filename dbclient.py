#
# Copyright SIG - June 2015
#

from pymongo import MongoClient

client = None
db = None
'''
Mongodb Connection
'''
try:
    client = MongoClient()
    # Use the test database
    db = client.resume_feedback
except Exception as e:
    print "Mongodb connection error %s" % e
