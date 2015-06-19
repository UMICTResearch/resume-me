import datetime
from resumeme import db


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField(default=False)
    role = db.BooleanField(default=True)
    timestamp = db.DateTimeField(default=datetime.datetime.now())

