# An improbable value to determine if a variable in the classes is set correctly
UNSET = -1

# Bounds
MAX_RATING_LENGTH = 1
MAX_QUESTION_LENGTH = 1024

# Question Type: Choice selections i.e. SINGLE choice, select MULTPLE choices, or fill in TEXT
TEXT = 0
SINGLE = 1
MULTIPLE = 2
NO_CHOICES = "no_choices"

# Config of the sections and the survey questions
all_questions = {
    'section' : [
        # Question
        {
            'id' : '00000',
            'text' : "Experience",
            'type' : TEXT,
            'choices' : NO_CHOICES,
            'enabled' : True
        },
        # Question
        {
            'id' : '00001',
            'text' : "Education",
            'type' : TEXT,
            'choices' : NO_CHOICES,
            'enabled' : True
        }
    ],

    'survey' : [
        # Question
        {
            'id' : '00000',
            'text' : "Was the feedback actionable?",
            'type' : SINGLE,
            'choices' : ("yes", "no"),
            'enabled' : True
        },
        # Question
        {
            'id' : '00001',
            'text' : "How would you rate the feedback?",
            'type' : SINGLE,
            'choices' : ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
            'enabled' : False
        }
    ]
}
