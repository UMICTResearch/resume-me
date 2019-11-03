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

response = boto3_client.list_hits()
num_hits = response['NumResults']
for HIT in response['HITs']:
    print('HITStatus: ' + HIT['HITStatus'])
    assignments = boto3_client.list_assignments_for_hit(
        HITId=HIT['HITId'],
        AssignmentStatuses=['Submitted'],
    )['Assignments']
    print(assignments)
    for assignment in assignments:
        print('AssignmentStatus: ' + assignment['AssignmentStatus'])