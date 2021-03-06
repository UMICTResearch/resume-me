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

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(accounts)
app.register_blueprint(resume)
app.register_blueprint(feedback)
app.register_blueprint(utils)
app.register_blueprint(admin)


# start the server
if __name__ == "__main__":
    app.run()
