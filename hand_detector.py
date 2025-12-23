"""Hand detector with compatibility for both legacy `mp.solutions` and the
`mediapipe.tasks` HandLandmarker. Provides a mock fallback when MediaPipe
is unavailable.
"""

import os
import time
import cv2

# Import mediapipe safely so importing this module doesn't fail when it's missing
try:
    import mediapipe as mp
except Exception:
    mp = None


class HandDetector:
    def __init__(self, mode=False, max_hands=1, detection_con=0.7, track_con=0.5, model_path=None):
        """Create a HandDetector.

        If `mediapipe` provides the legacy `solutions` API we use that. Otherwise
        we try to use `mediapipe.tasks` with a `hand_landmarker.task` model. If
        neither is available, the detector will run in a mock (no-op) mode.
        """
        self.mode = None
        self.results = None

        # Try legacy mp.solutions API (keeps previous behavior)
        try:
            if mp is not None and hasattr(mp, 'solutions') and hasattr(mp.solutions, 'hands'):
                self.mp_hands = mp.solutions.hands
                self.hands = self.mp_hands.Hands(
                    static_image_mode=mode,
                    max_num_hands=max_hands,
                    min_detection_confidence=detection_con,
                    min_tracking_confidence=track_con
                )
                self.mp_draw = mp.solutions.drawing_utils
                self.mode = 'solutions'
                return
        except Exception:
            pass

        # Try the new Tasks API if available
        try:
            if mp is not None:
                from mediapipe.tasks.python import vision
                self.tasks_vision = vision

                if model_path is None:
                    candidates = [
                        'hand_landmarker.task',
                        os.path.join('models', 'hand_landmarker.task')
                    ]
                    model_path = next((p for p in candidates if os.path.exists(p)), None)

                    if model_path is None:
                        # attempt automatic download
                        try:
                            from download_model import download_hand_landmarker
                            model_path = download_hand_landmarker(dest_path=os.path.join('models', 'hand_landmarker.task'))
                            print(f"Downloaded hand_landmarker model to {model_path}")
                        except Exception:
                            model_path = None

                if model_path is None:
                    raise ImportError("HandLandmarker model not found")

                options = vision.HandLandmarkerOptions(
                    base_options=vision.BaseOptions(model_asset_path=model_path),
                    running_mode=vision.RunningMode.VIDEO,
                    num_hands=max_hands
                )
                self.landmarker = vision.HandLandmarker.create_from_options(options)
                self.mode = 'tasks'
                return
        except Exception:
            pass

        # Fallback to mock mode
        self.mode = 'mock'
        print('Warning: No usable MediaPipe detector found; HandDetector running in mock mode.')

    def find_hands(self, img, draw=True):
        if self.mode == 'solutions':
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(img_rgb)

            if getattr(self.results, 'multi_hand_landmarks', None):
                for hand_lms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mp_draw.draw_landmarks(img, hand_lms, self.mp_hands.HAND_CONNECTIONS)
            return img

        if self.mode == 'tasks':
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image = self.tasks_vision.Image.create_from_array(img_rgb)
            ts = int(time.time() * 1000)
            try:
                self.results = self.landmarker.detect_for_video(image, timestamp_ms=ts)
            except Exception:
                self.results = self.landmarker.detect(image)

            # draw simple landmarks
            if draw and getattr(self.results, 'hand_landmarks', None):
                for hand_landmarks in self.results.hand_landmarks:
                    for lm in hand_landmarks.landmarks:
                        h, w, _ = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(img, (cx, cy), 3, (0, 255, 0), -1)
            return img

        # mock
        self.results = None
        return img

    def find_positions(self, img):
        lm_list = []
        if self.mode == 'solutions':
            if getattr(self, 'results', None) and getattr(self.results, 'multi_hand_landmarks', None):
                my_hand = self.results.multi_hand_landmarks[0]
                for id, lm in enumerate(my_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy, getattr(lm, 'z', 0)])
            return lm_list

        if self.mode == 'tasks':
            if getattr(self.results, 'hand_landmarks', None):
                hand = self.results.hand_landmarks[0]
                for id, lm in enumerate(hand.landmarks):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([id, cx, cy, getattr(lm, 'z', 0)])
            return lm_list

        # mock mode: empty list
        return lm_list