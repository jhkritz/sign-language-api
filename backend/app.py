"""
Starts the application.
"""

from application import init_app
from application.login_routes import auth_routes
from application.library_routes import library_routes
from application.api_routes import api_routes

app = init_app()
app.register_blueprint(auth_routes)
app.register_blueprint(api_routes)
app.register_blueprint(library_routes)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
