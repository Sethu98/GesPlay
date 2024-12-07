import mediapipe as mp
from mediapipe.tasks import python

from gesplay.gesture_handler import GestureHandler
from gesplay.util import Utils

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class GestureDecoder:
    MODEL_PATH = '../gesture_recognizer.task'

    def __init__(self, gesture_handler: GestureHandler):
        options = GestureRecognizerOptions(
            base_options=BaseOptions(model_asset_path=self.MODEL_PATH),
            running_mode=VisionRunningMode.LIVE_STREAM,
            # running_mode=VisionRunningMode.IMAGE,
            result_callback=self.process_recognition_result
        )
        self.recognizer = GestureRecognizer.create_from_options(options)
        self.gesture_handler = gesture_handler

    def process_recognition_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        # print(f'gesture recognition result: {result}')
        gesture_categories = []

        for gest in result.gestures:
            gesture_categories.extend([g.category_name for g in gest])

        if gesture_categories:
            self.gesture_handler.handle_gestures(gesture_categories)
            # print(f"gestures = {gesture_categories}")

    def decode_gestures(self, img):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        self.recognizer.recognize_async(mp_image, Utils.get_unix_timestamp_ms())
        # result = self.recognizer.recognize(mp_image)
        # self.process_recognition_result(result, None, None)

        return []
