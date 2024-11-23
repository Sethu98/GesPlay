import cv2
import mediapipe as mp
import time

from gesture_decoder import GestureDecoder


class GestureHandler:
    def __init__(self, key_map):
        self.key_map = key_map

    def handle_gesture(self, gesture):
        print(f"Key event triggered: {gesture}")  # Replace with your desired action


class GesPlay:
    def __init__(self):
        self.gesture_decoder = GestureDecoder()
        self.gesture_handler = GestureHandler(None)

    def start(self):
        cap = cv2.VideoCapture(0)

        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                              max_num_hands=2,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils

        pTime = 0
        cTime = 0

        # Add state to prevent continuous triggering
        last_gesture = None
        gesture_cooldown = 0
        COOLDOWN_FRAMES = 10  # Adjust this value to control how often the event can trigger

        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            # print(results.multi_hand_landmarks)

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        # print(id,lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # if id ==0:
                        cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                    # Check finger direction
                    if gesture_cooldown == 0:
                        gesture = self.gesture_decoder.decode_gesture(handLms, img)
                        if gesture and gesture != last_gesture:
                            self.gesture_handler.handle_gesture(gesture)
                            last_gesture = gesture
                            gesture_cooldown = COOLDOWN_FRAMES
                else:
                    last_gesture = None

            if gesture_cooldown > 0:
                gesture_cooldown -= 1

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

            cv2.imshow("Image", img)
            cv2.waitKey(1)


GesPlay().start()
