import os

"""Flask configuration."""

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'GDtfDCFYjD'

SQLALCHEMY_DATABASE_URI = 'postgresql://sign_language_api:flask123@localhost:5432/sign_language_api'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
IMAGE_PATH = ''

"""Heroku database configuration."""
try:
    HEROKU_DATABASE_URL = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://')
    if HEROKU_DATABASE_URL != '':
        SQLALCHEMY_DATABASE_URI = HEROKU_DATABASE_URL
except KeyError:
    pass
