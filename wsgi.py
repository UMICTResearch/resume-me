import os

# Import the main app
from resumeme import app

# Import Blueprint modules
from resumeme.core.controllers import core
from resumeme.accounts.controllers import accounts_flask_login
from resumeme.resume.controllers import resume
from resumeme.feedback.controllers import feedback

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(accounts_flask_login)
app.register_blueprint(resume)
app.register_blueprint(feedback)

# start the server
if __name__ == "__main__":
    app.run()
