"""
Tests some routes and the classification feature.

Note: We used Postman to generate the HTTP requests.
"""

import os
import subprocess
import nose2
import json
import requests

access_token = ""
lib_name = "ci_cd_test_lib"
input_data_path = os.getcwd() + '/input_data'


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
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()['access']


def create_library():
    """
    Creates the test library.
    """
    url = "http://127.0.0.1:5000/library/createlibrary"
    payload = {
        'library_name': f'{lib_name}',
        'description': 'Test library'
    }
    files = []
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200


def delete_library():
    """
    Deletes the test library.
    """
    url = f"http://127.0.0.1:5000/library/deletelibrary?library_name={lib_name}"
    payload = {}
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("DELETE", url, headers=headers, data=payload)


def upload_images():
    url = "http://127.0.0.1:5000/library/uploadsigns"
    sign_names = ['a', 'b', 'c']
    for sign_name in sign_names:
        payload = {'sign_name': f'{sign_name}',
                   'lib_name': f'{lib_name}'}
        files = [
            (
                'zip_file',
                (
                    f'{sign_name}.zip',
                    open(f'{input_data_path}/{sign_name}.zip', 'rb'), 'application/zip'
                )
            )
        ]
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        assert response.status_code == 200


def classify_image():
    url = "http://localhost:5000/library/classifyimage"
    payload = {'library_name': lib_name}
    sign_name = 'a'
    files = [
        (
            'image',
            (
                '{sign_name}.png',
                open(f'{input_data_path}/{sign_name}.png', 'rb'), 'image/png'
            )
        )
    ]
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
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
    nose2.main()
