from mediapipe.python.solutions.hands import Hands

from gesplay.constants import Gestures, Hand


class GestureDecoder:
    def decode_gestures(self, hand_landmarks, img):
        if not hand_landmarks:
            return []

        gestures = []
        # we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        # details: https://google.github.io/mediapipe/solutions/hands

        if hand_landmarks[4][3] == Hand.RIGHT.value and hand_landmarks[4][1] > hand_landmarks[3][1]:  # Right Thumb
            gestures.append(Gestures.THUMB_OUT.value)
        elif hand_landmarks[4][3] == Hand.LEFT.value and hand_landmarks[4][1] < hand_landmarks[3][1]:  # Left Thumb
            gestures.append(Gestures.THUMB_OUT.value)

        if hand_landmarks[8][2] < hand_landmarks[6][2]:  # Index finger
            gestures.append(Gestures.INDEX_OUT.value)
        # if hand_landmarks[12][2] < hand_landmarks[10][2]:     #Middle finger
        #     count = count+1
        # if hand_landmarks[16][2] < hand_landmarks[14][2]:     #Ring finger
        #     count = count+1
        if hand_landmarks[20][2] < hand_landmarks[18][2]:  # Little finger
            gestures.append(Gestures.PINKY_OUT.value)

        return gestures
