import time

import cv2

from gesplay.constants import Gestures
from gesplay.gesture_handler import GestureHandler
from gesplay.hand_detector import HandDetector
from gesture_decoder import GestureDecoder


class GesPlay:
    def __init__(self):
        self.gesture_handler = GestureHandler({
            Gestures.POINTING_UP.value: 'left',
            Gestures.THUMB_UP.value: 'right',
            Gestures.OPEN_PALM.value: 'space'
        })
        self.gesture_decoder = GestureDecoder(self.gesture_handler)
        self.hand_detector = HandDetector()

    def start(self):
        cap = cv2.VideoCapture(0)

        p_time = c_time = 0

        while True:
            success, img = cap.read()
            self.gesture_decoder.decode_gestures(img)
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            img_with_landmarks = self.hand_detector.draw_landmarks(img)
            cv2.imshow("Image", img_with_landmarks)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gesture_handler.cleanup()
                break


GesPlay().start()
