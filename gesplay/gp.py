import threading
import time

import cv2

from gesplay.gesture_handler import GestureHandler
from gesplay.hand_detector import HandDetector
from gesture_decoder import GestureDecoder


class GesPlay:
    def __init__(self, gesture_handler: GestureHandler):
        self.gesture_handler = gesture_handler
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

    # def set_game(self, game):
    #     layout = Utils.read_layout(game)
    #     if layout:
    #         self.gesture_handler.set_gesture_to_key_map(layout)

# class GesPlay:
#     def __init__(self, gesture_handler: GestureHandler):
#         self.gesture_handler = gesture_handler
#         self.gesture_decoder = GestureDecoder(self.gesture_handler)
#         self.hand_detector = HandDetector()
#         self.is_running = False
#         self.capture_thread = None
#         self.cap = None
#
#     def start(self):
#         if self.is_running:
#             return
#
#         self.is_running = True
#         self.cap = cv2.VideoCapture(0)
#         self.capture_thread = threading.Thread(target=self._capture_loop)
#         self.capture_thread.start()
#
#     def stop(self):
#         self.is_running = False
#         if self.capture_thread:
#             self.capture_thread.join()
#         if self.cap:
#             self.cap.release()
#         cv2.destroyAllWindows()
#         self.gesture_handler.cleanup()
#
#     def _capture_loop(self):
#         p_time = c_time = 0
#
#         while self.is_running:
#             success, img = self.cap.read()
#             if not success:
#                 continue
#
#             # Decode and handler gesture
#             thread = threading.Thread(target=self.gesture_decoder.decode_gestures, args=(img,))
#             thread.start()
#             thread.join()
#
#             c_time = time.time()
#             fps = 1 / (c_time - p_time)
#             p_time = c_time
#             cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
#             img_with_landmarks = self.hand_detector.draw_landmarks(img)
#             cv2.imshow("Image", img_with_landmarks)
#
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 self.stop()
#                 break
#
#     def set_game(self, game):
#         layout = Utils.read_layout(game)
#         if layout:
#             self.gesture_handler.set_gesture_to_key_map(layout)