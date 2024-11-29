import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils


class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mpHands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def draw_landmarks(self, image):
        """
        Returns new image with landmarks on the given image
        """
        image_copy = image.copy()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_image)

        if not results.multi_hand_landmarks:
            return image_copy

        for hand_idx in range(len(results.multi_handedness)):
            hand = results.multi_hand_landmarks[hand_idx]
            mpDraw.draw_landmarks(image_copy, hand, mpHands.HAND_CONNECTIONS)

        return image_copy
