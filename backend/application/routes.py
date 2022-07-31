from flask import current_app as app, Response, request, send_from_directory
from .models import user, SignLanguageLibrary, Sign
from zipfile import ZipFile
import numpy as np
from . import db
import cv2 as cv
import csv
import os


@app.route("/")
def home():
    return "Hello World!"


@app.route('/library/upload', methods=['POST'])
def upload_library():
    try:
        # Request arguments and files
        sign_meanings = request.files['sign_meanings']
        zipped_images = request.files['zipped_images']
        lib_name = request.form.to_dict()['library_name']
        # Path this library's images will be saved to
        img_path = app.config['IMAGE_PATH'] + '/' + lib_name
        lib = SignLanguageLibrary(name=lib_name)
        db.session.add(lib)
        db.session.commit()
        reader = csv.reader(sign_meanings, delimiter=',')
        zpfl = ZipFile(zipped_images.stream._file)
        for line in reader:
            image_file_name = line[0]
            sign_meaning = line[1]
            zpfl.extract(image_file_name, path=img_path)
            sign = Sign(meaning=sign_meaning, image_filename=image_file_name, library_id=lib.id)
            db.session.add(sign)
        db.session.commit()
    except KeyError:
        return Response(status=400)
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


def preprocess_image(image, desired_shape):
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    if image.shape != desired_shape:
        image = cv.resize(image, desired_shape)
    return image.flatten()
