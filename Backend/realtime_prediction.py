import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from Backend.mp_utils import mediapipe_detection, draw_styled_landmarks, extract_keypoints
from scipy import stats
import time
from collections import Counter

model = load_model('Backend/action.h5')
actions = np.array(['hello', 'thanks', 'iloveyou'])
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

# Shared list for Flask to access
most_common_per_interval = []

def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85 + num * 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return output_frame

def generate_frames():
    sequence = []
    sentence = []
    predictions = []
    threshold = 0.5
    temp_list = []
    time_check = time.time()
    most_frequent_action = ""

    cap = cv2.VideoCapture(0)
    mp_holistic = mp.solutions.holistic

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                continue

            image, results = mediapipe_detection(frame, holistic)
            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                predictions.append(np.argmax(res))

                if len(predictions) >= 10 and np.unique(predictions[-10:])[0] == np.argmax(res):
                    arg = actions[np.argmax(res)]
                    temp_list.append(arg)
                    if res[np.argmax(res)] > threshold:
                        if len(sentence) > 0:
                            if actions[np.argmax(res)] != sentence[-1]:
                                sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5:
                    sentence = sentence[-5:]

                image = prob_viz(res, actions, image, colors)

            cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
            cv2.putText(image, ' '.join(sentence), (3, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if time.time() - time_check >= 3:
                if temp_list:
                    most_common_action = Counter(temp_list).most_common(1)
                    if most_common_action:
                        most_frequent_action = most_common_action[0][0]

                        if not most_common_per_interval or most_frequent_action != most_common_per_interval[-1]:
                            most_common_per_interval.append(most_frequent_action)
                            print(f"List of unique actions: {most_common_per_interval}")

                time_check = time.time()
                temp_list = []

            # 👇 Convert image to JPEG for web stream
            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()
