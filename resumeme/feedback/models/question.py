from resumeme import db
import resumeme.feedback.configs.question as CONFIG


# This is the bare model of the question as read from the Config file.
class Question(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # The grouping in the config file: "section" or "survey" at the moment
    question_group = db.StringField(default=CONFIG.UNSET)
    # The question id number in file, this is both an entry which is the same as the list index.
    question_id = db.IntField(default=CONFIG.UNSET)
    # The question string
    question_text = db.StringField(default=CONFIG.UNSET, max_length=CONFIG.MAX_QUESTION_LENGTH)
    # Type: Single (User makes one selection), Multiple (User makes multiple selections) or Text Content
    question_type = db.IntField(default=CONFIG.UNSET,
                                choices=(CONFIG.UNSET, CONFIG.SINGLE, CONFIG.MULTIPLE, CONFIG.TEXT))
    # Actual choices text such as "Yes", "No", etc. Length of this is simple the total choice count.
    question_choices = db.ListField(db.StringField())
    # If it is enabled, question will appear on survey page. If it is disabled it will not.
    # It is disabled (enabled = False) when Config file says it is.
    question_enabled = db.BooleanField(default=False)


    # This is used to essentially load an appropriate question from the config file. For objects retrieved from
    # the database simply assign the returned object to a variable and treat that like a Question object. That would
    # essentially load an object from the database. This would iteratively generate the questions that are valid
    # in the templates.
    def create_question_from_file(self, question_group, question_id):
        self.__set_question_group(question_group)
        self.__set_question_id(question_id)
        self.set_question_text(CONFIG.all_questions[self.question_group][int(self.question_id)]['text'])
        self.set_question_type(CONFIG.all_questions[self.question_group][int(self.question_id)]['type'])
        self.set_question_choices(CONFIG.all_questions[self.question_group][int(self.question_id)]['choices'])
        self.__set_question_enabled(CONFIG.all_questions[self.question_group][int(self.question_id)]['enabled'])


    # Anything private is set by the config file whenever another class needs it to be or it itself needs it to
    # be set.
    def __set_question_group(self, question_group):
        self.question_group = question_group


    def __set_question_id(self, question_id):
        self.question_id = question_id


    def set_question_text(self, question_text):
        self.question_text = question_text


    def set_question_type(self, question_type):
        self.question_type = question_type


    def set_question_choices(self, question_choices):
        self.question_choices = list(question_choices)


    def __set_question_enabled(self, enabled):
        self.question_enabled = enabled
