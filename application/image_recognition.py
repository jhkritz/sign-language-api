import numpy as np
import cv2 as cv

"""
Experimentation with opencv.

Preprocesses images by grayscaling and flattening them (so that we can work with 1D vectors when
training and classifying). Classifies a sample image, 'A1234.jpg', using an implementation of the 
K-NearestNeighbours algorithm.

After some slight modifications to this code we should have a functioning classifier for the API.
"""


def read_and_preprocess_image(char):
    # Get an image from the images associated with <char> letter of the alphabet.
    filename = '../asl_alphabet_train/{0}/{0}1234.jpg'.format(char)
    return grayscale_and_flatten(cv.imread(filename))


def grayscale_and_flatten(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY).flatten()


def test_simplest_classify():
    # Alphabet just used to build filename for loading images from the directory with the sample
    # data.
    ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # The name of the image that will be classified
    INITIAL_TEST_IMAGE = '../asl_alphabet_train/A/A1234.jpg'
    data = np.array([im for im in map(read_and_preprocess_image, ALPHABET)], dtype=np.float32)
    test_images = np.array([grayscale_and_flatten(cv.imread(INITIAL_TEST_IMAGE))], dtype=np.float32)
    # Assuming each image is in it's own class (i.e A, B, C, etc..)
    labels = np.arange(len(ALPHABET), dtype=np.float32)
    knn = cv.ml.KNearest_create()
    knn.train(data, cv.ml.ROW_SAMPLE, labels)
    retval, results, responses, dists = knn.findNearest(test_images, k=12)
    # The test image is from the training data for the letter A, so we expect it to be classified
    # accordingly.
    assert results[0] == labels[0]


if __name__ == '__main__':
    import nose2
    nose2.main()
