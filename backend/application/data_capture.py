import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import sys
import os

"""
Note: this code is inspired by the following video, and it is only for getting initial test data.
TODO: reference tutorial video
"""


def get_signs(filename):
    desired_shape = (200, 200)
    offset = 30
    hand_detector = HandDetector(maxHands=1)
    capture = cv.VideoCapture(0)
    i = 0
    while i < 100:
        s, img = capture.read()
        cv.imwrite(filename + str(i) + '.png', img)
        hands, hands_img = hand_detector.findHands(img)
        try:
            x, y, w, h = hands[0]['bbox']
            cropped = hands_img[y-offset:y+offset+h, x-offset:x+w+offset]
            cropped = cv.resize(cropped, desired_shape)
            cv.imshow('img', img)
            cv.waitKey(1)
            i += 1
        except Exception as e:
            print(e)
            os.remove(filename + str(i) + '.png')


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage <filename>')
    else:
        get_signs(sys.argv[1])
