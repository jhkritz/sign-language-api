from pydoc import describe
import time
from flask import current_app as app, Response, request, send_from_directory
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
# from aiohttp import web
# from av import VideoFrame

# from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
# from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

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
            img = process_input_single_frame(
                img, hand_detector=hand_detector, desired_shape=desired_shape
            )
            os.remove(img_path + filename)
            if img is None:
                continue
            else:
                num_good_images += 1
                cv.imwrite(img_path + filename, img)
                #Image.fromarray(img).save(img_path + filename)
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
        image = process_input_single_frame(
            image, hand_detector=hand_detector, desired_shape=desired_shape
        )
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
def createlibrary():
    libname = request.form.get('library_name')
    lib_description = request.form.get('description')
    existinglib = SignLanguageLibrary.query.filter_by(name=libname).first()
    if existinglib:
        return {'message': 'Library exists'}
    library = SignLanguageLibrary(name=libname, description=lib_description)
    os.makedirs(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.add(library)
    db.session.commit()
    return Response(status=200)


@app.route('/library/signs', methods=['GET'])
def get_signs():
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(name=library_name).first_or_404()
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@app.route('/library/image', methods=['GET'])
def get_sign_image():
    lib_name = request.args['library_name']
    img_name = request.args['image_name']
    path = os.getcwd() + '/' + app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    return send_from_directory(path, img_name)


@app.route('/libraries/names', methods=['GET'])
def get_library_names():
    libs = SignLanguageLibrary.query.all()
    return {'library_names': [name for name in map(lambda lib: lib.name, libs)]}


@app.route('/libraries/getall', methods=['GET'])
def get_libraries():
    libs = SignLanguageLibrary.query.all()
    all_libs = []
    for lib in libs:
        thislib = {'name': lib.name, 'description': lib.description}
        all_libs.append(thislib)
    return {'libraries': all_libs}


@app.route('/library/deletesign', methods=['DELETE'])
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


def classify(to_classify, knn, k, label_meanings):
    retval, results, responses, dists = knn.findNearest(to_classify, k=k)
    classification = results[0][0]
    meaning = label_meanings[int(classification)]
    #meaning = Sign.get_sign_meaning(int(classification))
    quality_of_match = 0
    for resp in responses[0]:
        if resp == classification:
            quality_of_match += 1
    # print(responses[0])
    #print('len(responses) = ' + str(len(responses[0])))
    quality_of_match = 100 * quality_of_match / len(responses[0])
    return {'classification': meaning, 'quality_of_match': str(quality_of_match)}


def get_data_and_labels(lib_name, lib_path):
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


def process_input_single_frame(frame, hand_detector, desired_shape):
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


@socketio.on('image_request')
def return_image(data_image, lib_name):
    # socket function to process image and then return result
    try:

        # Note: This code is based on the code given on the webpage linked below:
        # https://www.geeksforgeeks.org/python-opencv-imdecode-function/
        # Open image with opencv
        b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
        image = cv2.imdecode(b_array, cv2.IMREAD_COLOR)
        # Setup the model
        lib_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
        data, labels, label_meanings = get_data_and_labels(lib_name, lib_path)
        # XXX: this code will crash if the library contains < 3 images
        k = min(data.shape[0], 10)
        knn = cv.ml.KNearest_create()
        knn.train(data, cv.ml.ROW_SAMPLE, labels)
        # Process the image
        processed_image = process_input_single_frame(image, hand_detector, desired_shape)
        # Prepare for classification
        flattened = processed_image.flatten()
        # knn.findNearest() expects an array of images for classification.
        to_classify = np.array(flattened[np.newaxis, :], dtype=np.float32)
        # Classify the processed image
        result = None
        if type(processed_image):
            result = classify(to_classify, knn, k, label_meanings)
        # This conversion is based on the code provided in the following StackOverflow post
        # https://stackoverflow.com/questions/58931854/
        # how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
        processed_image = cv2.imencode('.png', processed_image)[1]
        image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
        response = {'frame': image_out, 'result': result}
        # print(response['result'])
        emit('image_response', response)
    except Exception as e:
        print(e)


@app.route('/library/classifyimage', methods=['POST'])
def classify_request():
    # Majority of code copied from function above
    data_image = request.files['image'].read()
    lib_name = request.form['library_name']
    b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
    try:
        start = time.time()
        lda = LinearDiscriminantAnalysis()
        # Note: This code is based on the code given on the webpage linked below:
        # https://www.geeksforgeeks.org/python-opencv-imdecode-function/
        # Open image with opencv
        #b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
        image = cv2.imdecode(b_array, cv2.IMREAD_COLOR)
        # Setup the model
        lib_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
        data, labels, label_meanings = get_data_and_labels(lib_name, lib_path)
        # 3
        print(data.shape)
        lda.fit(data, labels)
        print('explained var = ' + str(lda.explained_variance_ratio_))
        print(lda.predict_proba(data))
        print(data.shape)
        proj = lda.transform(data)
        y_pred = lda.predict(data)
        plt.plot(proj[:, 0], proj[:, 1])
        plt.show()
        print(y_pred)
        count = 0
        for i in range(len(y_pred)):
            if y_pred[i] == labels[i]:
                count += 1
        print('num correct = ' + str(count))
        # 3
        processed_image = process_input_single_frame(image, hand_detector, desired_shape)
        result = None
        if processed_image is not None:
            processed_image = processed_image.flatten()
            trans = lda.transform(processed_image[np.newaxis, :])
            print(trans.shape)
            pred = lda.predict(processed_image[np.newaxis, :])
            quality_of_match = lda.predict_proba(processed_image[np.newaxis, :])[0]
            print(quality_of_match)
            quality_of_match = max(quality_of_match)
            # quality_of_match = lda.score(processed_image[np.newaxis, :], labels)
            # This conversion is based on the code provided in the following StackOverflow post
            # https://stackoverflow.com/questions/58931854/
            # how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
            processed_image = cv2.imencode('.png', processed_image)[1]
            image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
            meaning = label_meanings[int(pred[0])]
            result = {'classification': meaning, 'quality_of_match': str(quality_of_match)}
            print(result)
            response = {'processedImage': image_out, 'result': result}
            # print(response['result'])
            end = time.time()
            print('Time taken = ' + str(end - start))
            return response
        else:
            print('processed_image is none')
            return Response(status=400)
        """
        #projected_data = lda.transform(data)
        # XXX: this code will crash if the library contains < 3 images
        #k = min(data.shape[0], 1)
        k = min(data.shape[0], 10)
        #print('k = ' + str(k))
        knn = cv.ml.KNearest_create()
        #knn.train(projected_data, cv.ml.ROW_SAMPLE, labels)
        # Process the image
        processed_image = process_input_single_frame(image, hand_detector, desired_shape).flatten()
        result = None
        if processed_image is not None:
            # Prepare for classification
            flattened = processed_image.flatten()
            # knn.findNearest() expects an array of images for classification.
            to_classify = np.array(flattened[np.newaxis, :], dtype=np.float32)
            # Classify the processed image
            result = classify(to_classify, knn, k, label_meanings)
            # This conversion is based on the code provided in the following StackOverflow post
            # https://stackoverflow.com/questions/58931854/
            # how-to-stream-live-video-frames-from-client-to-flask-server-and-back-to-the-clie
            processed_image = cv2.imencode('.png', processed_image)[1]
            image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
            response = {'processedImage': image_out, 'result': result}
            # print(response['result'])
            print('Time taken = ' + str(end - start))
            return response
        """
    except Exception as e:
        print('exception')
        print(e)
        return Response(status=400)
