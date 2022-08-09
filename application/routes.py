from flask import current_app as app, Response, request, send_from_directory
from .models import user, SignLanguageLibrary, Sign
from zipfile import ZipFile
import numpy as np
from . import db
import os
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector


@app.route("/")
def home():
    return "Hello World!"


def preprocess_and_save_image(zpfl, lib_name, img_path, image_file_name):
    desired_shape = (200, 200)
    zpfl.extract(lib_name + '/' + image_file_name, path=img_path)
    img = cv.imread(img_path + '/' + lib_name + '/' + image_file_name)
    img = cv.resize(img, desired_shape)
    hand_detector = HandDetector(maxHands=1)
    offset = 30
    hands, hands_img = hand_detector.findHands(img)
    if hands:
        x, y, w, h = hands[0]['bbox']
        try:
            cropped = hands_img[y-offset:y+offset+h, x-offset:x+offset+w]
            cropped = cv.resize(cropped, desired_shape)
            cv.imwrite(img_path + '/' + image_file_name, cropped)
        except Exception as e:
            print(e)
    else:
        cv.imwrite(img_path + '/' + image_file_name, img)


@app.route('/library/upload', methods=['POST'])
def upload_library():
    try:
        # Request arguments and files
        sign_meanings = request.files['sign_meanings']
        zipped_images = request.files['zipped_images']
        lib_name = request.form.to_dict()['library_name']
        # The path that this library's images will be saved to
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name
        lib = SignLanguageLibrary(name=lib_name)
        db.session.add(lib)
        db.session.commit()
        # XXX: will not work as intended if the \r or \r\n are used instead of \n
        lines = sign_meanings.read().decode().split('\n')
        # TODO: Refer to source for the file extraction
        zpfl = ZipFile(zipped_images.stream._file)
        for line in lines:
            fields = line.split(',')
            if len(fields) < 2:
                continue
            image_file_name = fields[0]
            sign_meaning = fields[1]
            try:
                preprocess_and_save_image(zpfl, lib_name, img_path, image_file_name)
            except Exception as e:
                print(e)
            sign = Sign(meaning=sign_meaning, image_filename=image_file_name, library_id=lib.id)
            db.session.add(sign)
        db.session.commit()
    except KeyError:
        return Response(status=400)
    return Response(status=200)

#Endpoint to upload a single sign with a name
@app.route('/library/uploadsign', methods=['POST'])
def uploadsign():
    try:
        libid = request.form.get('lib_id')
        sign_name = request.form.get('sign_name')
        image = request.files['image_file']
        lib_name = SignLanguageLibrary.query.filter_by(id=libid).first().name

        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '.jpg'
        image.save(img_path)

        sign = Sign(meaning=sign_name, image_filename = img_path,  library_id=libid)
        db.session.add(sign)
        db.session.commit()
    except KeyError:
        return Response(status=400)
    return Response(status=200)

@app.route('/library/createlibrary', methods=['POST'])
def createlibrary():
    libname = request.form.get('library_name')
    existinglib = SignLanguageLibrary.query.filter_by(name=libname)
    if existinglib:
        return Response({'Library exists'})
    library = SignLanguageLibrary(name = libname)
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


@app.route('/test/local/stream/classification', methods=['GET'])
def test_classify_image_with_local_video_stream():
    """
    This code assumes that the library images have been resized to desired_shape
    """
    lib_name = 'test_local_stream'
    lib_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    capture = cv.VideoCapture(0)
    hand_detector = HandDetector(maxHands=1)
    desired_shape = (200, 200)
    data, labels = get_data_and_labels(lib_name, lib_path)
    # Setup the classifier
    knn = cv.ml.KNearest_create()
    knn.train(data, cv.ml.ROW_SAMPLE, labels)
    # Classify images from stream
    while True:
        input_img_array = process_input(capture, hand_detector, desired_shape)
        try:
            print(classify(input_img_array, knn))
            cv.waitKey(1)
        except Exception as e:
            print(e)
    return Response(status=200)

# Functions used to classify images.
####################################################################################################


def classify(to_classify, knn):
    retval, results, responses, dists = knn.findNearest(to_classify, k=1)
    classification = results[0][0]
    meaning = Sign.get_sign_meaning(int(classification))
    quality_of_match = 0
    for resp in responses[0]:
        if resp == classification:
            quality_of_match += 1
    quality_of_match = 100 * quality_of_match / len(responses[0])
    return {'classification': meaning, 'quality_of_match': str(quality_of_match)}


def get_data_and_labels(lib_name, lib_path):
    # Read library images and get labels
    lib = SignLanguageLibrary.query.filter_by(name=lib_name).first()
    labels = []
    data = []
    for sign in lib.signs:
        img = cv.imread(lib_path + sign.image_filename)
        data += [img.flatten()]
        labels += [sign.id]
    data = np.array(data, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    return data, labels


def process_input(capture, hand_detector, desired_shape):
    # TODO: reference tutorial video
    offset = 30
    s, input_img = capture.read()
    input_img = cv.resize(input_img, desired_shape)
    hands, hands_img = hand_detector.findHands(input_img)
    if hands:
        x, y, w, h = hands[0]['bbox']
        try:
            # All the images used need to be the same size
            cropped = hands_img[y-offset:y+offset+h, x-offset:x+w+offset]
            cropped = cv.resize(cropped, desired_shape)
            cv.imshow('Processed input', cropped)
            # Prepare for classification
            flattened = cropped.flatten()
            # knn.findNearest() expects an array of images for classification.
            return np.array(flattened[np.newaxis, :], dtype=np.float32)
        except Exception as e:
            print(e)
    return None


####################################################################################################
# XXX: The code below is outdated.
####################################################################################################
def preprocess_image(image, desired_shape):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if image.shape != desired_shape:
        image = cv.resize(image, desired_shape)
    return image.flatten()


@app.route('/library/classify/image', methods=['PUT'])
def classify_image():
    lib_name = request.form.to_dict()['library_name']
    lib_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/'
    img = request.files['image']
    img_path = lib_path + 'to_classify/'
    img_name = img_path + img.filename
    os.makedirs(img_path, exist_ok=True)
    img.save(img_name)
    # All the images used need to be the same size
    to_classify = cv.cvtColor(cv.imread(img_name), cv.COLOR_BGR2GRAY)
    desired_shape = to_classify.shape
    to_classify = np.array([to_classify.flatten()], dtype=np.float32)
    lib = SignLanguageLibrary.query.filter_by(name=lib_name).first_or_404()
    # Construct the data and label arrays
    labels = []
    data = []
    for sign in lib.signs:
        img = cv.imread(lib_path + sign.image_filename)
        data += [preprocess_image(img, desired_shape)]
        labels += [sign.id]
    data = np.array(data, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    # Setup the classifier
    knn = cv.ml.KNearest_create()
    knn.train(data, cv.ml.ROW_SAMPLE, labels)
    # knn.findNearest() expects an array of images for classification.
    retval, results, responses, dists = knn.findNearest(to_classify, k=12)
    classification = results[0][0]
    quality_of_match = 0
    for resp in responses[0]:
        if resp == classification:
            quality_of_match += 1
    quality_of_match = 100 * quality_of_match / len(responses[0])
    return {'classification': str(classification), 'quality_of_match': str(quality_of_match)}
####################################################################################################
