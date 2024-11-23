import time
from pynput.keyboard import Key, Controller


def test_keyboard_input():
    keyboard = Controller()

    print("Keyboard test starting in 5 seconds...")
    print("Please open a text editor to see the results.")
    time.sleep(5)

    # Type a string
    keyboard.type("Hello, world!")
    time.sleep(1)

    # Press and release the enter key
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(1)

    # Type another string
    keyboard.type("This is a test of pynput keyboard control.")
    time.sleep(1)

    print("Keyboard test completed.")


if __name__ == "__main__":
    test_keyboard_input()