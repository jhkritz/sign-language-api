import base64
import io
import time

import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from flask import request, current_app as app, Response

from .models import SignLanguageLibrary

hand_detector = HandDetector(maxHands=1)
desired_shape = (200, 200)


def classify():
    data_image = request.files['image'].read()
    lib_name = request.form['library_name']
    b_array = np.asarray(bytearray(io.BytesIO(data_image).read()), dtype='uint8')
    image = cv2.imdecode(b_array, cv2.IMREAD_COLOR)
    processed_image = preprocess_image(image)
    if processed_image is not None:
        flat_image = processed_image.flatten()
        processed_image = cv2.imencode('.png', processed_image)[1]
        image_out = 'data:image/png;base64,' + base64.b64encode(processed_image).decode('utf-8')
        start = time.time()
        result = knn_classify(lib_name, flat_image)
        end = time.time()
        print('Time taken = ' + str(end - start))
        return {'processedImage': image_out, 'result': result}
    else:
        print('processed_image is none')
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
        img = cv2.imread(lib_path + sign.meaning + '/' + sign.image_filename)
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
            cropped = hands_img[y - offset:y + offset + h, x - offset:x + w + offset]
            cropped = cv2.resize(cropped, desired_shape)
            return cropped
        except Exception as e:
            print(e)
    # Return None so that classification is aborted if hands aren't found.
    return None


def knn_classify(lib_name, flat_image):
    data, labels, label_meanings = get_data_and_labels(lib_name)
    k = min(int(data.shape[0] / len(label_meanings)), 20)
    knn = cv2.ml.KNearest_create()
    knn.train(data, cv2.ml.ROW_SAMPLE, labels)
    to_classify = np.array(flat_image[np.newaxis, :], dtype=np.float32)
    results, responses = knn.findNearest(to_classify, k=k)[1:-1]
    classification = results[0][0]
    meaning = label_meanings[int(classification)]
    quality_of_match = 0
    for resp in responses[0]:
        if resp == classification:
            quality_of_match += 1
    quality_of_match = 100 * quality_of_match / len(responses[0])
    return {'classification': meaning, 'quality_of_match': str(quality_of_match)}
