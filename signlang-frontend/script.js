document.addEventListener('DOMContentLoaded', () => {
    const welcomeMsg = document.createElement('div');
    welcomeMsg.textContent = '🤖: Welcome to SignSpeak! Start chatting.';
    welcomeMsg.style.marginBottom = '0.5rem';
    welcomeMsg.style.fontStyle = 'italic';
    const outputText = document.getElementById('output-text');
    const chatLog = document.getElementById('chat-log');
    chatLog.appendChild(welcomeMsg);
    const chatInput = document.getElementById('chat-input');
    const sendBtn = document.getElementById('send-btn');
    const micBtn = document.getElementById('mic-btn');
    const webcam = document.getElementById('webcam');

    const roleSelection = document.getElementById('role-selection');
    const switchRoleBtn = document.getElementById('switch-role-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const chatApp = document.getElementById('chat-app');
    const nurseBtn = document.getElementById('nurse-btn');
    const patientBtn = document.getElementById('patient-btn');
    const roleHeader = document.getElementById('role-header');

    // 👇 NEW: Grab detection toggle elements
    const detectionToggleWrapper = document.getElementById('detection-toggle-wrapper');
    const detectionToggle = document.getElementById('detection-toggle');
    const toggleLabel = document.getElementById('toggle-label');

    let userRole = null;
    let chatHistory = [];
    let wordIndex = 0;
    const simulatedWords = ['hello', 'yes', 'no', 'pain', 'thank you', 'help'];

    nurseBtn.addEventListener('click', () => {
        userRole = 'nurse';
        roleHeader.textContent = '🧑‍⚕️ Nurse Chat';
        chatInput.disabled = false;
        detectionToggleWrapper.style.display = 'none'; // 👈 Hide toggle for nurse
        micBtn.style.display = 'inline-block'; // Show for nurse
        enterChat();
    });
    

    patientBtn.addEventListener('click', () => {
        userRole = 'patient';
        roleHeader.textContent = '🧑‍🦯 Patient Chat';
        chatInput.disabled = false;
        detectionToggleWrapper.style.display = 'flex'; // 👈 Show toggle for patient
        micBtn.style.display = 'none'; // Hide for patient
        enterChat();
    });

    function enterChat() {
        roleSelection.classList.add('hidden');
        chatApp.classList.remove('hidden');

        // Start camera (fake simulation for now)
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    webcam.srcObject = stream;
                })
                .catch(err => {
                    console.error("Camera error:", err);
                });
        }

        // 👇 Toggle label update
        toggleLabel.textContent = detectionToggle.checked ? 'Detection: ON' : 'Detection: OFF';

        detectionToggle.addEventListener('change', () => {
            toggleLabel.textContent = detectionToggle.checked ? 'Detection: ON' : 'Detection: OFF';
        });

        // Detection runs every 5s if toggle is ON AND user is patient
        setInterval(() => {
            if (userRole !== 'patient' || !detectionToggle.checked) return;

            const word = simulatedWords[wordIndex % simulatedWords.length];
            wordIndex++;

            outputText.textContent = word;

            // Add word to input, build sentence
            chatInput.value = (chatInput.value + ' ' + word).trim();
        }, 5000);
    }

    sendBtn.addEventListener('click', () => {
        const msg = chatInput.value.trim();
        if (msg) {
            const sender = userRole === 'nurse' ? '🧑‍⚕️ Nurse' : '🧏 Patient';
            addMessage(`${sender}: ${msg}`);
            chatInput.value = '';
        }
    });

    function addMessage(message) {
        const div = document.createElement('div');
        div.textContent = message;
        div.style.marginBottom = '0.5rem';
        chatLog.appendChild(div);
        chatLog.scrollTop = chatLog.scrollHeight;
    
        // Save to chat history
        chatHistory.push(message);
    }
    
    switchRoleBtn.addEventListener('click', () => {
        if (webcam.srcObject) {
            webcam.srcObject.getTracks().forEach(track => track.stop());
            webcam.srcObject = null;
        }
    
        // Restore chat from history
        chatLog.innerHTML = '';
        chatHistory.forEach(msg => {
            const div = document.createElement('div');
            div.textContent = msg;
            div.style.marginBottom = '0.5rem';
            chatLog.appendChild(div);
        });
    
        chatInput.value = '';
        chatApp.classList.add('hidden');
        roleSelection.classList.remove('hidden');
        outputText.textContent = '...';
    });
    
    
    // 🗣️ Voice-to-text using Web Speech API
    let recognition;
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            micBtn.classList.remove('mic-inactive');
            micBtn.classList.add('mic-active');

            outputText.textContent = 'listening';
            outputText.classList.add('typing-dots');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;

            outputText.classList.remove('typing-dots');
            outputText.textContent = transcript;

            chatInput.value = (chatInput.value + ' ' + transcript).trim();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            outputText.classList.remove('typing-dots');
            outputText.textContent = '...';
            micBtn.classList.remove('mic-active');
            micBtn.classList.add('mic-inactive');
        };

        recognition.onend = () => {
            micBtn.classList.remove('mic-active');
            micBtn.classList.add('mic-inactive');

            outputText.classList.remove('typing-dots');
            outputText.textContent = '...';
        };
    } else {
        alert('Speech Recognition not supported in this browser. Please use Chrome.');
    }

    micBtn.addEventListener('click', () => {
        if (!recognition) return;
        recognition.start();
    });

    clearChatBtn.addEventListener('click', () => {
        chatLog.innerHTML = '';
        chatHistory = []; // if you're using chatHistory to persist
        chatInput.value = '';
    });
    
});
