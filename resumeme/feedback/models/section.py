from resumeme import db
from resumeme.accounts.models import User
import constants as CONSTANTS
import configs as CONFIGS

from models.question import Question
from models.survey import Survey

# Each instance contains one section of a resume, its name, and content.
class Section(db.EmbeddedDocument)
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # The maximum rating a section can have (min. is always 1)
    max_rating = db.IntField(default=int(MAX_SECTION_RATING), choices=(MAX_SECTION_RATING))
    # The section design - a section is essentially a question asked.
    section_question = db.EmbeddedField(Question)
    # Section rating value
    rating = db.StringField(max_length=CONSTANTS.MAX_RATING_LENGTH, required=True)
    # The actual response of the volunteer
    response = db.StringField(max_length=CONSTANTS.MAX_SURVEY_LENGTH)
    # Review of the specific section by the seeker; this can be a single survey question or it can
    # be a list of survey questions that were answered in relation to the specific section.
    review_list = db.EmbeddedDocumentFieldList(Survey)


    def create_section_from_file(self, question_group, question_id):
        self.section_question = Question()
        self.section_question.create_question_from_file(question_group, question_id)


    def get_question_group(self):
        return self.section_question.question_group

    def get_question_id(self):
        return self.section_question.question_id


    # This is the feedback response and section rating
    def add_response(self, response):
        self.response = response

    def add_rating(self, rating):
        self.rating = rating


    def append_review(self, response):
        survey = Survey()
        self.review_list.append(
            survey.create_survey_question(self, self.get_question_group(), self.get_question_id()))



