from resumeme import db
from resumeme.accounts.models import User

from models.section import Section
from models.survey import Survey

# Contains the Feedback provided
class Feedback(db.EmbeddedDocument):
    # Version to keep track of model
    version = 1
    # Date it was submitted
    last_updated = db.DateTimeField()
    # Used to set feedback_lock and show the new feedback label. If False means it is still unviewed. On True
    # feedback_lock is set to True and the new flag disappears.
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

    # TODO: INITIALIZATION Methods
    # TODO: (Implement) -- 4) Save to Database
    # TODO: (Implement) -- 5) Fill all Survey answers as received by user (map to the current enabled and unlocked
    # TODO:                   sections)
    # TODO: (Implement) -- 6) Fill all Section answers as received by user (map to the current enabled sections)
    #
    def __init__(self):
        super(C,self).__init__(source)
        initialize_and_update()


    # NOTE: This is where the question_group and question_id come from in from the file
    #
    # TODO: (Verify) If it is an object created by the database query it should load the data automatically also.
    # TODO: (Implement) If it doesn't then we will need to call it after we set a variable equal to the returned object.
    #
    # TODO: (Implement) Enabled state should always be updated from the all_questions data
    def initialize_and_update(self):
        # Iterate through the blocks relevant to the model calling the append method appropriate for the data type.
        # Starting index for iterations changes based on whether it is a new creation (0) or an update (x).
        for question_id in all_questions[question_group][len(self.feedback_sections):]:
            self.append_to_feedback_section(question_group, question_id)
        for question_id in all_questions[question_group][len(self.feedback_sections):]:
            self.append_to_review_questions(question_group, question_id)


    # This creates the section and then appends it to the list of resume sections
    def append_to_feedback_section(self, question_group, question_id):
        section = Section()
        section.create_section_question(question_group, question_id)
        self.feedback_sections.append(section)


    def append_to_review_questions(self, question_group, question_id):
        survey = Survey()
        section.create_survey_question(question_group, question_id)
        self.review_questions.append(survey)


    def link_volunteer(self, user):
        self.volunteer = user


    # Once viewed, the new flag disappears (that is simply a logic test). However, this function also locks the
    # feedback from further alterations by the volunteers. As such, it sets the feedback_lock variable.
    def feedback_has_been_viewed(self):
        self.viewed = True
        lock_feedback()

    # Lock Controls
    def lock_review():
        self._set_lock("review", True)

    def lock_feedback():
        self._set_lock("feedback", True)

    def unlock_review():
        self._set_lock("review", False)

    def unlock_feedback():
        self._set_lock("feedback", False)

    # Internal lock mechanism
    def _set_lock(self, lock_name, lock_state):
        if lock_name == "feedback":
            self.feedback_lock = lock_state
        elif lock_name == "review":
            self.review_lock = lock_state
        else
            # nothing (this is an error)

