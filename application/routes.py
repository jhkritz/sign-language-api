from flask import current_app as app, Response, request, send_from_directory
from .models import user, SignLanguageLibrary, Sign
from zipfile import ZipFile
import csv
from . import db
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
        lib = SignLanguageLibrary(title=lib_name)
        db.session.add(lib)
        db.session.commit()
        reader = csv.reader(sign_meanings, delimiter=',')
        zpfl = ZipFile(zipped_images.stream._file)
        for line in reader:
            image_file_name = line[0]
            sign_meaning = line[1]
            zpfl.extract(image_file_name, path=img_path)
            sign = Sign(meaning=sign_meaning, image_url=image_file_name, library_id=lib.id)
            db.session.add(sign)
        db.session.commit()
    except KeyError:
        return Response(status=400)
    return Response(status=200)


@app.route('/library/signs', methods=['GET'])
def get_signs():
    library_name = request.args['library_name']
    img_url_base = '/library/image'
    lib = SignLanguageLibrary.query.filter_by(title=library_name).first_or_404()
    signs = [sign.to_dict(img_url_base) for sign in lib.signs]
    return {'signs': signs}


@app.route('/library/image', methods=['GET'])
def get_sign_image():
    lib_name = request.args['library_name']
    img_name = request.args['image_name']
    path = app.config['IMAGE_PATH'] + '/' + lib_name
    return send_from_directory(path, img_name)


#Endpoint to upload a single sign with a name
@app.route('/library/uploadsign', methods=['POST'])
def uploadsign():
    try:
        libid = request.form.get('lib_id')
        sign_name = request.form.get('sign_name')
        image = request.files['image_file']
        lib_name = SignLanguageLibrary.query.filter_by(id=libid).first().title

        img_path = app.config['IMAGE_PATH'] + '/' + lib_name + '/' + sign_name + '.jpg'
        image.save(img_path)

        sign = Sign(meaning=sign_name, image_url = img_path,  library_id=libid)
        db.session.add(sign)
        db.session.commit()
    except KeyError:
        return Response(status=400)
    return Response(status=200)

@app.route('/library/createlibrary', methods=['POST'])
def createlibrary():
    libname = request.form.get('library_name')
    library = SignLanguageLibrary(title = libname)
    os.makedirs(app.config['IMAGE_PATH'] + '/' + libname)
    db.session.add(library)
    db.session.commit()
    return Response(status=200)