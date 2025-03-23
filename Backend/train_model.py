# train_model.py
import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# --- Parameters and data paths ---
DATA_PATH = os.path.join('MP_Data')
actions = np.array(['hello', 'thanks', 'iloveyou'])
no_sequences = 30
sequence_length = 30

# Map actions to labels
label_map = {label: num for num, label in enumerate(actions)}

# --- Data Preprocessing ---
sequences, labels = [], []
for action in actions:
    action_path = os.path.join(DATA_PATH, action)
    # Ensure the folders are processed in numerical order
    for sequence in sorted(os.listdir(action_path), key=lambda x: int(x)):
        window = []
        sequence_folder = os.path.join(action_path, sequence)
        for frame_num in range(sequence_length):
            file_path = os.path.join(sequence_folder, f"{frame_num}.npy")
            res = np.load(file_path)
            window.append(res)
        sequences.append(window)
        labels.append(label_map[action])

X = np.array(sequences)
y = to_categorical(labels).astype(int)

# Split the data (using a small test size)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)

print("X shape:", X.shape)
print("y shape:", y.shape)

# --- Build and Train the LSTM Model ---
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import TensorBoard

log_dir = os.path.join('Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(sequence_length, X.shape[2])))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
model.fit(X_train, y_train, epochs=2000, callbacks=[tb_callback])
model.summary()

# --- Save the trained model ---
model.save('action.h5')
