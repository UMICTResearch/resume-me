import datetime
from resumeme import db
from resumeme.accounts.models import User


class AdminDocs(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    file_upload = db.StringField()
    created = db.DateTimeField()
    last_updated = db.DateTimeField()
    user = db.ReferenceField(User)
