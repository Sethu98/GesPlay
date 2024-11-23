import enum


class Gestures(enum.Enum):
    LEFT = 0
    RIGHT = 1


class GestureDecoder:
    def decode_gesture(self, hand_landmarks, img):
        # Get index finger base and tip coordinates
        h, w, _ = img.shape
        base = hand_landmarks.landmark[5]  # Index finger MCP joint
        tip = hand_landmarks.landmark[8]  # Index finger tip

        # Convert to pixel coordinates
        base_x = int(base.x * w)
        tip_x = int(tip.x * w)

        # Calculate horizontal difference
        diff_x = tip_x - base_x

        # Define threshold for direction detection
        threshold = 30  # Adjust this value based on your needs

        if diff_x > threshold:
            return Gestures.LEFT
        elif diff_x < -threshold:
            return Gestures.RIGHT

        return None
