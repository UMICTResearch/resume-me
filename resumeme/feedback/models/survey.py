from resumeme import db
from models.question import Question


# Each instance contains one survey question (instance), its response and meta-data.
class Survey(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # This locks this question if a seeker has responded.
    survey_lock = db.BoolField(default=False)
    # The Question (Model)
    survey_question = db.EmbeddedField(Question)
    # The actual response of the job seeker (stored in the survey not the question)
    # This is simple a list of strings. So if it is a single large text field the list
    # only has one entry. If it is a list of multiple selections then it is a list
    # of strings each being one of the answers selected. E.g. Select top three
    # favorite job sites from list of 10 below.
    #
    # Question type will have to be checked to know how to interpret this.
    response = db.ListField(db.StringField())


    # Instantiates and populates the survey question from the file.
    def create_survey_question(self, question_group, question_id):
        self.survey_question = Question()
        self.survey_question.create_question_from_file(question_group, question_id)


    # Appends whatever is passed, whether it is a string or a list of strings (only for multi-choice questions).
    # In practice, this will really just be a single value appended whether it is a string or a list of strings.
    # It won't be called multiple times as there is only one question ever.
    def append_response(self, response_data):
        self.response.append(response_data)


    #  Question type will help whatever calls it to figure out how to interpret the data.
    def get_response(self):
        return self.response


    # Once the survey is completed and submitted it is locked on a per question basis.
    # If it is not locked (and the question config file says it is enabled) it can appear in a survey as needed.
    def lock_survey(self):
        self.set_survey_lock(True)

    def unlock_survey(self):
        self.set_survey_lock(False)

    def set_survey_lock(self, lock_state):
        self.survey_lock = lock_state


