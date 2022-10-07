"""
Captures images that contain hands from the user's webcam.

Note: this code is inspired by the following video, and it is only for getting initial test data.
TODO: reference tutorial video
"""

import sys
import os
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv


def get_signs(filename):
    """
    Reads frames from the user's webcam, checks if
    it contains hands and saves it if it does.
    """
    hand_detector = HandDetector(maxHands=1)
    capture = cv.VideoCapture(0)
    i = 0
    while i < 100:
        img = capture.read()[1]
        cv.imwrite(filename + str(i) + '.png', img)
        hands = hand_detector.findHands(img)[0]
        if len(hands) < 1:
            os.remove(filename + str(i) + '.png')
            continue
        cv.imshow('img', img)
        cv.waitKey(1)
        i += 1


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage <filename>')
    else:
        get_signs(sys.argv[1])
