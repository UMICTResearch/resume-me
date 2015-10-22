import unittest
import resumeme.feedback_unittest_testdata as volunteer_input
import pprint
from resumeme import db
import resumeme.feedback.constant as CONSTANT
import resumeme.feedback.config as CONFIG
import resumeme.feedback.constants.question as question_constant
import resumeme.feedback.models.question as question_model
import resumeme.feedback.models.survey as survey_model
import resumeme.feedback.configs.section as section_config
import resumeme.feedback.models.section as section_model

import os
import resumeme
import unittest
import tempfile

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
    def _survey_compare_assertEqual(self, survey_model, survey_config, group, index):
        self.assertEqual(survey_model.survey_lock, survey_config['enabled'])
        self._question_assertEqual(survey_model.survey_question, group, index)

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
        q = question_model.Question()
        # These loops cherry pick the data to test based on the group_index dict
        for group, id in volunteer_input.group_index.iteritems():
            q.create_question_from_file(group, id)
            self._question_assertEqual(q, group, id)


## Survey Testing
#
class TestSurvey(TestingUtils):

    def _create_survey_question_assertEqual(self):
        s = survey_model.Survey()
        for group, id in volunteer_input.group_index.iteritems():
            s.create_survey_question(group, id)
            self._question_assertEqual(s.survey_question, group, id)

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
        s = section_model.Section()
        for group, id in volunteer_input.group_index.iteritems():
            s.create_section_question(group, id)
            self._question_assertEqual(s.section_question, group, id)

    def test_append_survey_to_review_list(self):
        s = section_model.Section()
        group = 'section_review'
        for id in CONFIG.all_questions[group]:
            s.append_survey_to_review_list(group, id)
            self._survey_compare_assertEqual(s.review_list[int(id)],
                                             CONFIG.all_questions[group][id], group, id)

    def test_insert_single_review_into_review_list(self):
        s = section_model.Section()
        group = 'section_review'
        for id in CONFIG.all_questions[group]:
            s.append_survey_to_review_list(group, id)
            if int(id) % 2 == 0:
                s.insert_single_review_into_review_list(volunteer_input.short_test_data, id)
                self.assertEqual(s.review_list[int(id)].review[0], volunteer_input.short_test_data)
            else:
                s.insert_single_review_into_review_list(volunteer_input.long_test_data, id)
                # TODO: Eventually expand this to handle testing more than one selection (i.e. not just [0]
                self.assertEqual(s.review_list[int(id)].review[0], volunteer_input.long_test_data)

    def test_initialize_and_update_section_review_list(self):
        s = section_model.Section()
        s.initialize_and_update_section_review_list()






## Basic main function
#
if __name__ == '__main__':
    unittest.main()
