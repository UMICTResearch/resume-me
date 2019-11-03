from datetime import datetime
from flask_script import Manager

from resumeme import app

from resumeme.accounts.models import User
from resumeme.resume.models import Resume
from resumeme.utils.controllers import send_mail

manager = Manager(app)


@manager.command
def notify_volunteers():
    if list_resumes:
        user_objects = User.objects
        for user in user_objects:
            if user.role == 'volunteer':
                send_mail('Volunteers Needed', user.email, 'notify_volunteers', user=user)


def list_resumes():
    resume_objects = Resume.objects
    time_now = datetime.now()

    for resume in resume_objects:
        time_delta = time_now - resume.last_updated
        time_delta_minutes = int(time_delta.total_seconds() / 60)
        if time_delta_minutes < 1440:
            return True


if __name__ == "__main__":
    manager.run()
