from flask import current_app as app, Response, request
from . import db
from .models import User, APIKeys
import hashlib
import random
import uuid
@app.route('/login', methods=['POST'])
def login():
    return 'success'


@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    existinguser = User.query.filter_by(email=email).first()
    if existinguser:
        return {'message': 'User exists'}
    password = request.json.get('password')
    password_hash = hashlib.sha512(str(password).encode("utf-8") ).hexdigest()
    user = User(email=email, pass_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    key = str(user.id) + "." + str(uuid.uuid4())

    key_hash = hashlib.sha512(str(key).encode("utf-8") ).hexdigest()

    apikey = APIKeys(userid=user.id, api_key_hash=key_hash)
    db.session.add(apikey)
    db.session.commit()

    return {'api_key':key}


@app.route('/logout', methods=['POST'])
def logout():
    return 'success'
