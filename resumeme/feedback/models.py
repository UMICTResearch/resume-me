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
    rating = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH, choices=("1", "2", "3", "4", "5"), required=True)
    content = db.StringField(min_length=CONSTANTS.MIN_CONTENT_LENGTH, required=True)


class Feedback(db.Document):
    resume = db.ReferenceField(Resume)  # This field is populated by tagged resume that is clicked for feedback
    edit_lock = db.BooleanField(default=False)
    last_updated = db.DateTimeField(default=datetime.datetime.now())
    user = db.ReferenceField(User)
    viewed = db.BooleanField(default=False)
    # These are the new section fields
    first_section = db.EmbeddedDocumentField(_Section, required=True)
    second_section = db.EmbeddedDocumentField(_Section, required=True)
    third_section = db.EmbeddedDocumentField(_Section, required=True)
    fourth_section = db.EmbeddedDocumentField(_Section, required=True)
    fifth_section = db.EmbeddedDocumentField(_Section, required=True)
