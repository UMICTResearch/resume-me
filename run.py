#
# Copyright SIG - June 2015
#

from app import application
from logger import logger

if __name__ == "__main__":
    logr = logger('./Logs', 'resume-feedback-dev', insertDate=False)
    application.run(host='0.0.0.0', port=4500, debug=True)  #
    # else:
    #     # init logger
    #     application.wsgi_application = ProxyFix(application.wsgi_application)
    #     logr = logger('./Logs', 'resume-feedback-server', insertDate=False)
