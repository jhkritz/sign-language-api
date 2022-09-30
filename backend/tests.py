import subprocess
import nose2


def log_process(proc):
    print('returncode:\n' + str(proc.returncode))
    print('stdout:\n' + str(proc.stdout.decode('utf-8')))
    print('stderr:\n' + str(proc.stderr.decode('utf-8')))


def test_get_libraries():
    cmd = "curl --location --request GET 'http://127.0.0.1:5000/libraries/getall' --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2MzIwNDEyMCwianRpIjoiY2ViNzc4YWUtYzg4NC00N2IzLWEwZTUtMTE2ZWM1YzAwYmNmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjYzMjA0MTIwLCJleHAiOjE2NjMyMDUwMjB9.lCA-yNR9SxrrZZaOs-ItU-jCvz7wINySCoEiBLhgyuY'"
    completed = subprocess.run(cmd, capture_output=True, shell=True)
    log_process(completed)
    assert completed.returncode == 0
    output = completed.stdout.decode('utf-8')
    assert output.find('libraries') >= 0 or output.find('expired') >= 0


if __name__ == '__main__':
    nose2.main()
