#
# Copyright SIG - June 2015
#

from app import app
from logger import logger

if __name__ == "__main__":
    logr = logger('./Logs', 'resume-feedback-dev', insertDate=False)
    app.run(host='0.0.0.0', port=4999, debug=True)  #
    # else:
    #     # init logger
    #     app.wsgi_app = ProxyFix(app.wsgi_app)
    #     logr = logger('./Logs', 'resume-feedback-server', insertDate=False)
