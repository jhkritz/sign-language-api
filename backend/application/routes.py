from pydoc import describe
import json
import time
from flask import current_app as app, Response, request, send_from_directory, jsonify
from .models import SignLanguageLibrary, Sign
from zipfile import ZipFile
import numpy as np
from . import db
import os
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from flask_socketio import SocketIO, emit
from . import socketio
import io
from PIL import Image
import base64
import cv2
import shutil
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from matplotlib import pyplot as plt
from flask_jwt_extended import jwt_required, get_jwt_identity
from .login_routes import verifykey
from flask_cors import cross_origin
from sklearn.decomposition import PCA

hand_detector = HandDetector(maxHands=1)
desired_shape = (200, 200)


@app.route("/")
def home():
    return "Hello World!"


@app.route('/library/uploadsigns', methods=['POST'])
def upload_signs():
    try:
        lib_name = request.form['lib_name']
        sign_name = request.form['sign_name']
        zip_file = request.files['zip_file']
        zpfl = ZipFile(zip_file.stream._file)
        filenames = zpfl.namelist()
        total_num_images = 0
        num_good_images = 0
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '/'
        for filename in filenames[1:]:
            total_num_images += 1
            # XXX: what happens if the file already exists? Is it overwritten?
            zpfl.extract(filename, path=img_path)
            img = cv.imread(img_path + filename)
            img = preprocess_image(img)
            os.remove(img_path + filename)
            if img is None:
                continue
            else:
                num_good_images += 1
                cv.imwrite(img_path + filename, img)
                libid = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
                sign = Sign(
                    meaning=sign_name,
                    image_filename=filename,
                    library_id=libid
                )
                db.session.add(sign)
                db.session.commit()
            print('Sucessfully uploaded image ' + str(total_num_images))
        message = 'Successfully uploaded {} of {} images.'.format(num_good_images, total_num_images)
        print(message)
        return {'status': 200, 'message': message}
    except Exception as e:
        print(e)
        return Response(status=400)


@app.route('/library/uploadsign', methods=['POST'])
@jwt_required()
def uploadsign():
    # Endpoint to upload a single sign with a name
    try:
        lib_name = request.form.get('lib_name')
        sign_name = request.form.get('sign_name')
        image = request.files['image_file']
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '/'
        try:
            os.makedirs(img_path[:-1])
        except Exception as e:
            pass
        image.save(img_path + 'temp.jpg')
        image = cv2.imread(img_path + 'temp.jpg')
        image = preprocess_image(image)
        os.remove(img_path + 'temp.jpg')
        if image is None:
            msg = 'A hand could not be found in the image.'
            print(msg)
            return {"Error": msg}, 400
        Image.fromarray(image).save(img_path + sign_name + '.jpg')
        libid = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
        sign = Sign(meaning=sign_name, image_filename=sign_name + '.jpg',  library_id=libid)
        db.session.add(sign)
        db.session.commit()
    except Exception as e:
        print(e)
        return {"Error": str(e)}, 400
    return Response(status=200)


@app.route('/library/createlibrary', methods=['POST'])
@jwt_required()
def createlibrary():
    libname = request.form.get('library_name')
    lib_description = request.form.get('description')
    user_id = get_jwt_identity()
    existinglib = SignLanguageLibrary.query.filter_by(name=libname).first()
    if existinglib:
        return {'message': 'Library exists'}
    library = SignLanguageLibrary(name=libname, description=lib_description, ownerid=user_id)
    os.makedirs(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.add(library)
    db.session.commit()
    response = jsonify()
    return response, 200


@app.route('/library/signs', methods=['GET'])
@jwt_required()
def get_signs():
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(name=library_name).first_or_404()
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@app.route('/library/image', methods=['GET'])
@jwt_required()
def get_sign_image():
    lib_name = request.args['library_name']
    img_name = request.args['image_name']
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    return send_from_directory(path, img_name)


@app.route('/libraries/names', methods=['GET'])
@jwt_required()
def get_library_names():
    user_id = get_jwt_identity()
    libs = SignLanguageLibrary.query.filter_by(ownerid=user_id)
    return {'library_names': [name for name in map(lambda lib: lib.name, libs)]}


@app.route('/libraries/getall', methods=['GET'])
@jwt_required()
def get_libraries():
    user_id = get_jwt_identity()
    libs = SignLanguageLibrary.query.filter_by(ownerid=user_id)
    all_libs = []
    for lib in libs:
        thislib = {'name': lib.name, 'description': lib.description}
        all_libs.append(thislib)
    response = jsonify({'libraries': all_libs})
    return response, 200


@app.route('/library/deletesign', methods=['DELETE'])
@jwt_required()
def delete_sign():
    libname = request.json.get('library_name')
    signname = request.json.get('sign_name')
    try:
        lib = SignLanguageLibrary.query.filter_by(name=libname).first()
        Sign.query.filter_by(meaning=signname, library_id=lib.id).delete()
        db.session.commit()
        return Response(status=200)
    except:
        return Response(status=400)


@app.route('/library/deletelibrary', methods=['DELETE'])
@jwt_required()
def delete_library():
    libname = request.json.get('library_name')
    try:
        libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
        Sign.query.filter_by(library_id=libid).delete()
        SignLanguageLibrary.query.filter_by(name=libname).delete()
        shutil.rmtree(app.config['IMAGE_PATH'] + '/' + libname)
        db.session.commit()
        return Response(status=200)
    except:
        return Response(status=400)

# Functions used to classify images.
####################################################################################################


def get_data_and_labels(lib_name):
    lib_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    # Read library images and get labels
    lib = SignLanguageLibrary.query.filter_by(name=lib_name).first()
    labels = []
    data = []
    next_label = 0
    meaning_labels = {}
    label_meanings = []
    for sign in lib.signs:
        if sign.meaning not in meaning_labels.keys():
            meaning_labels[sign.meaning] = next_label
            label_meanings += [sign.meaning]
            next_label += 1
        fullpath = lib_path + sign.meaning + '/' + sign.image_filename
        img = cv.imread(lib_path + sign.meaning + '/' + sign.image_filename)
        data += [img.flatten()]
        labels += [meaning_labels[sign.meaning]]
    data = np.array(data, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    return data, labels, label_meanings


def preprocess_image(frame):
    # TODO: reference tutorial video
    offset = 30
    input_img = frame
    hands, hands_img = hand_detector.findHands(input_img)
    if hands:
        x, y, w, h = hands[0]['bbox']
        try:
            # All the images used need to be the same size
            cropped = hands_img[y-offset:y+offset+h, x-offset:x+w+offset]
            cropped = cv.resize(cropped, desired_shape)
            return cropped
        except Exception as e:
            print(e)
    # Return None so that classification is aborted if hands aren't found.
    return None


@app.route('/library/classifyimage', methods=['POST'])
def classify_request():
    """
    https://stackoverflow.com/questions/58931854/how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
    https://www.geeksforgeeks.org/python-opencv-imdecode-function/
    """
    classification_alg = 'KNN'
    data_image = request.files['image'].read()
    lib_name = request.form['library_name']
    b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
    try:
        image = cv2.imdecode(b_array, cv2.IMREAD_COLOR)
        processed_image = preprocess_image(image)
        if processed_image is not None:
            flat_image = processed_image.flatten()
            processed_image = cv2.imencode('.png', processed_image)[1]
            image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
            result = None
            if classification_alg == 'LDA':
                start = time.time()
                result = lda_classify(lib_name, flat_image)
                end = time.time()
                print('Time taken = ' + str(end - start))
            elif classification_alg == 'KNN':
                start = time.time()
                result = knn_classify(lib_name, flat_image)
                end = time.time()
                print('Time taken = ' + str(end - start))
            return {'processedImage': image_out, 'result': result}
        else:
            print('processed_image is none')
            return Response(status=400)
    except Exception as e:
        print(e)
        return Response(status=400)


def lda_classify(lib_name, processed_image):
    lda = LinearDiscriminantAnalysis()
    data, labels, label_meanings = get_data_and_labels(lib_name)
    lda.fit(data, labels)
    flat_image = processed_image.flatten()
    quality_of_match = max(lda.predict_proba(flat_image[np.newaxis, :])[0])
    prediction = lda.predict(flat_image[np.newaxis, :])[0]
    meaning = label_meanings[int(prediction)]
    return {'classification': meaning, 'quality_of_match': str(quality_of_match)}


def pca_transform(data, flat_image):
    pca = PCA(n_components=min(min(10, data.shape[0]), data.shape[1]))
    pca.fit(data)
    print('pca evr = ' + str(pca.explained_variance_ratio_))
    data = pca.transform(data)
    flat_image = pca.transform(flat_image[np.newaxis, :])[0]
    return data, flat_image


def knn_classify(lib_name, flat_image):
    data, labels, label_meanings = get_data_and_labels(lib_name)
    k = min(int(data.shape[0] / len(label_meanings)), 100)
    knn = cv.ml.KNearest_create()
    should_use_pca = True
    if should_use_pca:
        data, flat_image = pca_transform(data, flat_image)
    knn.train(data, cv.ml.ROW_SAMPLE, labels)
    to_classify = np.array(flat_image[np.newaxis, :], dtype=np.float32)
    retval, results, responses, dists = knn.findNearest(to_classify, k=k)
    classification = results[0][0]
    meaning = label_meanings[int(classification)]
    quality_of_match = 0
    for resp in responses[0]:
        if resp == classification:
            quality_of_match += 1
    quality_of_match = 100 * quality_of_match / len(responses[0])
    return {'classification': meaning, 'quality_of_match': str(quality_of_match)}


#########################################################################
# API routes using API keys instead of JWT
#########################################################################


@ app.route('/api/library/uploadsign', methods=['POST'])
def uploadsignapi():
    key = request.form.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401

    # Endpoint to upload a single sign with a name
    try:
        lib_name = request.form.get('lib_name')
        sign_name = request.form.get('sign_name')
        image = request.files['image_file']
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '_temp.jpg'
        image.save(img_path)
        image = cv2.imread(img_path)
        hand_detector = HandDetector(maxHands=1)
        desired_shape = (200, 200)
        image = preprocess_image(image)
        os.remove(img_path)
        if image is None:
            return {"Error": "A hand could not be found in the image"}, 400
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '.jpg'
        Image.fromarray(image).save(img_path)
        libid = SignLanguageLibrary.query.filter_by(name=lib_name).first().id
        sign = Sign(meaning=sign_name, image_filename=sign_name + '.jpg',  library_id=libid)
        db.session.add(sign)
        db.session.commit()
        print('success')
    except Exception as e:
        print(e)
        return {"Error": str(e)}, 400
    return Response(status=200)


@ app.route('/api/library/createlibrary', methods=['POST'])
def createlibraryapi():
    key = request.form.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    libname = request.form.get('library_name')
    lib_description = request.form.get('description')
    user_id = key[0]
    existinglib = SignLanguageLibrary.query.filter_by(name=libname).first()
    if existinglib:
        return {'message': 'Library exists'}
    library = SignLanguageLibrary(name=libname, description=lib_description, ownerid=user_id)
    os.makedirs(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.add(library)
    db.session.commit()
    response = jsonify()
    return response, 200


@ app.route('/api/library/signs', methods=['GET'])
def get_signsapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(name=library_name).first_or_404()
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@ app.route('/api/library/image', methods=['GET'])
def get_sign_imageapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    lib_name = request.args['library_name']
    img_name = request.args['image_name']
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    return send_from_directory(path, img_name)


@ app.route('/api/libraries/names', methods=['GET'])
def get_library_namesapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401

    user_id = key[0]
    libs = SignLanguageLibrary.query.filter_by(ownerid=user_id)
    return {'library_names': [name for name in map(lambda lib: lib.name, libs)]}


@ app.route('/api/libraries/getall', methods=['GET'])
def get_librariesapi():
    key = request.args['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    user_id = key[0]
    libs = SignLanguageLibrary.query.filter_by(ownerid=user_id)
    all_libs = []
    for lib in libs:
        thislib = {'name': lib.name, 'description': lib.description}
        all_libs.append(thislib)
    response = jsonify({'libraries': all_libs})
    return response, 200


@ app.route('/api/library/deletesign', methods=['DELETE'])
def delete_signapi():
    key = request.json.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    libname = request.json.get('library_name')
    signname = request.json.get('sign_name')
    try:
        lib = SignLanguageLibrary.query.filter_by(name=libname).first()
        Sign.query.filter_by(meaning=signname, library_id=lib.id).delete()
        db.session.commit()
        return Response(status=200)
    except:
        return Response(status=400)


@ app.route('/api/library/deletelibrary', methods=['DELETE'])
def delete_libraryapi():
    key = request.json.get('key')
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    libname = request.json.get('library_name')
    try:
        libid = SignLanguageLibrary.query.filter_by(name=libname).first().id
        Sign.query.filter_by(library_id=libid).delete()
        SignLanguageLibrary.query.filter_by(name=libname).delete()
        shutil.rmtree(app.config['IMAGE_PATH'] + '/' + libname)
        db.session.commit()
        return Response(status=200)
    except:
        return Response(status=400)


@app.route('/api/library/classifyimage', methods=['POST'])
def classify_requestapi():
    """
    https://stackoverflow.com/questions/58931854/how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
    https://www.geeksforgeeks.org/python-opencv-imdecode-function/
    """
    key = request.form['key']
    if verifykey(key) == "0":
        return {'message': 'Authentication failed'}, 401
    classification_alg = 'KNN'
    data_image = request.files['image'].read()
    lib_name = request.form['library_name']
    b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
    try:
        image = cv2.imdecode(b_array, cv2.IMREAD_COLOR)
        processed_image = preprocess_image(image)
        if processed_image is not None:
            flat_image = processed_image.flatten()
            processed_image = cv2.imencode('.png', processed_image)[1]
            image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
            result = None
            if classification_alg == 'LDA':
                start = time.time()
                result = lda_classify(lib_name, flat_image)
                end = time.time()
                print('Time taken = ' + str(end - start))
            elif classification_alg == 'KNN':
                start = time.time()
                result = knn_classify(lib_name, flat_image)
                end = time.time()
                print('Time taken = ' + str(end - start))
            return {'processedImage': image_out, 'result': result}
        else:
            print('processed_image is none')
            return Response(status=400)
    except Exception as e:
        print(e)
        return Response(status=400)
