from resumeme import db
import resumeme.feedback.config as CONFIG
import resumeme.feedback.constant as CONSTANT

import resumeme.feedback.configs.section as SECTION_CONFIG

from question import Question
from survey import Survey


# Each instance contains one section of a resume, its name, and content.
class Section(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # The maximum rating a section can have (min. is always 1)
    max_section_rating = SECTION_CONFIG.MAX_SECTION_RATING
    # The section design - a section is essentially a question asked.
    section_question = db.EmbeddedDocumentField(Question)
    # Section rating value selected by user
    section_rating = db.StringField(max_length=SECTION_CONFIG.MAX_SECTION_RATING)
    # The actual response of the volunteer
    section_response = db.StringField(max_length=SECTION_CONFIG.MAX_SECTION_LENGTH)
    # Review of the specific section by the seeker; this can be a single survey question or it can
    # be a list of survey questions that were answered in relation to the specific section.
    # review_list = db.EmbeddedDocumentListField(Survey)
    review_list = []


    # This makes sure the review_list is up to date with the config file. However, the section_question is
    # not handled by initialization yet. It can be in the future but currently the other classes handle it
    # by using the create functions directly.
    def __init__(self):
        super(Section, self).__init__()
        self.initialize_and_update_section_review_list()

    # Knowing the relevant question group that is referred to in the all_questions variable in the config file
    def review_list_question_group(self):
        return 'section_review'


    # Note that this is the section question. Essentially what the volunteer answers regarding the
    # resume. Such as "Experience", "Overall Skills", etc. Here you create the section based on the
    # group and id passed which are in-turn based on the config file.
    def create_section_question(self, question_group, question_id):
        self.section_question = Question()
        self.section_question.create_question_from_file(question_group, question_id)


    # Simply adding the rating value to the model.
    def add_section_rating(self, section_rating):
        self.section_rating = section_rating

    # Simply adding the volunteer response to the model.
    def add_section_response(self, section_response):
        self.section_response = section_response


    # TODO: (Implement) -- 1) Fill all Survey answers as received by user (map to the current enabled and unlocked
    # TODO:                   sections)

    # This adds the entire block of survey questions to the review_list and makes sure they are up to date.
    # TODO: Move this functionality into Question with regards to getting list of new questions back to
    # TODO: Append.
    def initialize_and_update_section_review_list(self):
        # Initialize the list by adding the data from the all_questions configuration.
        # Iterate through the blocks relevant to the model calling the append method.
        # Starting index for iterations changes based on whether it is a new creation (0) or an update (x).
        question_group = self.review_list_question_group()
        # all_questions is a Dict object
        for question_id in CONFIG.all_questions[question_group]:
            # Add new survey question to the List if the index number which is also question_id is not present.
            # This is determined by the length of the list hence <= determines it. Self in count needed due to
            # this being called in init function.
            if self.review_list is None or int(question_id) <= self.review_list.count(self):
                self.append_survey_to_review_list(question_group, question_id)
            # Question ID winds up being equal to the array index values; enable and disable as needed
            if CONFIG.all_questions[question_group][question_id]['enabled'] == True:
                self.review_list[int(question_id)].enable_survey()
            elif CONFIG.all_questions[question_group][question_id]['disabled'] == True:
                self.review_list[int(question_id)].disable_survey()



    # This creates the Survey and then appends it to the list of resume sections ensuring one Survey is added.
    def append_survey_to_review_list(self, question_group, question_id):
        review = Survey()
        review.create_survey_question(question_group, question_id)
        self.review_list.append(review)

    # This takes a single Survey review and inserts it into a survey list item in review_list
    def insert_single_review_into_review_list(self, review_data, question_id):
        self.review_list[int(question_id)].add_review_to_survey(review_data)

