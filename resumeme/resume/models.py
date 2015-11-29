from resumeme import db
from resumeme.accounts.models import User


class Resume(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    file_upload = db.StringField()
    created = db.DateTimeField()
    last_updated = db.DateTimeField()
    anon = db.BooleanField(default=False)
    user = db.ReferenceField(User)
    lock = db.BooleanField(default=False)
    feedback_list = db.ListField(db.GenericReferenceField())
