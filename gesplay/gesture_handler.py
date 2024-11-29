import pyautogui


class GestureHandler:
    def __init__(self, gesture_to_key_map):
        self.active_keys = set()
        self.gesture_to_key = gesture_to_key_map

    def handle_gestures(self, detected_gestures):
        # print("Handling gestures: ", detected_gestures)

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