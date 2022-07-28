import numpy as np
import cv2 as cv

"""
Experimentation with opencv
"""


def preprocess_images(images):
    n, m, k = images.shape[:3]
    d = m*k
    greyscaled = np.zeros((n, d), dtype=np.uint8)
    i = 0
    for img in images:
        # Convert to greyscale and flatten
        temp = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        greyscaled[i, :] = temp.flatten()
        i += 1
    # greyscaled = np.array(greyscaled)
    return greyscaled


def get_trained_knn(training_data, labels):
    assert training_data.shape[0] == labels.shape[0]
    knn = cv.ml.KNearest_create()
    knn.train(training_data.astype(np.float32), cv.ml.ROW_SAMPLE, labels[:np.newaxis])
    return knn


def test_classify():
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    INITIAL_TEST_IMAGE = '../asl_alphabet_train/A/A1234.jpg'
    labels = np.arange(len(ALPHABET), dtype=np.float32)
    data = []
    for i in range(len(ALPHABET)):
        filename = '../asl_alphabet_train/{0}/{0}1234.jpg'.format(ALPHABET[i])
        img = cv.imread(filename)
        data += [img]
    data = np.array(data)
    data = preprocess_images(data)
    data = data[:, :, np.newaxis]
    knn = get_trained_knn(data, labels)
    test_image = preprocess_images(np.array([cv.imread(INITIAL_TEST_IMAGE)]))[0]
    test_images = test_image[np.newaxis, :, np.newaxis]
    test_images = test_images.astype(np.float32)
    retval, results, responses, dists = knn.findNearest(test_images, k=12)
    assert results[0] == labels[0]


"""
def test_preprocess_images():
    INITIAL_TEST_IMAGE = '../asl_alphabet_train/A/A1234.jpg'
    images = np.array([cv.imread(INITIAL_TEST_IMAGE)])
    # Delete the RGB dimension
    newShape = images.shape[:3]
    # Receive matrix of flattened vectors
    preprocessed = preprocess_images(images)
    # Reshape the matrix
    preprocessed = np.reshape(preprocessed, newShape)
    cv.imshow('before', images[0])
    cv.imshow('after', preprocessed[0])
    cv.waitKey(0)
    assert True
"""


if __name__ == '__main__':
    import nose2
    nose2.main()
