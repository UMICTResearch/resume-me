#
# Copyright SIG - June 2015
#

from app import app
from logger import logger

if __name__ == "__main__":
    logr = logger('./Logs', 'resume-feedback-dev', insertDate=False)
    app.run()
