import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv

"""
Note: this code is inspired by the following video, and it is only for getting initial test data.
TODO: reference tutorial video
"""


def get_signs():
    desired_shape = (200, 200)
    offset = 30
    hand_detector = HandDetector(maxHands=1)
    capture = cv.VideoCapture(0)
    # TODO: Hard code the file of whatever sign you want to generate.
    filename = 'c.jpg'
    while True:
        s, img = capture.read()
        hands, hands_img = hand_detector.findHands(img)
        try:
            x, y, w, h = hands[0]['bbox']
            cropped = hands_img[y-offset:y+offset+h, x-offset:x+w+offset]
            cropped = cv.resize(cropped, desired_shape)
            cv.imshow('cropped', cropped)
            cv.waitKey(1)
            cv.imwrite(filename, cropped)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_signs()
