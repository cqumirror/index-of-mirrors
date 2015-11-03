from flask import Flask
app = Flask(__name__)

# default configuration
APP_NAME = "Actor"
# SQLALCHEMY_ECHO = True
# SQLALCHEMY_RECORD_QUERIE = True

# load configuration
app.config.from_object(__name__)
app.config.from_envvar("ACTOR_SETTINGS")

from actor import views
