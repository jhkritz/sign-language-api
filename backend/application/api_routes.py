"""
API routes using API keys instead of JWT
"""
from flask import Blueprint, request

from application.image_processing import classify
from application.login_routes import verifykey
from application.library_routes import (
    upload, create_library, get_signs,
    get_sign_image, get_library_names,
    get_users_libraries, delete_sign, delete_library
)

api_routes = Blueprint('api_routes', __name__)


@api_routes.route('/api/library/uploadsign', methods=['POST'])
@api_routes.route('/api/library/upload_sign_video', methods=['POST'])
@api_routes.route('/api/library/uploadsigns', methods=['POST'])
def api_upload():
    key = request.form.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    return upload(user_id)


@api_routes.route('/api/library/createlibrary', methods=['POST'])
def createlibraryapi():
    key = request.form.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    return create_library(key[0])


@api_routes.route('/api/library/signs', methods=['GET'])
def get_signsapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    return get_signs(key[0])


@api_routes.route('/api/library/image', methods=['GET'])
def get_sign_imageapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    return get_sign_image(key[0])


@api_routes.route('/api/libraries/names', methods=['GET'])
def get_library_namesapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    return get_library_names(user_id)


@api_routes.route('/api/libraries/getall', methods=['GET'])
def get_librariesapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    return get_users_libraries(user_id)


@api_routes.route('/api/library/deletesign', methods=['DELETE'])
def delete_signapi():
    key = request.json.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    return delete_sign(user_id)


@api_routes.route('/api/library/deletelibrary', methods=['DELETE'])
def delete_libraryapi():
    key = request.json.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    return delete_library(user_id)


@api_routes.route('/api/library/classifyimage', methods=['POST'])
def classify_requestapi():
    key = request.form['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    return classify()
