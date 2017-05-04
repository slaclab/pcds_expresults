from flask import Flask, current_app
import logging
import sys

from config import EXP_RESULTS_FOLDER, DEBUG
from context import app, roles_db, security
from pages import pages_blueprint

__author__ = 'mshankar@slac.stanford.edu'


# Initialize application.
app = Flask(__name__)
app.secret_key = "Create a temporary secret key that is unique to this application."
app.debug = DEBUG

if DEBUG:
    print "Sending all debug messages to the console"
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


# Set the expiration for static files to 60 seconds; consider changing this later.
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60; 

# Register routes.
app.register_blueprint(pages_blueprint, url_prefix="")

# Initialize any MySQL connectors here.
# The init_app in turn registers open/close connection calls with Flask's start/end request callbacks
roles_db.init_app(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
