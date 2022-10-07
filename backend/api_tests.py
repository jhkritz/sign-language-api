"""
Tests some of the API routes and the classification feature.

Note: We used Postman to generate the HTTP requests.
"""

import os
import json
import requests
import nose2

LIB_NAME = "ci_cd_test_lib"
input_data_path = os.getcwd()
if not input_data_path.find('/backend') >= 0:
    input_data_path += '/backend/input_data'
else:
    input_data_path += '/input_data'


def get_access_token():
    """
    Gets an access token for testing.
    """
    url = "http://127.0.0.1:5000/login"
    payload = json.dumps({
        "email": "ci@cd.com",
        "password": "continuous"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
    return response.json()['access']


def get_api_key():
    """
    Gets an API key
    """
    url = "http://127.0.0.1:5000/api/resetapikey"
    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload, timeout=30)
    return response.json()['api_key']


def create_library():
    """
    Creates the test library.
    """
    url = "http://127.0.0.1:5000/api/library/createlibrary"
    payload = {'key': api_key,
               'library_name': LIB_NAME,
               'description': 'none'}
    files = [
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, timeout=30)
    assert response.status_code == 200


def delete_library():
    """
    Deletes the test library.
    """
    url = f"http://127.0.0.1:5000/api/library/deletelibrary?library_name={LIB_NAME}&key={api_key}"
    payload = {}
    headers = {}
    requests.request("DELETE", url, headers=headers, data=payload, timeout=30)


def upload_images():
    """
    Uploads the training data.
    """
    url = "http://127.0.0.1:5000/api/library/uploadsigns"
    sign_names = ['a', 'b', 'c']
    for sign_name in sign_names:
        payload = {'key': api_key,
                   'sign_name': f'{sign_name}',
                   'lib_name': f'{LIB_NAME}'}
        with open(f'{input_data_path}/{sign_name}.zip', 'rb') as zpfl:
            files = [
                (
                    'zip_file',
                    (
                        f'{sign_name}.zip',
                        zpfl, 'application/zip'
                    )
                )
            ]
            headers = {}
            response = requests.request("POST", url, headers=headers,
                                        data=payload, files=files, timeout=30)
            assert response.status_code == 200


def classify_image():
    """
    Checks that the server correctly classifies one
    of the training images.
    """
    url = "http://localhost:5000/api/library/classifyimage"
    payload = {'key': api_key, 'library_name': LIB_NAME}
    sign_name = 'a'
    with open(f'{input_data_path}/{sign_name}.png', 'rb') as img:
        files = [
            (
                'image',
                (
                    '{sign_name}.png',
                    img, 'image/png'
                )
            )
        ]
        headers = {
        }
        response = requests.request("POST", url, headers=headers,
                                    data=payload, files=files, timeout=30)
        assert response.status_code == 200
        assert response.json()['result']['classification'] == sign_name


def test_classification():
    """
    Tests the classification feature.
    """
    delete_library()
    # create a library.
    create_library()
    # upload some images.
    upload_images()
    # classify an image.
    classify_image()


if __name__ == '__main__':
    access_token = get_access_token()
    api_key = get_api_key()
    nose2.main()
