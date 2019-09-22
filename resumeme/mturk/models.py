import datetime
from resumeme import db, app
from resumeme.accounts.models import User
from resumeme.resume.models import Resume
import constants as CONSTANTS


class _Section(db.EmbeddedDocument):
    name = db.StringField(max_length=CONSTANTS.MAX_SECTION_NAME_LENGTH,
                          choices=(CONSTANTS.FIRST_SECTION, CONSTANTS.SECOND_SECTION, CONSTANTS.THIRD_SECTION,
                                   CONSTANTS.FOURTH_SECTION, CONSTANTS.FIFTH_SECTION, CONSTANTS.LEGACY_SECTION),
                          default=None)
    rating = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH, choices=("1", "2", "3", "4", "5"), required=True)
    content = db.StringField(min_length=CONSTANTS.MIN_CONTENT_LENGTH, required=True)
    review = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH,
                            choices=(CONSTANTS.SECTION_CHOICE_ONE, CONSTANTS.SECTION_CHOICE_TWO,
                                     CONSTANTS.SECTION_CHOICE_THREE))


class Feedback(db.Document):
    version = 1
    last_updated = db.DateTimeField()

    # TODO: Implement edit_lock
    viewed = db.BooleanField(default=False) # used to set edit_lock and show the new feedback flag
    edit_lock = db.BooleanField(default=False) # locked state means the feedback can't be updated
    review_lock = db.BooleanField(default=False) # locked once a review by the seeker has been provided

    resume = db.ReferenceField(Resume)  # This field is populated by tagged resume that is clicked for feedback
    user = db.ReferenceField(User) # jobseeker
    volunteer = db.ReferenceField(User) # volunteer

    # These are the section fields
    first_section = db.EmbeddedDocumentField(_Section)
    second_section = db.EmbeddedDocumentField(_Section)
    third_section = db.EmbeddedDocumentField(_Section)
    fourth_section = db.EmbeddedDocumentField(_Section)
    fifth_section = db.EmbeddedDocumentField(_Section)

    # Questions - set to zero by default
    first_question = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH,
                                    choices=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"))
    second_question = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH,
                                     choices=(CONSTANTS.CHOICE_ONE, CONSTANTS.CHOICE_TWO, CONSTANTS.CHOICE_THREE))
    third_question = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH,
                                     choices=(CONSTANTS.CHOICE_ONE, CONSTANTS.CHOICE_TWO, CONSTANTS.CHOICE_THREE))

    thank_you_message = db.BooleanField(default=False)
