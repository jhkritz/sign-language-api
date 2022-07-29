from flask import current_app as app, Response, request
from .models import user, SignLanguageLibrary, Sign
from zipfile import ZipFile
import csv


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
        lib = SignLanguageLibrary(title=lib_name)
        db.session.add(lib)
        reader = csv.reader(sign_meanings, delimiter=',')
        zpfl = ZipFile(zipped_images.stream._file)
        for line in reader:
            image_file_name = line[0]
            sign_meaning = line[1]
            zpfl.extract(image_file_name, path=img_path)
            sign = Sign(meaning=sign_meaning, image_url=img_path+image_file_name, library_id=lib.id)
            db.session.add(sign)
    except KeyError:
        return Response(status=400)
    return Response(status=200)
