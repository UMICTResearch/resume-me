import boto3

ENV = 'dev'
EXTERNAL_QUESTION = """\
<?xml version="1.0" encoding="UTF-8"?>
<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
  <ExternalURL>https://beta.review-me.us/mturk</ExternalURL>
  <FrameHeight>0</FrameHeight>
</ExternalQuestion>
"""
WORKER_REQUIREMENTS = [{
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'RequiredToPreview': True,
}]

boto3_session = boto3.Session()
boto3_client = boto3_session.client(
    'mturk',
    endpoint_url=
        'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
        if ENV == 'dev' else
        'https://mturk-requester.us-east-1.amazonaws.com',
)

response = boto3_client.create_hit(
    MaxAssignments=1,
    AutoApprovalDelayInSeconds=10,
    LifetimeInSeconds=60,
    AssignmentDurationInSeconds=600,
    Reward='0.1',
    Title='review-me',
    Keywords='resume, review, rate',
    Description='Please review resume, rate it and give feedback',
    Question=EXTERNAL_QUESTION,
    QualificationRequirements=WORKER_REQUIREMENTS,
)