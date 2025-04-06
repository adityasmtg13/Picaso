from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend access

# Configure Gemini
genai.configure(api_key="AIzaSyBwWG5ueiTzGSXkd_9u8SO1Wk0CYVzIZRw")
model = genai.GenerativeModel('gemini-2.0-flash')

def clean_response(text):
    """Remove markdown symbols from the response"""
    return text.replace('**', '').replace('```', '').replace("'''", "").strip()

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip()
    
    # Handle empty input
    if not user_input:
        return jsonify({'response': "Please enter a message."})
    
    # Handle questions about capabilities
    if any(phrase in user_input.lower() for phrase in ["what can you do", "what do you do", "your capabilities", "help me with"]):
        return jsonify({
            'response': "I'm a friendly assistant that can help with general knowledge, learning topics, coding questions, education subjects, and even some life situations. What would you like help with?"
        })
    
    # Handle identity questions
    if any(phrase in user_input.lower() for phrase in ["your name", "who are you", "what's your name"]):
        return jsonify({
            'response': "I'm PICASO, your helpful AI assistant! How can I assist you today?"
        })
    
    # Get response from Gemini
    if user_input:
        try:
            response = model.generate_content(user_input)
            cleaned_response = clean_response(response.text)
            return jsonify({'response': cleaned_response})
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'response': "Sorry, I'm having trouble responding right now. Please try again."})

if __name__ == '__main__':
    app.run(host='localhost', port=3000, debug=True)