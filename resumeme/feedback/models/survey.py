from resumeme import db
from question import Question


# Each instance contains one survey question (instance), its review data and meta-data.
class Survey(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # This locks this question if a seeker has responded.
    survey_lock = db.BooleanField(default=False)
    # The Question (Model)
    survey_question = db.EmbeddedDocumentField(Question)
    # The actual reply of the job seeker (stored in the survey not the question)
    # This is simple a list of strings. So if it is a single large text field the list
    # only has one entry. If it is a list of multiple selections then it is a list
    # of strings each being one of the answers selected. E.g. Select top three
    # favorite job sites from list of 10 below.
    #
    # Question type will have to be checked to know how to interpret this.
    review = db.ListField(db.StringField())


    # Instantiates and populates the survey question from the file.
    def create_survey_question(self, question_group, question_id):
        self.survey_question = Question()
        self.survey_question.create_question_from_file(question_group, question_id)


    # Appends whatever is passed, whether it is a string or a list of strings (only for multi-choice questions).
    # In practice, this will really just be a single value appended whether it is a string or a list of strings.
    # It won't be called multiple times as there is only one question ever.
    def add_review_to_survey(self, review_data):
        self.review.append(review_data)


    #  Question type will help whatever calls it to figure out how to interpret the data.
    def get_review(self):
        return self.review


    # Once the survey is completed and submitted it is locked on a per question basis.
    # If it is not locked (and the question config file says it is enabled) it can appear in a survey as needed.
    def lock_survey(self):
        self._set_survey_lock(True)

    def unlock_survey(self):
        self._set_survey_lock(False)

    def _set_survey_lock(self, lock_state):
        self.survey_lock = lock_state


    def print_survey(self):
        print("----SURVEY----")
        print("%s <----(survey_lock)" % self.survey_lock)
        self.survey_question.print_question()
        for index, item in enumerate(self.review):
            print("%s <----(review[%i])" % (item,  index))
