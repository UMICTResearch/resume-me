import datetime
from resumeme import db
from resumeme.accounts.models import User


class Resume(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    user = db.ReferenceField(User)
