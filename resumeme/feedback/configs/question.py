from resumeme.feedback.constants.question import *

# Config of the sections and the survey questions. This is a configuration file that will be changed by the
# admin console.
all_questions = {
    # Section design which determines what the volunteer see.
    'section' : [
        # Question
        {
            'id' : "0",
            'text' : "Experience",
            'type' : TEXT,
            'choices' : NO_CHOICES,
            'enabled' : True
        },
        # Question
        {
            'id' : "1",
            'text' : "Education",
            'type' : SINGLE,
            'choices' : ["good", "bad"],
            'enabled' : True
        }
    ],

    # These questions pertain to specific sections. Same set applies to all questions.
    'section_review' : [
        # Question
        {
            'id' : '0',
            'text' : "Did this section contain sufficient detail?",
            'type' : SINGLE,
            'choices' : ["yes", "no"],
            'enabled' : True
        }
    ],

    # General survey questions that can be sent to everyone.
    'survey' : [
        # Question
        {
            'id' : '0',
            'text' : "Would you recommend this site to friends?",
            'type' : SINGLE,
            'choices' : ["yes", "no"],
            'enabled' : True
        }
    ],

    # General review questions that can be sent out to the job seekers.
    'review' : [
        # Question
        {
            'id' : '0',
            'text' : "Was the feedback actionable?",
            'type' : SINGLE,
            'choices' : ["yes", "no"],
            'enabled' : True
        },
        # Question
        {
            'id' : '1',
            'text' : "How would you rate the feedback?",
            'type' : SINGLE,
            'choices' : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            'enabled' : False
        }
    ]
}
