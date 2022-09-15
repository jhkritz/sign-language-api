from flask import current_app as app, Response, request, jsonify
from . import db
from .models import User, APIKeys
import hashlib
import random
import uuid
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                set_access_cookies,
                                set_refresh_cookies,
                                jwt_required,
                                unset_jwt_cookies,
                                get_jwt_identity
                                )


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    existinguser = User.query.filter_by(email=email).first()
    if not existinguser:
        return {'message': 'Unkown user'}, 400
    password = request.json.get('password')
    password_hash = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    if not existinguser.pass_hash == password_hash:
        return {'message': 'Incorrect password'}, 400

    access_token = create_access_token(identity=existinguser.id)
    refresh_token = create_refresh_token(identity=existinguser.id)
    # return auth and token in json
    return {'access': access_token, 'refresh': refresh_token}, 200


@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    existinguser = User.query.filter_by(email=email).first()
    if existinguser:
        return {'message': 'User exists'}, 400
    password = request.json.get('password')
    password_hash = hashlib.sha512(str(password).encode("utf-8")).hexdigest()
    user = User(email=email, pass_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    key = generateapikey(user.id)

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    #set_access_cookies(response, access_token)
    #set_refresh_cookies(response, refresh_token)

    return {'api_key': key, 'access': access_token, 'refresh': refresh_token}


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Success'})
    unset_jwt_cookies(response)
    return response


@app.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refreshtoken():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    response = jsonify()
    return {'access': access_token, 'refresh': refresh_token}


@app.route('/api/resetapikey', methods=['GET'])
@jwt_required()
def resetapikey():
    userid = request.args['id']
    return generateapikey(userid)


# create api key and store hash in DB
# return unhashed key
def generateapikey(id):

    # check for existing key and remove it
    if not (User.query.filter_by(id=id).first()):
        return "0"
    existingkey = APIKeys.query.filter_by(userid=id).delete()

    key = str(id) + "." + str(uuid.uuid4())
    key_hash = hashlib.sha512(str(key).encode("utf-8")).hexdigest()
    apikey = APIKeys(userid=id, api_key_hash=key_hash)
    db.session.add(apikey)
    db.session.commit()

    return key

# verify key and return user id. return 0 if failed to verify


def verifykey(api_key):
    hash = hashlib.sha512(str(api_key).encode("utf-8")).hexdigest()
    keys = APIKeys.query.all()

    userid = 0
    for key in keys:
        if key.api_key_hash == hash:
            userid = key.userid
    return str(userid)


@app.route('/api/testkey', methods=['POST'])
def testkey():
    key = request.json.get('key')
    return verifykey(key)