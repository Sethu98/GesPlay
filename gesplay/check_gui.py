import random
import threading
import time

import keyboard
import pyautogui


class KeyBoardUtil:
    @staticmethod
    def key_down_for_secs(key, secs):
        # pyautogui.press(key, 20)
        pyautogui.keyDown(key)
        time.sleep(secs)
        pyautogui.keyUp(key)

    def left(self):
        t = threading.Thread(target=KeyBoardUtil.key_down_for_secs, args=('left', 0.2), daemon=True)
        t.start()


        # self.key_down_for_secs('left', 0.1)

    def right(self):
        t = threading.Thread(target=KeyBoardUtil.key_down_for_secs, args=('left', 0.2))
        t.start()

        # self.key_down_for_secs('right', 0.1)


def main_py_auto_gui():
    time.sleep(3)
    print("Started press")

    for i in range(15):
        if i % 2:
            print("Pressing space")
            pyautogui.press('space')

        val = random.randint(0, 1)
        key = 'left' if val == 0 else 'right'

        pyautogui.keyDown(key)
        print('pressed', key)
        time.sleep(1)
        pyautogui.keyUp(key)
        print('released', key)


def main_keyboard():
    time.sleep(3)
    keyboard.write("Well hello there")


# main_py_auto_gui()
