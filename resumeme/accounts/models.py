import datetime
from resumeme import db


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    role = db.StringField(default=True)
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField(default=False)
    timestamp = db.DateTimeField(default=datetime.datetime.now())
