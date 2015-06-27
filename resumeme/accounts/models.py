import datetime
from resumeme import dbnew

class User(dbnew.Document):
    email = dbnew.EmailField(unique=True)
    password = dbnew.StringField(default=True)
    active = dbnew.BooleanField(default=True)
    isAdmin = dbnew.BooleanField(default=False)
    timestamp = dbnew.DateTimeField(default=datetime.datetime.now())

