import sys
import os
import requests
from flask import Flask, render_template, request, jsonify
from src.bot_interface import BotInterface

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)
bot = BotInterface()

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def get_llm_response(prompt):
    """Get response from TinyLlama model"""
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json().get('response', '')
        return "Sorry, I couldn't process that request."
    except Exception as e:
        print(f"Error calling Ollama API: {str(e)}")
        return "Sorry, there was an error processing your request."

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', query='', response='')

@app.route('/api/query', methods=['POST'])
def api_query():
    query = request.form['query']
    
    # Check if the query is weather-related
    if any(state.lower() in query.lower() for state in bot.indian_states):
        # Use existing weather functionality
        result = bot.process_query(query)
        lines = result.split("\n")
        weather = ""
        if lines and lines[0].startswith("Weather:"):
            weather = lines[0].replace("Weather:", "").strip()
        return jsonify(response=result, weather=weather)
    else:
        # Use TinyLlama for general queries
        result = get_llm_response(query)
        return jsonify(response=result)

# Optional: Add a dedicated endpoint for LLM-only queries
@app.route('/api/llm', methods=['POST'])
def llm_query():
    query = request.form['query']
    result = get_llm_response(query)
    return jsonify(response=result)

# Optional: Add streaming endpoint for LLM responses
@app.route('/api/llm/stream', methods=['POST'])
def llm_stream():
    query = request.form['query']
    
    def generate():
        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": "tinyllama",
                    "prompt": query,
                    "stream": True
                },
                stream=True
            )
            
            for line in response.iter_lines():
                if line:
                    yield f"data: {line.decode('utf-8')}\n\n"
        except Exception as e:
            yield f"data: {{'error': '{str(e)}'}}\n\n"
    
    return app.response_class(
        generate(),
        mimetype='text/event-stream'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
