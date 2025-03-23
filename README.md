# SignSpeak: A Sign Language Messenger  

## 🏆 Inspiration  
The inspiration for this project came from the need for better communication between nurses and patients who use sign language. Hospitals can be stressful places, and effective communication is crucial, especially in emergency situations. Many patients struggle to express their needs due to language barriers, and we wanted to create a system that helps bridge that gap.  

## 🔍 What We Learned  
Through this project, we gained valuable insights into:  
- **Real-time hand gesture recognition** using machine learning.  
- **Building a web application** that integrates AI-driven sign detection.  
- **Flask and OpenCV integration** for live video processing.  
- **Frontend development** to ensure a smooth user experience.  
- **Handling Web Speech API** to enable voice-to-text for non-signing users.  

## 🛠️ How We Built It  
The project consists of three major components:  

### 1️⃣ **Machine Learning & Gesture Recognition**  
- **Python (Flask, OpenCV, TensorFlow)** was used to build a real-time hand gesture recognition system.  
- The **train_model.py** script trains a model to recognize different hand signs.  
- The **realtime_prediction.py** script processes live video input and predicts sign language gestures in real time.  

### 2️⃣ **Backend API & Data Processing**  
- **Flask server** is responsible for serving real-time predictions and handling requests from the frontend.  
- The **data_collection.py** script was used to gather training data.  
- The **mp_utils.py** file contains helper functions for image preprocessing and model inference.  

### 3️⃣ **Frontend Interface**  
- The web application is built using **HTML, CSS, and JavaScript**.  
- The **index.html** file provides the UI structure.  
- The **script.js** file manages user interactions, role selection (nurse/patient), and integrates with the Flask API for sign recognition.  
- **CSS animations** and UI styling enhance accessibility and usability.  

## 🚧 Challenges We Faced  
- **Real-time processing delays**: Handling video input and making predictions fast enough for a seamless conversation was a challenge. We optimized the model and reduced computational overhead to improve response time.  
- **Integrating speech recognition**: The Web Speech API was tricky to implement consistently across browsers, but we managed to ensure smooth voice input.  
- **UI/UX Design**: Making an accessible and intuitive interface required iterative improvements based on feedback.  

## 🎯 Conclusion  
This project was a rewarding experience that highlighted the importance of **AI for accessibility**. We hope that **SignSpeak** can make a difference in real-world healthcare settings, improving communication and inclusivity for patients with hearing impairments.  

🚀 *Made with 💙 for inclusive care!*
