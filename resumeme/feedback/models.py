from resumeme import db
from resumeme.accounts.models import User
import constants as CONSTANTS
import configs as CONFIGS

from models.question import Question
from models.section import Section
from models.survey import Survey
from models.feedback import Feedback

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
