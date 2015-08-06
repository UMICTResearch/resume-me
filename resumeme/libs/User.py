# -*- coding: utf-8 -*-
from flask.ext.login import (UserMixin, AnonymousUserMixin)
from resumeme.accounts import models


class User(UserMixin):
    def __init__(self, email=None, username=None, password=None, role=None, location=None, source=None, sourceoptional=None,
                 active=True, id=None):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.location = location
        self.source = source
        self.sourceoptional = sourceoptional
        self.active = active
        self.isAdmin = False
        self.id = None

    def save(self):
        newUser = models.User(email=self.email, username=self.username, password=self.password, role=self.role, location=self.location,
                              source=self.source, sourceoptional=self.sourceoptional, active=self.active)
        newUser.save()
        self.id = newUser.id
        return self.id

    def get_by_email(self, email):

        dbUser = models.User.objects.get(email=email)
        if dbUser:
            self.email = dbUser.email
            self.active = dbUser.active
            self.id = dbUser.id
            return self
        else:
            return None

    def get_by_email_w_password(self, email):

        try:
            dbUser = models.User.objects.get(email=email)

            if dbUser:
                self.email = dbUser.email
                self.active = dbUser.active
                self.password = dbUser.password
                self.role = dbUser.role
                self.id = dbUser.id
                return self
            else:
                return None
        except:
            return None

    def get_mongo_doc(self):
        if self.id:
            return models.User.objects.with_id(self.id)
        else:
            return None

    def get_by_id(self, id):
        dbUser = models.User.objects.with_id(id)
        if dbUser:
            self.email = dbUser.email
            self.active = dbUser.active
            self.id = dbUser.id
            self.role = dbUser.role

            return self
        else:
            return None


class Anonymous(AnonymousUserMixin):
    name = u"Anonymous"
