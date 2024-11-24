from collections import namedtuple

import cv2
import mediapipe as mp

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

LandmarkRecord = namedtuple("LandmarkRecord", ['lm_id', 'pos_x', 'pos_y', 'label'])

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = mpHands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def find_landmarks(self, image):
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe ne
        landmarks = self.find_hand_landmarks(image, rgb_img)

        return landmarks

    def find_hand_landmarks(self, orig_image, rgb_image, draw=True):
        results = self.hands.process(rgb_image)

        if not results.multi_hand_landmarks:
            return []

        landmark_list = []

        for hand_idx in range(len(results.multi_handedness)):
            label = results.multi_handedness[hand_idx].classification[0].label
            # Account for inversion in webcam
            if label == "Left":
                label = "Right"
            elif label == "Right":
                label = "Left"

            cur_hand_landmarks = []
            hand = results.multi_hand_landmarks[hand_idx]

            for lm_id, landmark in enumerate(hand.landmark):
                height, width, channel = orig_image.shape
                pos_x, pos_y = int(landmark.x * width), int(landmark.y * height)
                cur_hand_landmarks.append(LandmarkRecord(lm_id, pos_x, pos_y, label))

            if draw:
                mpDraw.draw_landmarks(orig_image, hand, mpHands.HAND_CONNECTIONS)

            landmark_list.append((label, cur_hand_landmarks))

        return landmark_list
