from flask import current_app as app
from .models import user
from zipfile import ZipFile
import csv


@app.route("/")
def home():
    return "Hello World!"


@app.route('/library/upload', methods=['POST'])
def upload_library():
    try:
        sign_meanings = request.files['sign_meanings']
        zipped_images = request.files['zipped_images']
        img_path = app.config['IMAGE_PATH'] + '/' + request.form.to_dict()['library_name']
        reader = csv.reader(sign_meanings, delimiter=',')
        zpfl = ZipFile(zipped_images.stream._file)
        for line in reader:
            image_file_name = line[0]
            sign_meaning = line[1]
            zpfl.extract(image_file_name, )
        pass
        if request.files['zipped_images']:
            pass
    except KeyError:
        print('missing some files')
