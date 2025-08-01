from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Determine the path to the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data.json')

# Load the JSON data
def load_data():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Return default data if file not found
        return {
            "default_response": "I'm sorry, the knowledge base is currently unavailable.",
            "questions": []
        }

# Process user query and find the best response
def get_response(user_input, data):
    user_input = user_input.lower().strip()
    
    # Check for direct matches
    for item in data.get('questions', []):
        if user_input in [q.lower() for q in item.get('question', [])]:
            return item.get('answer', '')
    
    # Check for keyword matches
    for item in data.get('questions', []):
        for keyword in item.get('keywords', []):
            if keyword.lower() in user_input:
                return item.get('answer', '')
    
    # Default response if no match found
    return data.get('default_response', "I'm not sure how to answer that.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    data = load_data()
    response = get_response(user_input, data)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)