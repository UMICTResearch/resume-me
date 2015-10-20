import unittest
import pprint
from resumeme import db
import resumeme.feedback.constant
import resumeme.feedback.config
import resumeme.feedback.constants.question as q_const
import resumeme.feedback.configs.question as q_conf
import resumeme.feedback.models.question as q_mod
import resumeme.feedback.models.survey as y_mod
import resumeme.feedback.configs.section as s_conf
import resumeme.feedback.models.section as s_mod


class TestQuestion(unittest.TestCase):

    def SetUp(self):
        pass

    def _create_question_from_file_assertEqual(self, g, i):
        q = q_mod.Question()
        q.create_question_from_file(g, i)
        self.assertEqual((q.question_group,
                          q.question_id,
                          q.question_text,
                          q.question_type,
                          q.question_choices,
                          q.question_enabled),
                         (g,
                          i,
                          q_conf.all_questions[g][i]['text'],
                          q_conf.all_questions[g][i]['type'],
                          q_conf.all_questions[g][i]['choices'],
                          q_conf.all_questions[g][i]['enabled'],
                          ))

    def test_create_question_from_file(self):
        self._create_question_from_file_assertEqual("section", 0)
        self._create_question_from_file_assertEqual("section_review", 0)
        self._create_question_from_file_assertEqual("survey", 0)
        self._create_question_from_file_assertEqual("review", 1)

if __name__ == '__main__':
    unittest.main()
