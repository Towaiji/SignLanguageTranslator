# # realtime_prediction.py
# import cv2
# import numpy as np
# import mediapipe as mp
# from tensorflow.keras.models import load_model
# from mp_utils import mediapipe_detection, draw_styled_landmarks, extract_keypoints
# from scipy import stats
# import os
# import time
# from collections import Counter

# # Load the trained model
# model = load_model('action.h5')
# actions = np.array(['hello', 'thanks', 'iloveyou'])
# temp_list = [] #this will contain data for every 2 second interval in the loop
# all_data = [] #accumulation of temp_lists

# # Define colors for probability visualization
# colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

# def prob_viz(res, actions, input_frame, colors):
#     """Visualize probabilities on the frame."""
#     output_frame = input_frame.copy()
#     for num, prob in enumerate(res):
#         cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
#         cv2.putText(output_frame, actions[num], (0, 85 + num * 40), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
#     return output_frame

# # Variables for prediction smoothing
# sequence = []
# sentence = []
# predictions = []
# threshold = 0.5
# time_check = time.time()

# cap = cv2.VideoCapture(0)
# mp_holistic = mp.solutions.holistic

# with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             continue
#         image, results = mediapipe_detection(frame, holistic)
#         draw_styled_landmarks(image, results)

#         # Append keypoints and maintain a fixed-length sequence
#         keypoints = extract_keypoints(results)
#         sequence.append(keypoints)
#         sequence = sequence[-30:]

#         if len(sequence) == 30:
#             res = model.predict(np.expand_dims(sequence, axis=0))[0]
#             predictions.append(np.argmax(res))

#             # Prediction smoothing logic
#             if len(predictions) >= 10 and np.unique(predictions[-10:])[0] == np.argmax(res):
#                 arg = actions[np.argmax(res)]
#                 temp_list.append(arg)
#                 if res[np.argmax(res)] > threshold:
#                     print(f"Argument is: {arg}")
#                     if len(sentence) > 0:
#                         if actions[np.argmax(res)] != sentence[-1]:
#                             sentence.append(actions[np.argmax(res)])
#                     else:
#                         sentence.append(actions[np.argmax(res)])
#             if len(sentence) > 5:
#                 sentence = sentence[-5:]

#             image = prob_viz(res, actions, image, colors)

#         cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
#         cv2.putText(image, ' '.join(sentence), (3, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
#         # Check every 2 seconds
#         if time.time() - time_check >= 2:
#             # Save the current sentence to temp_list
#             # temp_list.append(arg)

#             # Find the most frequent action in temp_list
#             most_common_action = Counter(temp_list).most_common(1)
#             if most_common_action:
#                 most_frequent_action = most_common_action[0][0]  # The most frequent action

#             print(f"Most frequent action in the last 2 seconds: {most_frequent_action}")

#             # Reset the timer and temp list for the next cycle
#             time_check = time.time()
#             all_data.append(temp_list)
#             temp_list = []

        
#         curr_list = ' '.join(sentence)
#         print(' '.join(sentence))

#         cv2.imshow('OpenCV Feed', image)

#         if cv2.waitKey(10) & 0xFF == ord('q'):
#             break
#     cap.release()
#     cv2.destroyAllWindows()


import cv2
import numpy as np
import mediapipe as mp
from tensorflow.keras.models import load_model
from mp_utils import mediapipe_detection, draw_styled_landmarks, extract_keypoints
from scipy import stats
import os
import time
from collections import Counter

# Load the trained model
model = load_model('action.h5')
actions = np.array(['hello', 'thanks', 'iloveyou'])

# Define colors for probability visualization
colors = [(245, 117, 16), (117, 245, 16), (16, 117, 245)]

def prob_viz(res, actions, input_frame, colors):
    """Visualize probabilities on the frame."""
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0, 60 + num * 40), (int(prob * 100), 90 + num * 40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85 + num * 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return output_frame

# Variables for prediction smoothing
sequence = []
sentence = []
predictions = []
threshold = 0.5
temp_list = []  # Temporary list to store actions every 2 seconds
time_check = time.time()  # To track time for 2 seconds interval
most_frequent_action = ""  # Variable to store the most frequent action
last_print_time = 0  # Time of the last print to prevent printing too often
most_common_per_interval = []  # List of most common words per interval

cap = cv2.VideoCapture(0)
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        image, results = mediapipe_detection(frame, holistic)
        draw_styled_landmarks(image, results)

        # Append keypoints and maintain a fixed-length sequence
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]

        if len(sequence) == 30:
            res = model.predict(np.expand_dims(sequence, axis=0))[0]
            predictions.append(np.argmax(res))

            # Prediction smoothing logic
            if len(predictions) >= 10 and np.unique(predictions[-10:])[0] == np.argmax(res):
                arg = actions[np.argmax(res)]
                temp_list.append(arg)  # Append the predicted action to temp_list
                if res[np.argmax(res)] > threshold:
                    # print(f"Argument is: {arg}")
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

        # Check every 2 seconds
        if time.time() - time_check >= 3:
            # Find the most frequent action in temp_list
            if temp_list:
                most_common_action = Counter(temp_list).most_common(1)


                if most_common_action:
                    most_frequent_action = most_common_action[0][0]  # Get the most frequent action

                    if (not most_common_per_interval):
                        most_common_per_interval.append(most_frequent_action)

                    elif(most_frequent_action != most_common_per_interval[-1]): #append only if last most frequent action stored in the list isnt the same as current most frequent action
                        most_common_per_interval.append(most_frequent_action)


                    if most_common_per_interval:
                        print(f"List of unique actions: {most_common_per_interval}")

            # Reset the timer and temp list for the next cycle
            time_check = time.time()
            
            temp_list = []  # Clear the list for the next 2-second interval

        cv2.imshow('OpenCV Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()