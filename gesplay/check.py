import os

import pyautogui

from gesplay.constants import LAYOUTS_FOLDER_PATH

for file in os.listdir(LAYOUTS_FOLDER_PATH):
    print(file)

print(pyautogui.KEYBOARD_KEYS)
