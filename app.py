from flask import Flask, request, jsonify
from advanced_medical_chatbot import AdvancedMedicalChatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
chatbot = AdvancedMedicalChatbot()

@app.route('/')
def home():
    return "Welcome to the Medical Chatbot API!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message')
        print(f"Received message: {user_input}")  # Debug print
        bot_response = chatbot.get_response(user_input)
        print(f"Bot response: {bot_response}")  # Debug print
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)