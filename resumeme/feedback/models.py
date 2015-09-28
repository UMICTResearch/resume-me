import datetime
from resumeme import db
from resumeme.accounts.models import User
from resumeme.resume.models import Resume
import constants as CONSTANTS


# This is the bare model of the question as read from the Config file.
class Question(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # The question string
    question_text = db.StringField(max_length=CONSTANTS.MAX_QUESTION_LENGTH)
    # Type: Single (User makes one selection), Multiple (User makes multiple selections) or Text Content
    type = db.IntField(choices=(CONSTANTS.SINGLE, CONSTANTS.MULTIPLE, CONSTANTS.TEXT))
    # Arbitrary count: 1 = Text field, 2 = Yes/No style, 10 = Rating style, etc.
    number_of_choices = db.IntField()
    # Actual choices text such as "Yes", "No", etc.
    choices = db.ListField(db.StringField())


# Each instance contains one survey question (instance), its response and meta-data.
class Survey(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # If it is enabled, question will appear on survey page. If it is disabled it will not.
    # It is disabled (enabled = False) when Config file says it is.
    survey_enabled = db.BoolField(default=False)
    # This locks this question if a seeker has responded and loads previous answer if enabled.
    survey_lock = db.BoolField(default=False)
    # The Question (Model)
    survey_question = db.EmbeddedField(Question)
    # The actual response of the seeker (stored in the survey not the question)
    response = db.StringField(max_length=CONSTANTS.MAX_SURVEY_LENGTH)


# Each instance contains one section of a resume, its name, and content.
class Section(db.EmbeddedDocument)
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # If it is enabled, section will appear on feedback page. If it is disabled it will not.
    # It is disabled (enabled = False) when Config file says it is.
    section_enabled = db.BoolField(default=False)
    # The section design - a section is essentially a question asked.
    section_question = db.EmbeddedField(Question)
    # Section rating
    rating = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH, choices=("1", "2", "3", "4", "5"), required=True)
    # The actual response of the volunteer
    response = db.StringField(max_length=CONSTANTS.MAX_SURVEY_LENGTH)
    # Review of the specific section by the seeker
    survey_question = db.EmbeddedDocumentFieldList(Survey)


# Contains the Feedback provided
class Feedback(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # Used to set feedback_lock and show the new feedback label.
    viewed = db.BooleanField(default=False)
    # Locked state means the feedback can't be updated anymore. This happens once the seeker has opened the feedback
    # and therefore viewed it or in other circumstances such as when a time limit for resume feedback has been reached.
    # Avoids infinitely open resume.
    feedback_lock = db.BooleanField(default=False)
    # Locked once a review by the seeker has been provided.
    review_lock = db.BooleanField(default=False)
    # Volunteer interface to provide Feedback with all the sections to fill out.
    feedback_sections = db.EmbeddedDocumentFieldList(Section)
    # Seeker interface to provide a review of the volunteer, note this is a type of Survey.
    review_questions = db.EmbeddedDocumentFieldList(Survey)
    # volunteer - This is not just a link to the volunteer providing feedback but is also used to determine if
    # that particular volunteer can see the resume because they are one of the people under the threshhold
    volunteer = db.ReferenceField(User)
    # jobseeker
    seeker = db.ReferenceField(User)


# This is the chain of Feedback documents that will be linked to
class FeedbackList(db.Document)
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # This determines how many more volunteers can provide feedback. Each new volunteer subtracts this count by
    # one and once it reaches zero no more volunteers can provide feedback.
    feedback_threshhold = db.IntField(default=3)
    # List of Feedbacks
    feedback_list = db.EmbeddedDocumentFieldList(Feedback)
    # This field is populated by tagged document that is clicked for feedback
    review_me_document = db.GenericReferenceField()
