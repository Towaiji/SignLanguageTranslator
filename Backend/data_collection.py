# data_collection.py
import cv2
import numpy as np
import os
import mediapipe as mp
from mp_utils import mediapipe_detection, draw_styled_landmarks, extract_keypoints

# --- Setup paths and parameters ---
DATA_PATH = os.path.join('MP_Data')
actions = np.array(['hello', 'thanks', 'iloveyou'])
no_sequences = 30      # Number of videos per action
sequence_length = 30   # Frames per video
start_folder = 30      # Starting folder index

# Create folders for each action and sequence
for action in actions:
    action_path = os.path.join(DATA_PATH, action)
    if not os.path.exists(action_path):
        os.makedirs(action_path)
    existing = os.listdir(action_path)
    dirmax = np.max(np.array(existing).astype(int)) if existing else 0
    for sequence in range(1, no_sequences + 1):
        folder_path = os.path.join(action_path, str(dirmax + sequence))
        os.makedirs(folder_path, exist_ok=True)

# --- Data collection loop ---
cap = cv2.VideoCapture(0)
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    # Loop through each action
    for action in actions:
        # Loop through sequences (videos)
        for sequence in range(start_folder, start_folder + no_sequences):
            # Loop through frames in the sequence
            for frame_num in range(sequence_length):
                ret, frame = cap.read()
                if not ret:
                    continue
                image, results = mediapipe_detection(frame, holistic)
                draw_styled_landmarks(image, results)

                if frame_num == 0:
                    cv2.putText(image, 'STARTING COLLECTION', (120, 200),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4, cv2.LINE_AA)
                    cv2.putText(image, f'Collecting frames for {action} Video Number {sequence}', (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)
                    cv2.waitKey(500)
                else:
                    cv2.putText(image, f'Collecting frames for {action} Video Number {sequence}', (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.imshow('OpenCV Feed', image)

                # Export keypoints
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(DATA_PATH, action, str(sequence), str(frame_num))
                np.save(npy_path, keypoints)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
    cap.release()
    cv2.destroyAllWindows()
