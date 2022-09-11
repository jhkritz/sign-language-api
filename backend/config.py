import os

"""Flask configuration."""

TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SECRET_KEY = 'GDtfDCFdwafwafwafYjD'
JWT_SECRET_KEY='GDtfDCFdwafwafwafYjD'
JWT_TOKEN_LOCATION=['cookies']

SQLALCHEMY_DATABASE_URI = 'postgresql://sign_language_api:flask123@localhost:5432/sign_language_api'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
IMAGE_PATH = './library_images'

"""Heroku database configuration."""
try:
    HEROKU_DATABASE_URL = os.environ['DB_URL'].replace('postgres://', 'postgresql://')
    print(HEROKU_DATABASE_URL)
    if HEROKU_DATABASE_URL != '':
        SQLALCHEMY_DATABASE_URI = HEROKU_DATABASE_URL
except KeyError:
    pass
