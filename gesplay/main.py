import json
import os.path
import select
import sys
import threading
import time

import cv2

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gesplay.gesture_handler import GestureHandler
from gesplay.hand_detector import HandDetector
from gesture_decoder import GestureDecoder


class GesPlay:
    def __init__(self, gesture_handler: GestureHandler):
        # # Bubble trouble
        # self.gesture_handler = GestureHandler({
        #     Gestures.POINTING_UP.value: 'left',
        #     Gestures.THUMB_UP.value: 'right',
        #     Gestures.OPEN_PALM.value: 'space'
        # }, None)

        # Mophead dash
        # self.gesture_handler = GestureHandler({
        #     Gestures.POINTING_UP.value: 'left',
        #     Gestures.THUMB_UP.value: 'right',
        #     Gestures.OPEN_PALM.value: 'up',
        #     Gestures.THUMB_DOWN.value: 'down'
        # }, None)

        # self.gesture_handler = GestureHandler(None, {
        #     Gestures.POINTING_UP.value: 'left',
        #     Gestures.THUMB_UP.value: 'right',
        #     Gestures.THUMB_DOWN.value: 'left_click'
        # })

        # Dino game
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


def check_input(timeout=0.1):
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().strip()

    return None


def handle_inputs(gesture_handler: GestureHandler):
    while True:
        user_input = check_input()
        if not user_input:
            continue

        words = user_input.split()
        # print(words)

        if len(words) != 2:
            print("Invalid input")
            continue

        command, arg = words
        if command == "play":
            layout = get_layout(arg)
            if layout:
                gesture_handler.set_gesture_to_key_map(layout)
                print(f"Switched to {arg}")
        else:
            print(f"Failed to switch to {arg}")


def get_layout(game_name):
    file_path = f'layouts/{game_name}.json'

    try:
        with open(file_path) as handle:
            content = handle.read()
            return json.loads(content)
    except:
        return None


def start_gesplay():
    layout = get_layout('dino')
    gesture_handler = GestureHandler(layout)
    t = threading.Thread(target=handle_inputs, args=(gesture_handler,))
    t.start()

    GesPlay(gesture_handler).start()
    t.join()


if __name__ == "__main__":
    start_gesplay()
