iimport os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app and enable CORS for all routes
app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Validate OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OpenAI API key is missing. Please set it in the .env file.")

# Initialize NLTK Sentiment Analyzer
try:
    nltk.download('vader_lexicon', quiet=True)
    analyzer = SentimentIntensityAnalyzer()
except Exception as e:
    logger.error(f"Failed to initialize NLTK: {str(e)}")
    raise

@app.route('/')
def home():
    """Root endpoint returning server status."""
    return jsonify({"status": "ok", "message": "Flask server is running. Use the '/chat' endpoint to interact with the chatbot."})

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests."""
    return '', 204

@app.route('/chat', methods=['POST'])
def chat():
    """
    Chatbot endpoint that performs sentiment analysis and generates responses.
    
    Expected JSON payload: {"message": "user message here"}
    Returns: {"response": "chatbot response", "sentiment": "sentiment category"}
    """
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({"error": "Invalid content type. Application/json required."}), 400
        
        # Extract and validate user message
        data = request.json
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"error": "The 'message' field cannot be empty."}), 400

        # Perform sentiment analysis
        sentiment_scores = analyzer.polarity_scores(user_message)
        sentiment = (
            "positive" if sentiment_scores['compound'] > 0.5
            else "negative" if sentiment_scores['compound'] < -0.5
            else "neutral"
        )

        # Generate response using OpenAI
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # Updated to latest stable version
                messages=[
                    {
                        "role": "system",
                        "content": "You are a supportive mental health chatbot. Provide empathetic and helpful responses."
                    },
                    {
                        "role": "user",
                        "content": f"The user has expressed a {sentiment} sentiment: {user_message}"
                    }
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            chatbot_response = response.choices[0].message.content.strip()
            
            return jsonify({
                "response": chatbot_response,
                "sentiment": sentiment,
                "model": "gpt-3.5-turbo-0125"
            })

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            error_message = str(e)
            if "model_not_found" in error_message:
                return jsonify({
                    "error": "Model access error. Please check your OpenAI API access.",
                    "details": error_message
                }), 503
            return jsonify({
                "error": "Failed to generate response from OpenAI.",
                "details": error_message
            }), 503

    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.getenv("PORT", 5000))
    
    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_ENV") == "development"
    )
