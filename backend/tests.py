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


def test_classification_accuracy():
    lib_name = "ClassificationAccuracy"
    signs = ['a', 'b', 'c']
    num_correct = 0
    total = 0
    positive_confidence = 0
    negative_confidence = 0
    signs_per_dir = 10
    for sign in signs:
        count = 0
        for img_name in os.listdir('./test_data/{}'.format(sign)):
            print(img_name)
            if count >= signs_per_dir:
                break
            count += 1
            path_to_image = "./test_data/{}/{}".format(sign, img_name)
            # path_to_image = "/home/river/cs344/sign_language_recognition/backend/test_data/" + img_name
            cmd = "curl --location --request POST 'http://localhost:5000/library/classifyimage' \
                    --form 'library_name=\"{}\"' \
                    --form 'image=@\"{}\"'".format(lib_name, path_to_image)
            completed = subprocess.run(cmd, capture_output=True, shell=True)
            try:
                output = json.loads(completed.stdout.decode('utf-8'))
                res = output['result']
                if res['classification'] == 'small_' + sign:
                    num_correct += 1
                    positive_confidence += float(res['quality_of_match'])
                else:
                    negative_confidence += float(res['quality_of_match'])
                total += 1
                print(output['result'])
            except Exception as e:
                print(e)
    avg_pc = positive_confidence / num_correct
    avg_nc = negative_confidence / (total - num_correct)
    ratio_correct = num_correct / total
    print(avg_pc)
    print(avg_nc)
    print(ratio_correct)


if __name__ == '__main__':
    nose2.main()
