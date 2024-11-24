import time

import cv2
import mediapipe as mp
import pyautogui

from gesplay.constants import Hand
from gesplay.hand_detector import HandDetector
from gesture_decoder import GestureDecoder, Gestures


class GestureHandler:
    def __init__(self):
        self.active_keys = set()
        self.gesture_to_key = {
            (Hand.RIGHT.value, Gestures.PINKY_OUT.value): 'left',
            (Hand.RIGHT.value, Gestures.THUMB_OUT.value): 'right',
            (Hand.LEFT.value, Gestures.INDEX_OUT.value): 'space'
        }

    def handle_gestures(self, detected_gestures):
        print("Handling gestures: ", detected_gestures)

        if not detected_gestures:
            # Release all keys when no gestures detected
            for key in list(self.active_keys):
                self.release_key(key)
            return

        # Determine which keys should be pressed
        should_be_pressed = set()
        for gesture in detected_gestures:
            key = self.gesture_to_key.get(gesture)
            if key:
                should_be_pressed.add(key)

        # Press new keys
        for key in should_be_pressed:
            if key not in self.active_keys:
                self.press_key(key)

        # Release keys that shouldn't be pressed anymore
        for key in list(self.active_keys):
            if key not in should_be_pressed:
                self.release_key(key)

    def press_key(self, key):
        pyautogui.keyDown(key)
        self.active_keys.add(key)

    def release_key(self, key):
        pyautogui.keyUp(key)
        self.active_keys.remove(key)

    def cleanup(self):
        for key in list(self.active_keys):
            self.release_key(key)


class GesPlay:
    def __init__(self):
        self.hand_detector = HandDetector()
        self.gesture_decoder = GestureDecoder()
        self.gesture_handler = GestureHandler()

    def start(self):
        cap = cv2.VideoCapture(0)

        p_time = 0
        c_time = 0

        # Add state to prevent continuous triggering
        last_gesture = None
        gesture_cooldown = 0
        COOLDOWN_FRAMES = 10  # Adjust this value to control how often the event can trigger

        while True:
            success, img = cap.read()

            try:
                landmarks = self.hand_detector.find_landmarks(img)
                gestures = []
                for label, hand_landmarks in landmarks:
                    hg = self.gesture_decoder.decode_gestures(hand_landmarks, img)
                    gestures.extend((label, g) for g in hg)

                if gestures:
                    print(gestures)
                    self.gesture_handler.handle_gestures(gestures)
                # if landmarks:
                #     print(landmarks)
            except Exception as e:
                print(f"Error: {e}")
                self.gesture_handler.cleanup()

            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            cv2.imshow("Image", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.gesture_handler.cleanup()
                break

            if gesture_cooldown > 0:
                gesture_cooldown -= 1


GesPlay().start()
