from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import sys
import os

"""
Note: this code is inspired by the following video, and it is only for getting initial test data.
TODO: reference tutorial video
"""


def get_signs(filename):
    hand_detector = HandDetector(maxHands=1)
    capture = cv.VideoCapture(0)
    i = 0
    while i < 100:
        s, img = capture.read()
        cv.imwrite(filename + str(i) + '.png', img)
        hands, hands_img = hand_detector.findHands(img)
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
