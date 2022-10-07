"""
Initializes the application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager

# Globally accessible libraries
db = SQLAlchemy()
socketio = SocketIO()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    JWTManager(app)
    app.config.from_object('config')
    # app.add_url_rule('/library/image', endpoint='get_sign_image', build_only=True)
    # Initialize CORS
    CORS(app)

    # Initialize Plugins
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    with app.app_context():
        try:
            db.create_all()
        except Exception as exception:
            print(exception)
            print('continuing...')
        return app
