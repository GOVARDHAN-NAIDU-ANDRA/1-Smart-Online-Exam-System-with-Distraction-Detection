# backend/focus_detector.py

import cv2
import mediapipe as mp

class FocusDetector:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=5,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect_focus(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)

        face_count = 0
        is_focused = False

        if result.multi_face_landmarks:
            face_count = len(result.multi_face_landmarks)

            if face_count == 1:
                landmarks = result.multi_face_landmarks[0].landmark
                left_eye = landmarks[33]
                right_eye = landmarks[263]
                nose_tip = landmarks[1]

                # Heuristic: eyes aligned horizontally & nose centered (x ~ 0.5)
                eye_diff_y = abs(left_eye.y - right_eye.y)
                nose_centered = abs(nose_tip.x - 0.5)

                if eye_diff_y < 0.03 and nose_centered < 0.1:
                    is_focused = True

        return face_count, is_focused
