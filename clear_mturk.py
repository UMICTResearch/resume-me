import boto3

ENV = 'dev'

boto3_session = boto3.Session()
boto3_client = boto3_session.client(
    'mturk',
    endpoint_url=
        'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
        if ENV == 'dev' else
        'https://mturk-requester.us-east-1.amazonaws.com',
)

response = boto3_client.list_reviewable_hits()
HITs = response['HITs']
for HIT in HITs:
    assignments = boto3_client.list_assignments_for_hit(
        HITId=HIT['HITId'],
        AssignmentStatuses=['Submitted'],
    )['Assignments']
    for assignment in assignments:
        boto3_client.approve_assignment(
            AssignmentId=assignment['AssignmentId'],
        )
    boto3_client.delete_hit(
        HITId=HIT['HITId']
    )