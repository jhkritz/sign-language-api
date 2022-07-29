from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')
    app.add_url_rule('/library/image', endpoint='get_sign_image', build_only=True)
    # Initialize Plugins
    db.init_app(app)
    with app.app_context():
        # Include our Routes
        from application import routes
        db.create_all()
        return app
