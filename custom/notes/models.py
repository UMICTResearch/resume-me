import datetime
from custom import db
from custom.accounts.models import User


class Note(db.Document):
    title = db.StringField(required=True, max_length=120)
    content = db.StringField()
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    user = db.ReferenceField(User)
