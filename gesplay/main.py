import threading
import time

import cv2

from gesplay.constants import Gestures
from gesplay.gesture_handler import GestureHandler
from gesplay.hand_detector import HandDetector
from gesture_decoder import GestureDecoder


class GesPlay:
    def __init__(self):
        # # Bubble trouble
        # self.gesture_handler = GestureHandler({
        #     Gestures.POINTING_UP.value: 'left',
        #     Gestures.THUMB_UP.value: 'right',
        #     Gestures.OPEN_PALM.value: 'space'
        # }, None)

        # Mophead dash
        self.gesture_handler = GestureHandler({
            Gestures.POINTING_UP.value: 'left',
            Gestures.THUMB_UP.value: 'right',
            Gestures.OPEN_PALM.value: 'up',
            Gestures.THUMB_DOWN.value: 'down'
        }, None)

        # self.gesture_handler = GestureHandler(None, {
        #     Gestures.POINTING_UP.value: 'left',
        #     Gestures.THUMB_UP.value: 'right',
        #     Gestures.THUMB_DOWN.value: 'left_click'
        # })

        # Dino game
        # self.gesture_handler = GestureHandler({
        #     Gestures.THUMB_UP.value: 'space'
        # }, None)
        self.gesture_decoder = GestureDecoder(self.gesture_handler)
        self.hand_detector = HandDetector()

    def start(self):
        cap = cv2.VideoCapture(0)

        p_time = c_time = 0

        while True:
            success, img = cap.read()

            # Decode and handler gesture
            thread = threading.Thread(target=self.gesture_decoder.decode_gestures, args=(img,))
            thread.start()
            thread.join()

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
