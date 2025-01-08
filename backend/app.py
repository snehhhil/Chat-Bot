import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app and enable CORS for all routes
app = Flask(__name__)
CORS(app)

# Load OpenAI API Key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded correctly
if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Please set it in the .env file.")

# Initialize NLTK Sentiment Analyzer
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# Root Route (Prevents 404 errors on direct root access)
@app.route('/')
def home():
    return "Flask server is running. Use the '/chat' endpoint to interact with the chatbot."

# Ignore favicon.ico errors
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Chatbot Route for Sentiment Analysis and OpenAI Interaction
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        # Sentiment Analysis
        sentiment_score = analyzer.polarity_scores(user_message)
        sentiment = "neutral"
        if sentiment_score['compound'] > 0.5:
            sentiment = "positive"
        elif sentiment_score['compound'] < -0.5:
            sentiment = "negative"

        # Generate Response using OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a supportive mental health chatbot. Respond to a {sentiment} message: {user_message}",
            max_tokens=150
        )
        
        chatbot_response = response.choices[0].text.strip()
        return jsonify({"response": chatbot_response, "sentiment": sentiment})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask App
if __name__ == "__main__":
    app.run(debug=True)