from resumeme import db

from question import Question
from survey import Survey

from resumeme.feedback.configs.section import MAX_SECTION_RATING, MAX_SECTION_LENGTH

# Each instance contains one section of a resume, its name, and content.
class Section(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # The maximum rating a section can have (min. is always 1)
    max_section_rating = MAX_SECTION_RATING
    # The section design - a section is essentially a question asked.
    section_question = db.EmbeddedDocumentField(Question)
    # Section rating value selected by user
    section_rating = db.StringField(max_length=MAX_SECTION_RATING, required=True)
    # The actual response of the volunteer
    section_response = db.StringField(max_length=MAX_SECTION_LENGTH)
    # Review of the specific section by the seeker; this can be a single survey question or it can
    # be a list of survey questions that were answered in relation to the specific section.
    review_list = db.EmbeddedDocumentListField(Survey)


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

    def review_list_question_group(self):
        return 'section_review'



    # TODO: Function to load a full list of section_review questions.
    #
    def __load_section_review_questions(self):
        # Initialize the list by adding the data from the all_questions configuration.
        # When the users answer their replies based on what is enabled at the time get filled in.
        pass

    # This takes the review specific to the section that the job seeker gives (text, selected choices, etc.)
    # and adds them to the survey list. First it adds the survey question to the Survey object.
    # Then the actual review content.
    def add_review_to_section(self, review_data, question_id):
        self.review_list.append(Survey())
        self.review_list[-1].create_survey_question(self.review_list_question_group(), question_id)
        self.review_list[-1].add_review_to_survey(review_data)


    def print_section(self):
        print("----SECTION----")
        print("%s <----(max_section_rating)" % self.max_section_rating)
        self.section_question.print_question()
        print("%s <----(section_rating)" % self.section_rating)
        print("%s <----(section_response)" % self.section_response)
        for index, review in enumerate(self.review_list):
            print("----(review_list[%i])----" % index)
            review.print_survey()
