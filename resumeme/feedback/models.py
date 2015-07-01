import datetime
from resumeme import db
from resumeme.accounts.models import User
from resumeme.resume.models import Resume
import constants as CONSTANTS


class _Section(db.EmbeddedDocument):
    name = db.StringField(max_length=CONSTANTS.MAX_SECTION_NAME_LENGTH,
                          choices=(CONSTANTS.FIRST_SECTION, CONSTANTS.SECOND_SECTION, CONSTANTS.THIRD_SECTION,
                                   CONSTANTS.FOURTH_SECTION, CONSTANTS.FIFTH_SECTION),
                          default=None)
    rating = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH, choices=("1", "2", "3", "4", "5"))
    content = db.StringField()


class Feedback(db.Document):
    resume = db.ReferenceField(Resume)  # This field is populated by tagged resume that is clicked for feedback
    edit_lock = db.BooleanField(default=False)
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    user = db.ReferenceField(User)
    # These are the new section fields
    first_section = db.EmbeddedDocumentField(_Section)
    second_section = db.EmbeddedDocumentField(_Section)
    third_section = db.EmbeddedDocumentField(_Section)
    fourth_section = db.EmbeddedDocumentField(_Section)
    fifth_section = db.EmbeddedDocumentField(_Section)
