from resumeme import db
from resumeme.accounts.models import User

class ReviewMeDocument(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    file_upload = db.StringField()
    created = db.DateTimeField()
    last_updated = db.DateTimeField()
    anon = db.BooleanField(default=False)
    user = db.ReferenceField(User)
    lock = db.BooleanField(default=False)
    feedback_list = db.ListField(db.GenericReferenceField())
    type = "resume"

    meta = {'allow_inheritance': True}


class Resume(ReviewMeDocument):

    meta = {'allow_inheritance': True}



