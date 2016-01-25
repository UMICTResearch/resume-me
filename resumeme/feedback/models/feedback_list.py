from resumeme import db
from resumeme.accounts.models import User

import resumeme.feedback.config
import resumeme.feedback.constant as CONSTANT

from resumeme.feedback.models.feedback import Feedback

# This is the chain of Feedback documents that will be linked to
class FeedbackList(db.Document):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # This determines how many more volunteers can provide feedback. Each new volunteer subtracts this count by
    # one and once it reaches zero no more volunteers can provide feedback.
    feedback_threshhold = CONSTANT.MAX_VOLUNTEER_PER_FEEDBACK
    # List of Feedbacks
    feedback_list = db.EmbeddedDocumentListField(Feedback)
    # This field is populated by tagged document that is clicked for feedback
    review_me_document = db.GenericReferenceField()
    # jobseeker
    job_seeker = db.ReferenceField(User)


    def append_object_to_feedback_list(self, feedback):
        self.feedback_list.append(feedback)
        self.feedback_threshhold = self.feedback_threshhold - 1


    def link_review_me_document(self, document):
        self.review_me_document = document


    def link_job_seeker(self, user):
        self.job_seeker = user


    def get_list(self):
        return self.feedback_list



    meta = {'allow_inheritance': True}

