import pyautogui


class MouseMovement:
    LEFT = 'left'
    RIGHT = 'right'
    LEFT_CLICK = 'left_click'


class GestureHandler:
    def __init__(self, gesture_to_key_map, gesture_to_mouse_map=None):
        self.active_keys = set()
        self.gesture_to_key_map = gesture_to_key_map or dict()
        self.gesture_to_mouse_map = gesture_to_mouse_map or dict()

    def set_gesture_to_key_map(self, gesture_to_key_map):
        print(f"Setting gesture to key map: {gesture_to_key_map}")
        self.gesture_to_key_map = gesture_to_key_map

    def handle_gestures(self, detected_gestures):
        if self.gesture_to_mouse_map:
            self.handle_mouse_gestures(detected_gestures)

        if self.gesture_to_key_map:
            self.handle_keyboard_gestures(detected_gestures)

    def handle_mouse_gestures(self, detected_gestures):
        for gesture in detected_gestures:
            movement_type = self.gesture_to_mouse_map.get(gesture)
            if movement_type:
                if movement_type == MouseMovement.LEFT_CLICK:
                    print("Clicking")
                    pyautogui.click()
                elif movement_type == MouseMovement.LEFT:
                    pyautogui.moveRel(-50, 0)
                elif movement_type == MouseMovement.RIGHT:
                    pyautogui.moveRel(50, 0)

    # def handle_keyboard_gestures2(self, detected_gestures):
    #     for gesture in detected_gestures:
    #         key = self.gesture_to_key_map.get(gesture)
    #         if key:
    #             pyautogui.press(key)

    def handle_keyboard_gestures(self, detected_gestures):
        # print("Handling gestures: ", detected_gestures)

        if not detected_gestures:
            # Release all keys when no gestures detected
            for key in list(self.active_keys):
                self.release_key(key)
            return

        # Determine which keys should be pressed
        should_be_pressed = set()
        for gesture in detected_gestures:
            key = self.gesture_to_key_map.get(gesture)
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