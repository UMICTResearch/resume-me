import os

# Import the main app
from custom import app

# Import Blueprint modules
from custom.notes.controllers import notes_app
from custom.accounts.controllers import accounts_flask_login
from custom.core.controllers import core

# Register Blueprints modules
app.register_blueprint(core)
app.register_blueprint(notes_app)
app.register_blueprint(accounts_flask_login)

# start the server
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4500, debug=True)
