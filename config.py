# ***********************************************************************
#  CODE CITATION: "Configuring Your Flask App"                          *
#  BY: Todd Birchard on September 30, 2018 / ACCESSED: June 12, 2023    *
#  URL: https://hackersandslackers.com/configure-flask-applications/    *
# ***********************************************************************

"""Flask APP configuration."""
from os import environ, path
from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

# General Config
ENVIRONMENT = environ.get("ENVIRONMENT")
FLASK_APP = environ.get("FLASK_APP")
FLASK_DEBUG = environ.get("FLASK_DEBUG")
SECRET_KEY = environ.get("SECRET_KEY")