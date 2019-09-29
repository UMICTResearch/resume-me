# Rating Field 
MAX_RATING_LENGTH = 1

# Content Field 
MIN_CONTENT_LENGTH = 2

# Section Field
LEGACY_SECTION = "Overall Feedback"
FIRST_SECTION = "Overall, the skills and experience listed on this resume match the job description specified."
SECOND_SECTION = "Formatting Issues"
THIRD_SECTION = "Education"
FOURTH_SECTION = "Experience"
FIFTH_SECTION = "Skills/Misc"
MAX_SECTION_NAME_LENGTH = 128

# Simple numbers to represent the values
#
CHOICE_ONE = "1"
CHOICE_TWO = "2"
CHOICE_THREE = "3"

SECTION_CHOICE_ONE = "1"
SECTION_CHOICE_TWO = "2"
SECTION_CHOICE_THREE = "3"

EXTERNAL_QUESTION = """\
<?xml version="1.0" encoding="UTF-8"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
  <ExternalURL>https://review-me.us/mturk</ExternalURL>
  <FrameHeight>0</FrameHeight>
</ExternalQuestion>
"""

WORKER_REQUIREMENTS = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'RequiredToPreview': True,
}]