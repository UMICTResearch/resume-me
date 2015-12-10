from resumeme import db
import resumeme.feedback.config as CONFIG
import resumeme.feedback.constant as CONSTANT
import resumeme.feedback.utils as UTIL

from resumeme.accounts.models import User

from section import Section
from survey import Survey

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
    feedback_sections = []
    # Seeker interface to provide a review of the volunteer, note this is a type of Survey.
    review_questions = []
    # volunteer - This is not just a link to the volunteer providing feedback but is also used to determine if
    # that particular volunteer can see the resume because they are one of the people under the threshhold
    volunteer = db.ReferenceField(User)


    # TODO: INITIALIZATION Methods
    # TODO: (Implement) -- 4) Save to Database (will have the try-except statement)
    # TODO: (Implement) -- 5) Fill all Survey answers as received by user (map to the current enabled and unlocked
    # TODO:                   sections) - this will receive the data as a giant block
    # TODO: (Implement) -- 6) Fill all Section answers as received by user (map to the current enabled sections)
    # TODO:                   this will receive the data as a giant block
    def __init__(self):
        super(Feedback, self).__init__()
        self.update_review_questions()
        self.update_feedback_sections()


    # ---------------------------------------------------------------------------------------------------------
    # Knowing the relevant question group that is referred to in the all_questions variable in the config file
    def feedback_sections_question_group(self):
        return "section"

    def review_questions_question_group(self):
        return "review"

    # Way to know which volunteer worked on this resume data
    def link_volunteer(self, user):
        self.volunteer = user


    # ---------------------------------------------------------------------------------------------------------
    # NOTE: This is where the question_group and question_id come from.
    #
    # TODO: (Verify) If it is an object created by the database query it should load the data automatically also.
    # TODO: (Implement) If it doesn't then we will need to call it after we set a variable equal to the returned object.
    def update_review_questions(self):
        group = self.review_questions_question_group()
        # all_questions is a Dict object
        sorted_question_list = UTIL.get_question_group_config_list(group)
        for id, value in enumerate(sorted_question_list):
            if  self.review_questions.count(self) <= id:
                self.append_to_review_questions(str(id))

            self.review_questions[id].update_survey_enable_state(group, str(id))

    def update_feedback_sections(self):
        group = self.feedback_sections_question_group()
        # all_questions are a Dict object so we use the UTIL functions to get data from the file
        # to allow us to ignore that and treat it more or less like a list.
        sorted_question_list = UTIL.get_question_group_config_list(group)
        for id, value in enumerate(sorted_question_list):
            if self.feedback_sections.count(self) <= id:
                self.append_to_feedback_sections(str(id))

            self.feedback_sections[id].update_section_enable_state(str(id))

    # This creates the section and then appends it to the list of resume sections
    def append_to_feedback_sections(self, question_id):
        section = Section()
        section.create_section_question(question_id)
        self.feedback_sections.append(section)

    def append_to_review_questions(self, question_id):
        survey = Survey()
        survey.create_survey_question(self.review_questions_question_group(), question_id)
        self.review_questions.append(survey)


    # ---------------------------------------------------------------------------------------------------------
    # Once viewed, the new flag disappears (that is simply a logic test). However, this function also locks the
    # feedback from further alterations by the volunteers. As such, it sets the feedback_lock variable.
    def feedback_has_been_viewed(self):
        self.viewed = True
        lock_feedback()

    # Lock Controls
    def lock_review():
        self._set_lock(self.review_questions_question_group, True)

    def lock_feedback():
        self._set_lock(self.feedback_sections_question_group, True)

    def unlock_review():
        self._set_lock(self.review_questions_question_group, False)

    def unlock_feedback():
        self._set_lock(self.feedback_sections_question_group, False)

    # Internal lock mechanism
    def _set_lock(self, lock_name, lock_state):
        if lock_name == self.feedback_section_question_group():
            self.feedback_lock = lock_state
        elif lock_name == self.review_question_question_group():
            self.review_lock = lock_state
        else:
            # nothing (this is an error)
            pass



    meta = {'allow_inheritance': True}
