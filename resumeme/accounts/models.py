from resumeme import db


class User(db.Document):
    email = db.EmailField(unique=True)
    username = db.StringField(unique=True)
    password = db.StringField(default=True)
    role_initial = db.StringField(default=True)
    role = db.StringField(default=True)
    location = db.StringField(default=True)
    source = db.StringField(default=True)
    sourceoptional = db.StringField(default=True)
    active = db.BooleanField(default=True)
    isAdmin = db.BooleanField(default=False)
    timestamp = db.DateTimeField()
