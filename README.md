# 🖐️ Sign Speak

## 📌 Overview  
**Sign Speak** is a real-time tool that translates sign language gestures into text using **computer vision**, **MediaPipe**, and **machine learning**. It helps bridge communication gaps for individuals with hearing impairments.  

## 🎯 Features  
- ✅ **Real-time Sign Language Detection** using a webcam  
- ✅ **Hand Gesture Tracking** with MediaPipe  
- ✅ **Machine Learning-based Gesture Classification**  
- ✅ **User-friendly Chat Interface** for communication  
- ✅ **Speech-to-Text Integration** (for nurses/assistants)  
- ✅ **Role-based UI** (Patient & Nurse modes)  

## 🏗️ Project Structure  

```plaintext
📂 SignLanguageTranslator/
│── 📜 README.md                # Documentation  
│── 📂 models/                  # Trained ML models  
│── 📂 data/                    # Gesture datasets  
│── 📜 data_collection.py       # Captures gesture data  
│── 📜 train_model.py           # Trains the ML model  
│── 📜 realtime_prediction.py   # Real-time recognition  
│── 📜 mp_utils.py              # MediaPipe utilities  
│── 📜 main.py                  # Main execution file  
│── 📂 static/                  # CSS & JavaScript files  
│── 📂 templates/               # Web HTML templates  
│── 📜 requirements.txt         # Dependencies  

⚙️ Installation & Setup

1️⃣ Clone the Repository

git clone https://github.com/your-username/SignLanguageTranslator.git
cd SignLanguageTranslator

2️⃣ Install Dependencies

Ensure Python 3.8+ is installed, then run:

pip install -r requirements.txt

3️⃣ Run the Application

python main.py

🚀 Usage

1️⃣ Select a Role: Choose between Nurse (Text/Voice) or Patient (Sign Language).
2️⃣ For Patients: Activate Gesture Detection to recognize signs.
3️⃣ For Nurses: Use text input or voice-to-text for communication.
4️⃣ Chat Window: Messages appear in real-time for seamless interaction.

🛠️ Technical Stack
	•	Python (Core programming)
	•	OpenCV (Video processing)
	•	MediaPipe (Hand gesture tracking)
	•	TensorFlow/Keras (Model training)
	•	Flask (Web-based interface)
	•	JavaScript (Web Speech API) (Voice-to-text support)

📊 Model Training

# Collect gesture data
python data_collection.py  

# Train the model
python train_model.py  

# Run real-time gesture detection
python realtime_prediction.py  


🤝 Contributing
	1.	Fork the repository
	2.	Create a new branch: git checkout -b feature-name
	3.	Commit changes: git commit -m "Added feature"
	4.	Push to branch: git push origin feature-name
	5.	Open a Pull Request

📜 License

This project is licensed under the MIT License.

