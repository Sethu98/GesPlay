import random
import time

import pyautogui
import keyboard
from pynput.keyboard import Key, Controller


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
        pyautogui.keyUp('left')
        print('released', key)


def main_keyboard():
    time.sleep(3)
    keyboard.write("Well hello there")


main_py_auto_gui()
