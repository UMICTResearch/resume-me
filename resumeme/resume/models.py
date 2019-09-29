from resumeme import db
from resumeme.accounts.models import User
import datetime

class Resume(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    file_upload = db.StringField()
    created = db.DateTimeField()
    last_updated = db.DateTimeField()
    anon = db.BooleanField(default=False)
    user = db.ReferenceField(User)
    lock = db.BooleanField(default=False)
    last_reviewed = db.DateTimeField(default=datetime.datetime(1900,1,1))
    feedback_list = db.ListField(db.GenericReferenceField())
    posted = db.BooleanField(default=False)
