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
            sign = Sign(meaning=sign_meaning, image_url=image_file_name, library_id=lib.id)
            db.session.add(sign)
    except KeyError:
        return Response(status=400)
    return Response(status=200)


@app.route('/library/signs/<library_name>', methods=['GET'])
def get_signs():
    img_url_base = '/library/image/'
    lib = SignLanguageLibrary.query.first_or_404(title=library_name)
    # The image url will be incorrect and the elements of the list below are likely not formatted
    # correctly. Plan to correct this soon
    signs = [sign for sign in lib.signs]
    return {'signs': signs}


def get_sign_image():
