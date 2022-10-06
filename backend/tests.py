import subprocess
import nose2
import json


access_token = ""


def log_process(proc):
    print('returncode:\n' + str(proc.returncode))
    print('stdout:\n' + str(proc.stdout.decode('utf-8')))
    print('stderr:\n' + str(proc.stderr.decode('utf-8')))


def get_access_token():
    cmd = "curl --location --request POST 'http://127.0.0.1:5000/login'\
            --header 'Content-Type: application/json' \
            --data-raw '{\"email\": \"ci@cd.com\", \"password\": \"continuous\"}'"
    completed = subprocess.run(cmd, capture_output=True, shell=True)
    output = json.loads(completed.stdout.decode('utf-8'))
    return output['access']


def test_get_libraries():
    cmd = "curl --location --request GET 'http://127.0.0.1:5000/libraries/getall'\
            --header 'Authorization: Bearer {}'".format(access_token)
    completed = subprocess.run(cmd, capture_output=True, shell=True)
    log_process(completed)
    assert completed.returncode == 0
    output = completed.stdout.decode('utf-8')
    assert output.find('libraries') >= 0


if __name__ == '__main__':
    access_token = get_access_token()
    nose2.main()
