import os

# Import the main app
from resumeme import app

# Import Blueprint modules
from resumeme.core.controllers import core
from resumeme.accounts.controllers import accounts
from resumeme.resume.controllers import resume
from resumeme.feedback.controllers import feedback
from resumeme.utils.controllers import utils
from resumeme.admin.controllers import admin

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(accounts)
app.register_blueprint(resume)
app.register_blueprint(feedback)
app.register_blueprint(utils)
app.register_blueprint(admin)

import resumeme
import unittest
import tempfile
import test_feedback_testdata as TEST_DATA
import resumeme.feedback.constant as CONSTANT
import resumeme.feedback.config as CONFIG
import resumeme.feedback.constants.question as question_constant
import resumeme.feedback.models.question as question_model
import resumeme.feedback.models.survey as survey_model
import resumeme.feedback.configs.section as section_config
import resumeme.feedback.models.section as section_model
import resumeme.feedback.models.feedback as feedback_model
import resumeme.feedback.utils as UTILS


class ResumeMeTestCase(unittest.TestCase):

    def setUp(self):
        resumeme.app.config['MONGODB_SETTINGS'] = { 'DB' : tempfile.mkstemp() }
        self.db_fd, resumeme.app.config['DATABASE'] = tempfile.mkstemp()
        resumeme.app.config['TESTING'] = True
        self.app = resumeme.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(resumeme.app.config['DATABASE'])

## Extra utility functions inherited from base object class and in turn inherited by all test classes.
#
class TestingUtils(ResumeMeTestCase, object):

    def _question_assertEqual(self, question_object, group, index):
        self.assertEqual((question_object.question_group, question_object.question_id,
                          question_object.question_text,
                          question_object.question_type,
                          question_object.question_choices,
                          question_object.question_enabled),
                         (group, index,
                          CONFIG.all_questions[group][index]['text'],
                          CONFIG.all_questions[group][index]['type'],
                          CONFIG.all_questions[group][index]['choices'],
                          CONFIG.all_questions[group][index]['enabled']))

    # Checks to make sure that a question object matches the file content.
    def _survey_compare_assertEqual(self, survey_block, sorted_file_config_list, group, index):
        self.assertEqual(survey_block.survey_lock, sorted_file_config_list['enabled'])
        self._question_assertEqual(survey_block.survey_question, group, str(index))

    # Compares the feedback_sections
    def _feedback_sections_compare_assertEqual(self, section_block, sorted_file_config_list, group, index):
        self.assertEqual(section_block.section_enabled, sorted_file_config_list[1]['enabled'])

        for id, value in enumerate(sorted_file_config_list):
            self._survey_compare_assertEqual(section_block.review_list[id], sorted_file_config_list[id],
                                             group, index)

    # Returns True if content of two arrays are completely identical else returns False.
    def _compare_arrays_equal(self, original, copy):
        for i in range(len(original)):
            if original[i] != copy[i]:
                return False
        return True

    def _compare_simple_list(L1, L2):
        return len(L1) == len(L2) and sorted(L1) == sorted(L2)


## Question Testing
#
class TestQuestion(TestingUtils):

    def test_create_question_from_file(self):

        for group in TEST_DATA.group_index:
            sorted_list = list(sorted(CONFIG.all_questions[group].items()))

            for id, value in enumerate(sorted_list):
                q = question_model.Question()
                q.create_question_from_file(group, str(id))
                self._question_assertEqual(q, group, str(id))

            for id, value in enumerate(sorted_list):
                self._question_assertEqual(q, group, str(id))


## Survey Testing
#
class TestSurvey(TestingUtils):

    def _create_survey_question_assertEqual(self):

        for group in TEST_DATA.group_index:
            sorted_list = list(sorted(CONFIG.all_questions[group].items()))

            for id, value in enumerate(sorted_list):
                s = survey_model.Survey()
                s.create_survey_question(group, str(id))
                self._question_assertEqual(s.survey_question, group, str(id))

            for id, value in enumerate(sorted_list):
                self._question_assertEqual(s.survey_question, group, str(id))

    def test_add_review_to_survey(self):
        review = [ "Good work.", "This is not bad.", "Wonderful." ]
        s = survey_model.Survey()

        s.add_review_to_survey(review[0])
        self.assertTrue(self._compare_arrays_equal(review[0:1], s.review))
        s.add_review_to_survey(review[1])
        self.assertTrue(self._compare_arrays_equal(review[0:2], s.review))
        s.add_review_to_survey(review[2])
        self.assertTrue(self._compare_arrays_equal(review, s.review))


## Section Testing
#
class TestSection(TestingUtils):

    def test_review_list_question_group(self):
        s = section_model.Section()
        self.assertEqual(s.review_list_question_group(), "section_review")


    def test_create_section_question(self):
        group = "section"

        sorted_list = list(sorted(CONFIG.all_questions[group].items()))
        for id, value in enumerate(sorted_list):
            s = section_model.Section()
            s.create_section_question(str(id))
            self._question_assertEqual(s.section_question, group, str(id))

        for id, value in enumerate(sorted_list):
            self._question_assertEqual(s.section_question, group, str(id))


    def test_append_survey_to_review_list(self):
        group = 'section_review'

        sorted_list = list(sorted(CONFIG.all_questions[group].items()))
        for id, value in enumerate(sorted_list):
            s = section_model.Section()
            s.append_survey_to_review_list(str(id))
            self._survey_compare_assertEqual(s.review_list[id], CONFIG.all_questions[group][str(id)], group, id)

        for id, value in enumerate(sorted_list):
            self._survey_compare_assertEqual(s.review_list[id], CONFIG.all_questions[group][str(id)], group, id)


    def test_insert_single_review_into_review_list(self):
        group = 'section_review'

        sorted_list = list(sorted(CONFIG.all_questions[group].items()))
        for id, value in enumerate(sorted_list):
            s1 = section_model.Section()
            s1.append_survey_to_review_list(str(id))
            s1.insert_single_review_into_review_list(TEST_DATA.short_test_data, str(id))
            self.assertEqual(s1.review_list[id].review[0], TEST_DATA.short_test_data)

        for id, value in enumerate(sorted_list):
            self.assertEqual(s1.review_list[id].review[0], TEST_DATA.short_test_data)

        for id, value in enumerate(sorted_list):
            s2 = section_model.Section()
            s2.append_survey_to_review_list(str(id))
            s2.insert_single_review_into_review_list(TEST_DATA.long_test_data, str(id))
            # TODO: Eventually expand this to handle testing more than one selection (i.e. not just [0]
            self.assertEqual(s2.review_list[id].review[0], TEST_DATA.long_test_data)

        for id, value in enumerate(sorted_list):
            self.assertEqual(s2.review_list[id].review[0], TEST_DATA.long_test_data)


    def test___init_and_update_section_review_list(self):
        s = section_model.Section()
        group = 'section_review'
        sorted_list = list(sorted(CONFIG.all_questions[group].items()))
        for id, value in enumerate(sorted_list):
            self._survey_compare_assertEqual(s.review_list[id], CONFIG.all_questions[group][str(id)], group, id)


## Feedback Testing
#
class TestFeedback(TestingUtils):

    def test_update_feedback_sections(self):
        f = feedback_model.Feedback()

        group = 'review'
        sorted_list = list(sorted(CONFIG.all_questions[group].items()))

        for id, value in enumerate(sorted_list):
            self._survey_compare_assertEqual(f.review_questions[id], sorted_list, group, id)

        group = 'section'
        for id, value in enumerate(sorted_list):
            self._feedback_sections_compare_assertEqual(f.feedback_sections[id], sorted_list, group, id)






## Basic main function
#
if __name__ == '__main__':
    unittest.main()
