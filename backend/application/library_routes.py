"""
Routes associated with sign language libraries.
"""

import os
import shutil
from zipfile import ZipFile
import cv2
from flask import (
    current_app as app, send_from_directory,
    jsonify, Blueprint, request
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .image_processing import preprocess_image, classify
from .models import User, UserRole, Sign, SignLanguageLibrary
import base64

library_routes = Blueprint('library_routes', __name__)


@library_routes.route("/")
def home():
    """
    Simple home route.
    """
    return "Hello World!"


@library_routes.route('/library/upload_sign_video', methods=['POST'])
@library_routes.route('/library/uploadsigns', methods=['POST'])
@library_routes.route('/library/uploadsign', methods=['POST'])
@jwt_required()
def upload_signs_jwt():
    """
    Receives requests to upload signs in the form of a zip file,
    an image, or a video. Gets the user's identity from their JWT
    and calls a function that processes the file.
    """
    caller_id = get_jwt_identity()
    return upload(caller_id)


def upload(caller_id):
    """
    Extracts variable names and sets up the
    environment for saving the file(s). Calls
    a function that actually processes and
    saves the file(s) to be uploaded.
    """
    lib_name = request.form['lib_name']
    libid = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    role = UserRole.query.filter_by(
        userid=caller_id, libraryid=libid, admin=True
    ).first()
    if role is None:
        return {"Error": "Permission Denied"}, 400
    sign_name = request.form['sign_name']
    img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    os.makedirs(img_path[:-1], exist_ok=True)
    zip_file = request.files.get('zip_file')
    image = request.files.get('image_file')
    video = request.files.get('video')
    if zip_file is not None:
        return upload_zip_file(sign_name, img_path, zip_file, libid)
    if image is not None:
        return upload_single_image(sign_name, img_path, image, libid)
    assert video is not None
    return upload_video(sign_name, img_path, video, libid)


def upload_zip_file(sign_name, img_path, zip_file, libid):
    """
    Extracts images from the zip file, preprocesses them
    and creates database entries for them.
    """
    zip_name = 'temp_zip.zip'
    zip_file.save(zip_name)
    with ZipFile(zip_name) as zpfl:
        filenames = zpfl.namelist()
        total_num_images = 0
        num_good_images = 0
        for filename in filenames[1:]:
            print(filename)
            total_num_images += 1
            # XXX: what happens if the file already exists? Is it overwritten?
            zpfl.extract(filename, path=img_path)
            if save_image(img_path, sign_name, filename, libid):
                num_good_images += 1
                print('Successfully uploaded image ' + str(total_num_images))
        db.session.commit()
        message = f'Successfully uploaded {num_good_images} of {total_num_images} images.'
        print(message)
        # XXX: test this
        return {'message': message}, 200
    return {'message': "Failed to upload zip file."}, 500


def save_image(img_path, sign_name, filename, libid):
    """
    Creates a database entry for the input image
    and saves the image on the filesystem.
    """
    img = preprocess_image(cv2.imread(img_path + filename))
    os.remove(img_path + filename)
    if img is not None:
        cv2.imwrite(img_path + filename, img)
        sign = Sign(
            meaning=sign_name,
            image_filename=filename,
            library_id=libid
        )
        db.session.add(sign)
    return img is not None


def upload_single_image(sign_name, img_path, image, libid):
    """
    Handles a single image file upload.
    """
    filename = sign_name + '.png'
    image.save(img_path + filename)
    if save_image(img_path, sign_name, filename, libid):
        db.session.commit()
        return {}, 200
    msg = 'A hand could not be found in the image.'
    print(msg)
    return {"Error": msg}, 400


def upload_video(sign_name, img_path, video, libid):
    """
    Reads frames from the video, preprocesses them,
    creates a database entry for them and saves the
    preprocessed images to the file system.
    """
    filename = 'temp_video.webm'
    video.save(filename)
    video_capture = cv2.VideoCapture('./' + filename)
    frame_grabbed, img = video_capture.read()
    count = 0
    while frame_grabbed:
        img = preprocess_image(img)
        if img is not None:
            img_name = sign_name + str(count) + '.png'
            cv2.imwrite(img_path + img_name, img)
            sign = Sign(meaning=sign_name, image_filename=img_name, library_id=libid)
            db.session.add(sign)
            count += 1
            print(count)
        frame_grabbed, img = video_capture.read()
    print('Successfully uploaded ' + str(count) + ' images.')
    db.session.commit()
    os.remove('temp_video.webm')
    return {}, 200


@library_routes.route('/library/createlibrary', methods=['POST'])
@jwt_required()
def create_library_jwt():
    """
    Gets the user's identity from their JWT and calls
    a function that creates a library for that user.
    """
    user_id = get_jwt_identity()
    return create_library(user_id)


def create_library(user_id):
    """
    Creates a new database entry for the library
    with the user with ID user_id as the admin.
    """
    libname = request.form.get('library_name')
    lib_description = request.form.get('description')
    existinglib = SignLanguageLibrary.query.filter_by(name=libname).first()
    if existinglib:
        return {'message': 'Library exists'}, 403
    library = SignLanguageLibrary(name=libname, description=lib_description)
    os.makedirs(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.add(library)
    db.session.commit()
    owner_role = UserRole(userid=user_id, libraryid=library.id, admin=True)
    db.session.add(owner_role)
    db.session.commit()
    return {}, 200


@library_routes.route('/library/signs', methods=['GET'])
@jwt_required()
def get_signs_jwt():
    """
    Gets the user's identity from their JWT and
    calls a function that gets the signs for them.
    """
    user_id = get_jwt_identity()
    return get_signs(user_id)


def get_signs(user_id):
    """
    Gets the signs from the library with name library_name
    for the user, if they have permission to use this
    library.
    """
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(name=library_name).first_or_404()
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=lib.id).first()
    if not user_role:
        return {"Error": "Permission Denied"}, 400
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@library_routes.route('/library/imageb64', methods=['GET'])
@jwt_required()
def get_sign_image_base64_jwt():
    user_id = get_jwt_identity()
    return get_sign_image_base64(user_id)


def get_sign_image_base64(caller_id):
    lib_name = request.args['library_name']
    if lib_name != '':
        lib = SignLanguageLibrary.query.filter_by(name=lib_name).first_or_404()
        caller_role = UserRole(userid=caller_id, libraryid=lib.id)
        if not caller_role:
            return {"Error": "Permission Denied"}, 400
    img_name = request.args['image_name']
    img_name = Sign.query.filter_by(meaning=img_name).first_or_404().image_filename
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    try:
        with open(path+img_name, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())
    except:
        return jsonify(), 404
    return my_string

@library_routes.route('/library/image', methods=['GET'])
@jwt_required()
def get_sign_image_jwt():
    """
    Gets the user's ID from their JWT and
    calls a function that returns the image
    they requested.
    """
    user_id = get_jwt_identity()
    return get_sign_image(user_id)


def get_sign_image(caller_id):
    """
    Returns the image associated with the sign if
    the user has permission to use the library
    to which the image belongs.
    """
    lib_name = request.args['library_name']
    if lib_name != '':
        lib = SignLanguageLibrary.query.filter_by(name=lib_name).first_or_404()
        caller_role = UserRole(userid=caller_id, libraryid=lib.id)
        if not caller_role:
            return {"Error": "Permission Denied"}, 400
    img_name = request.args['image_name']
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    print(path + img_name)
    return send_from_directory(path, img_name)


@library_routes.route('/libraries/names', methods=['GET'])
@jwt_required()
def get_library_names_jwt():
    """
    Gets the caller's ID from their JWT
    and calls a functions to get the
    names of the libraries they have
    permission to access.
    """
    caller_id = get_jwt_identity()
    return get_library_names(caller_id)


def get_library_names(caller_id):
    """
    Gets the names of the library that the
    caller has permission to access.
    """
    libs = SignLanguageLibrary.query.filter_by(ownerid=caller_id)
    return {'library_names': name for name in map(lambda lib: lib.name, libs)}


@library_routes.route('/libraries/getall', methods=['GET'])
@jwt_required()
def get_libraries_jwt():
    """
    Gets the caller's ID from their JWT and calls get_users_libraries()
    """
    caller_id = get_jwt_identity()
    return get_users_libraries(caller_id)


def get_users_libraries(caller_id):
    """
    Gets the libraries that the caller
    has permission to access.
    """
    libs = SignLanguageLibrary.query.all()
    all_libs = []
    for lib in libs:
        # skip all libs that the user doesn't have access to.
        caller_role = UserRole.query.filter_by(userid=caller_id, libraryid=lib.id).first()
        if not caller_role:
            continue
        thislib = {'name': lib.name, 'description': lib.description}
        all_libs.append(thislib)
    response = jsonify({'libraries': all_libs})
    return response, 200


@library_routes.route('/library/deletesign', methods=['DELETE'])
@jwt_required()
def delete_sign_jwt():
    """
    Gets the caller's ID from their JWT and calls
    delete_sign.
    """
    caller_id = get_jwt_identity()
    return delete_sign(caller_id)


def delete_sign(caller_id):
    """
    Deletes a sign from a library if the caller has permission to do so.
    """
    libname = request.args['library_name']
    signname = request.args['sign_name']
    lib = SignLanguageLibrary.query.filter_by(name=libname).first()
    caller_role = UserRole.query.filter_by(userid=caller_id, libraryid=lib.id, admin=True)
    if caller_role is None:
        return {"Error": "Permission Denied"}, 400
    Sign.query.filter_by(meaning=signname, library_id=lib.id).delete()
    db.session.commit()
    return {}, 200

@library_routes.route('/library/deletesigns', methods=['DELETE'])
#@jwt_required()
def delete_signs_jwt():
    libname = request.json.get('library_name')
    signs = request.json.get('signs')
    libid = SignLanguageLibrary.query.filter_by(name = libname).first_or_404().id

    for sign in signs:
        signtodel = Sign.query.filter_by(meaning=sign, library_id=libid).delete()

    return jsonify(), 200



@library_routes.route('/library/deletelibrary', methods=['DELETE'])
@jwt_required()
def delete_library_jwt():
    """
    Gets the caller's ID from their JWT and deletes a library
    if they have admin permissions for that library.
    """
    user_id = get_jwt_identity()
    return delete_library(user_id)


def delete_library(caller_id):
    """
    Deletes a library if the caller has admin
    permissions for this library.
    """
    print(request)
    libname = request.args.get('library_name')
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    caller_role = UserRole.query.filter_by(userid=caller_id, libraryid=libid, admin=True)
    if caller_role is None:
        return {"Error": "Permission Denied"}, 400
    UserRole.query.filter_by(libraryid=libid).delete()
    Sign.query.filter_by(library_id=libid).delete()
    SignLanguageLibrary.query.filter_by(name=libname).delete()
    shutil.rmtree(app.config['IMAGE_PATH'] + '/' + libname, ignore_errors=True)
    db.session.commit()
    return {}, 200


@library_routes.route('/library/adduser', methods=['POST'])
@jwt_required()
def adduser_jwt():
    """
    Gets the caller's ID and calls adduser.
    """
    caller_id = get_jwt_identity()
    return adduser(caller_id)


def adduser(caller_id):
    """
    Gives a user basic permissions for a library if
    the caller has admin permissions for this library.
    """
    libname = request.json.get('library_name')
    useremail = request.json.get('user_email')

    # check if sending user is admin first.
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    caller_role = UserRole.query.filter_by(userid=caller_id, libraryid=libid, admin=True).first()
    if caller_role is None:
        return {"Error": "Permission Denied"}, 400

    newuser = User.query.filter_by(email=useremail).first()
    if not newuser:
        return {"Error": "User cannot be found"}, 400

    newrole = UserRole(userid=newuser.id, libraryid=libid, admin=False)
    db.session.add(newrole)
    db.session.commit()
    return jsonify(), 200


@library_routes.route('/library/get/user/groups', methods=['GET'])
@jwt_required()
def get_user_groups_jwt():
    """
    Gets the caller's ID from their JWT and calls
    a function that gets the groups of users
    associated with the library.
    """
    caller_id = get_jwt_identity()
    return get_user_groups(caller_id)


def get_user_groups(caller_id):
    """
    Gets the groups of users associated with a library.
    """
    lib_name = request.args['library_name']
    # check if sending user is admin first.
    lib_id = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    callers_role = UserRole.query.filter_by(userid=caller_id, libraryid=lib_id, admin=True).first()
    if callers_role is None:
        return {"Error": "Permission Denied"}, 400
    admins = UserRole.query.filter_by(libraryid=lib_id, admin=True).all()
    normal_users = UserRole.query.filter_by(libraryid=lib_id, admin=False).all()
    admins = list(
        map(
            lambda user_role: User.query.filter_by(id=user_role.userid).first().email,
            admins
        )
    )
    normal_users = list(
        map(
            lambda user_role: User.query.filter_by(id=user_role.userid).first().email,
            normal_users
        )
    )
    all_users = User.query.all()
    roles = UserRole.query.filter_by(libraryid=lib_id).all()
    permissionless_users = []
    for user_a in all_users:
        has_permissions = False
        for role in roles:
            if user_a.id == role.userid:
                has_permissions = True
                break
        if not has_permissions:
            permissionless_users += [user_a.email]
    return {
        'permissionlessUsers': permissionless_users,
        'normalUsers': normal_users,
        'adminUsers': admins
    }, 200


@library_routes.route('/library/addadmin', methods=['POST'])
@jwt_required()
def addadmin_jwt():
    """
    Gets the ID of the user from their JWT and calls a
    function that gives another user admin permissions.
    """
    caller_id = get_jwt_identity()
    return addadmin(caller_id)


def addadmin(caller_id):
    """
    Gives the user admin permissions for this library.
    """
    libname = request.json.get('library_name')
    useremail = request.json.get('user_email')

    # check if sending user is admin first.
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    caller_role = UserRole.query.filter_by(userid=caller_id, libraryid=libid, admin=True).first()
    if caller_role is None:
        return {"Error": "Permission Denied"}, 400
    if not caller_role.admin:
        return {"Error": "Permission Denied"}, 400

    newuser = User.query.filter_by(email=useremail).first()
    if not newuser:
        return {"Error": "User cannot be found"}

    newrole = UserRole(userid=newuser.id, libraryid=libid, admin=True)
    db.session.add(newrole)
    db.session.commit()
    return jsonify(), 200


@library_routes.route('/library/revoke/permissions', methods=['DELETE'])
@jwt_required()
def revoke_permissions_jwt():
    """
    Removes the all permissions the user has for this library.
    """
    # XXX: will this work with the api key?
    lib_name = request.args['library_name']
    user_email = request.args['user_email']
    user_id = User.query.filter_by(email=user_email).first().id
    library_id = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    UserRole.query.filter_by(libraryid=library_id, userid=user_id).delete()
    db.session.commit()
    return {}, 200


@library_routes.route('/library/classifyimage', methods=['POST'])
def classify_request_jwt():
    """
    https://stackoverflow.com/questions/58931854/how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
    https://www.geeksforgeeks.org/python-opencv-imdecode-function/
    """
    return classify()
