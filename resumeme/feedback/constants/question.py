# This is a constants file as used by the question model. This is not controlled by the admin console but has
# to be changed directly in the code.

# Bounds
MAX_RATING_LENGTH = 1
MAX_QUESTION_LENGTH = 1024

# Question Type: Choice selections i.e. SINGLE choice, select MULTPLE choices, or fill in TEXT
TEXT = 0
SINGLE = 1
MULTIPLE = 2
NO_CHOICES = ["no_choices"]

# Content Field (to ensure that they put at least an "ok" and also to prevent blank submissions)
MIN_CONTENT_LENGTH = 2

