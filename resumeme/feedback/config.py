# This is the main config file to add the list of questions.

# Need the information from the question configuration about what question types can be used.
from resumeme.feedback.configs.question import *

# Config of the sections and the survey questions. This is a configuration file that will be changed by the
# admin console.
all_questions = \
    {
        # Section design which determines what the volunteer see.
        'section' : {
            # Question
            '0' : #id
                {
                    'text' : "Experience",
                    'type' : TEXT,
                    'choices' : NO_CHOICES,
                    'enabled' : True
                },
            # Question
            '1' : #id
                {
                    'text' : "Skills",
                    'type' : TEXT,
                    'choices' : NO_CHOICES,
                    'enabled' : True
                },
            # Question
            '2' : #id
                {
                    'text' : "Education",
                    'type' : SINGLE,
                    'choices' : ["good", "bad"],
                    'enabled' : True
                },
        },

        # These questions pertain to specific sections. Same set applies to all questions.
        'section_review' : {
            # Question
            '0' : #id
                {
                    'text' : "Did the review of this section contain sufficient detail?",
                    'type' : SINGLE,
                    'choices' : ["yes", "no"],
                    'enabled' : True
                }
        },

        # General survey questions that can be sent to everyone.
        'survey' : {
            # Question
            '0' : #id
                {
                    'text' : "Would you recommend this site to friends?",
                    'type' : SINGLE,
                    'choices' : ["yes", "no"],
                    'enabled' : True
                }
        },

        # General review questions that can be sent out to the job seekers.
        'review' : {
            # Question
            '0' : #id
                {
                    'text' : "Was the feedback actionable?",
                    'type' : SINGLE,
                    'choices' : ["yes", "no"],
                    'enabled' : True
                },
            # Question
            '1' : #id
                {
                    'text' : "How would you rate the feedback?",
                    'type' : SINGLE,
                    'choices' : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                    'enabled' : False
                }
        }
    } # End of entire variable

