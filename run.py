import os

# Import the main app
from resumeme import app

# Import Blueprint modules
from resumeme.core.controllers import core
from resumeme.accounts.controllers import accounts
from resumeme.resume.controllers import resume
from resumeme.feedback.controllers import feedback
from resumeme.utils.controllers import utils
from resumeme.admin.controllers import admin
from resumeme.mturk.controllers import mturk

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(accounts)
app.register_blueprint(resume)
app.register_blueprint(feedback)
app.register_blueprint(utils)
app.register_blueprint(admin)
app.register_blueprint(mturk)



# start the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4500, debug=True)
