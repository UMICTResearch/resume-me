from resumeme import db
from resumeme.accounts.models import User
import constants as CONSTANTS
import configs as CONFIGS

from models.question import Question
from models.section import Section
from models.survey import Survey
from models.feedback import Feedback

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
    job_seeker = db.ReferenceField(User)

