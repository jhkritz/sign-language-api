from flask import current_app as app, Response, request, jsonify
from . import db
from .models import User, APIKeys
import hashlib
import random
import uuid
from flask_jwt_extended import (create_access_token, 
create_refresh_token, 
set_access_cookies,
set_refresh_cookies )

@app.route('/login', methods=['POST'])
def login():

    #return auth and token
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

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    response = jsonify({'api_key':key})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@app.route('/logout', methods=['POST'])
def logout():
    return 'success'
