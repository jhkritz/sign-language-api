import os
import shutil
from zipfile import ZipFile

from flask import send_from_directory, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from . import db
from .image_processing import *
from .models import User, UserRole, Sign

library_routes = Blueprint('library_routes', __name__)


@library_routes.route("/")
def home():
    return "Hello World!"


@library_routes.route('/library/upload_sign_video', methods=['POST'])
@library_routes.route('/library/uploadsigns', methods=['POST'])
@library_routes.route('/library/uploadsign', methods=['POST'])
@jwt_required()
def upload_signs():
    user_id = get_jwt_identity()
    return upload(user_id)


def upload(user_id):
    lib_name = request.form['lib_name']
    libid = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    role = UserRole.query.filter_by(userid=user_id, libraryid=libid, admin=True).first()
    if role is None:
        return {"Error": "Permission Denied"}, 400
    sign_name = request.form['sign_name']
    img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '/'
    os.makedirs(img_path[:-1], exist_ok=True)
    zip_file = request.files.get('zip_file')
    image = request.files.get('image_file')
    video = request.files.get('video')
    if zip_file is not None:
        return upload_zip_file(sign_name, img_path, zip_file, libid)
    if image is not None:
        return upload_single_image(sign_name, img_path, image, libid)
    if video is not None:
        return upload_video(sign_name, img_path, video, libid)


def upload_zip_file(sign_name, img_path, zip_file, libid):
    zip_name = 'temp_zip.zip'
    zip_file.save(zip_name)
    zpfl = ZipFile(zip_name)
    filenames = zpfl.namelist()
    total_num_images = 0
    num_good_images = 0
    for filename in filenames[1:]:
        total_num_images += 1
        # XXX: what happens if the file already exists? Is it overwritten?
        zpfl.extract(filename, path=img_path)
        if save_image(img_path, sign_name, filename, libid):
            num_good_images += 1
            print('Successfully uploaded image ' + str(total_num_images))
    db.session.commit()
    message = 'Successfully uploaded {} of {} images.'.format(num_good_images, total_num_images)
    print(message)
    return {'status': 200, 'message': message}


def save_image(img_path, sign_name, filename, libid):
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
    filename = sign_name + '.png'
    image.save(img_path + filename)
    if save_image(img_path, sign_name, filename, libid):
        db.session.commit()
        return {}, 200
    else:
        msg = 'A hand could not be found in the image.'
        print(msg)
        return {"Error": msg}, 400


def upload_video(sign_name, img_path, video, libid):
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
    return Response(status=200)


@library_routes.route('/library/createlibrary', methods=['POST'])
@jwt_required()
def create_library():
    user_id = get_jwt_identity()
    return create_library(user_id)


def create_library(user_id):
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
    response = jsonify()
    return response, 200


@library_routes.route('/library/signs', methods=['GET'])
@jwt_required()
def get_signs():
    user_id = get_jwt_identity()
    return get_signs(user_id)


def get_signs(user_id):
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(name=library_name).first_or_404()
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=lib.id).first()
    if not user_role:
        return {"Error": "Permission Denied"}, 400
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@library_routes.route('/library/image', methods=['GET'])
@jwt_required()
def get_sign_image():
    user_id = get_jwt_identity()
    return get_sign_image(user_id)


def get_sign_image(user_id):
    lib_name = request.args['library_name']
    if lib_name != '':
        lib = SignLanguageLibrary.query.filter_by(name=lib_name).first_or_404()
        user_role = UserRole(userid=user_id, libraryid=lib.id)
        if not user_role:
            return {"Error": "Permission Denied"}, 400
    img_name = request.args['image_name']
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    return send_from_directory(path, img_name)


@library_routes.route('/libraries/names', methods=['GET'])
@jwt_required()
def get_library_names():
    user_id = get_jwt_identity()
    return get_library_names(user_id)


def get_library_names(user_id):
    libs = SignLanguageLibrary.query.filter_by(ownerid=user_id)
    return {'library_names': [name for name in map(lambda lib: lib.name, libs)]}


@library_routes.route('/libraries/getall', methods=['GET'])
@jwt_required()
def get_libraries():
    user_id = get_jwt_identity()
    return get_users_libraries(user_id)


def get_users_libraries(user_id):
    libs = SignLanguageLibrary.query.all()
    all_libs = []
    for lib in libs:
        # skip all libs that the user doesn't have access to.
        user_role = UserRole.query.filter_by(userid=user_id, libraryid=lib.id).first()
        if not user_role:
            continue
        thislib = {'name': lib.name, 'description': lib.description}
        all_libs.append(thislib)
    response = jsonify({'libraries': all_libs})
    return response, 200


@library_routes.route('/library/deletesign', methods=['DELETE'])
@jwt_required()
def delete_sign():
    user_id = get_jwt_identity()
    return delete_sign(user_id)


def delete_sign(user_id):
    libname = request.args['library_name']
    signname = request.args['sign_name']
    lib = SignLanguageLibrary.query.filter_by(name=libname).first()
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=lib.id, admin=True)
    if user_role is None:
        return {"Error": "Permission Denied"}, 400
    Sign.query.filter_by(meaning=signname, library_id=lib.id).delete()
    db.session.commit()
    return Response(status=200)


@library_routes.route('/library/deletelibrary', methods=['DELETE'])
@jwt_required()
def delete_library():
    user_id = get_jwt_identity()
    return delete_library(user_id)


def delete_library(user_id):
    print(request)
    libname = request.args.get('library_name')
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=libid, admin=True)
    if user_role is None:
        return {"Error": "Permission Denied"}, 400
    UserRole.query.filter_by(libraryid=libid).delete()
    Sign.query.filter_by(library_id=libid).delete()
    SignLanguageLibrary.query.filter_by(name=libname).delete()
    shutil.rmtree(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.commit()
    return Response(status=200)


@library_routes.route('/library/adduser', methods=['POST'])
@jwt_required()
def adduser():
    user_id = get_jwt_identity()
    return adduser(user_id)


def adduser(user_id):
    libname = request.json.get('library_name')
    useremail = request.json.get('user_email')

    # check if sending user is admin first.
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=libid, admin=True).first()
    if user_role is None:
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
def get_user_groups():
    user_id = get_jwt_identity()
    return get_user_groups(user_id)


def get_user_groups(user_id):
    lib_name = request.args['library_name']
    # check if sending user is admin first.
    lib_id = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    callers_role = UserRole.query.filter_by(userid=user_id, libraryid=lib_id, admin=True).first()
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
def addadmin():
    user_id = get_jwt_identity()
    return addadmin(user_id)


def addadmin(user_id):
    libname = request.json.get('library_name')
    useremail = request.json.get('user_email')

    # check if sending user is admin first.
    libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
    user_role = UserRole.query.filter_by(userid=user_id, libraryid=libid, admin=True).first()
    if user_role is None:
        return {"Error": "Permission Denied"}, 400
    if not user_role.admin:
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
def revoke_permissions():
    # XXX: will this work with the api key?
    lib_name = request.args['library_name']
    user_email = request.args['user_email']
    user_id = User.query.filter_by(email=user_email).first().id
    library_id = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
    UserRole.query.filter_by(libraryid=library_id, userid=user_id).delete()
    db.session.commit()
    return {}, 200


@library_routes.route('/library/classifyimage', methods=['POST'])
def classify_request():
    """
    https://stackoverflow.com/questions/58931854/how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
    https://www.geeksforgeeks.org/python-opencv-imdecode-function/
    """
    return classify()
