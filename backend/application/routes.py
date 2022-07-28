from flask import current_app as app
from .models import user

@app.route("/")
def home():
    return "Hello World!"