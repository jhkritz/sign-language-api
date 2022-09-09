import subprocess
import json
import nose2
import os


def log_process(proc):
    print('returncode:\n' + str(proc.returncode))
    print('stdout:\n' + str(proc.stdout.decode('utf-8')))
    print('stderr:\n' + str(proc.stderr.decode('utf-8')))


def test_get_libraries():
    cmd = "curl --location --request GET 'http://127.0.0.1:5000/libraries/getall'"
    completed = subprocess.run(cmd, capture_output=True, shell=True)
    log_process(completed)
    assert completed.returncode == 0
    assert completed.stdout.decode('utf-8').find('libraries') >= 0


if __name__ == '__main__':
    nose2.main()
