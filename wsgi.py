import os

# Import the main app
from resumeme import app

# Import Blueprint modules
from resumeme.notes.controllers import notes_app
from resumeme.accounts.controllers import accounts_flask_login
from resumeme.core.controllers import core

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(notes_app)
app.register_blueprint(accounts_flask_login)

# start the server
if __name__ == "__main__":
    app.run()
