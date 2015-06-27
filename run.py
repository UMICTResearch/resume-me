#
# Copyright SIG - June 2015
#
import os

from resumeme import application
from logger import logger

#Get Blueprints
from resumeme.accounts import auth_flask_login

application.register_blueprint(auth_flask_login)

if __name__ == "__main__":
    logr = logger('./Logs', 'resume-feedback-dev', insertDate=False)
    application.run(host='0.0.0.0', port=4500, debug=True)  #
    # else:
    #     # init logger
    #     application.wsgi_application = ProxyFix(application.wsgi_application)
    #     logr = logger('./Logs', 'resume-feedback-server', insertDate=False)
