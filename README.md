🧠 Mental Health AI Chatbot
A supportive mental health chatbot powered by Vite, Flask, and OpenAI. It offers sentiment analysis and mood tracking to help users monitor their emotional health.


📦 Project Structure:
/mental_health_chatbot
├── backend
│   ├── app.py                  # Flask backend with sentiment analysis
│   └── requirements.txt        # Python dependencies
├── frontend
│   ├── public
│   ├── src
│   │   ├── components
│   │   │   └── Chatbot.jsx     # Chatbot UI Component
│   │   └── App.jsx             # Main React Component
│   └── vite.config.js          # Vite Configuration
│   └── package.json            # Frontend dependencies
└── README.md                   # Project Documentation


✨ Features:
	•	💬 AI-Powered Chatbot: Uses OpenAI API for empathetic responses.
	•	📊 Sentiment Analysis: Detects user sentiment (positive, neutral, negative).
	•	📈 Mood Tracking: Tracks mood history over multiple conversations.
	•	⚡ Vite Frontend: Fast and optimized frontend development using Vite.
	•	🛠️ Flask Backend: Python Flask for API handling and sentiment analysis.


🛠️ Tech Stack:
	•	Frontend: Vite, React, Axios
	•	Backend: Flask, OpenAI, NLTK
	•	Sentiment Analysis: NLTK Sentiment Intensity Analyzer (VADER)
	•	Language Model: OpenAI text-davinci-003
