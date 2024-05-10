from rag_cot import configure_rag, process_query_with_chain_of_thought
from flask import Flask, request, jsonify


app = Flask(__name__)

# Default endpoint to avoid 404 errors when accessing '/'
@app.route('/')
def home():
    return "Welcome to the chatbot API. Use '/chatbot/query' to interact with the chatbot."

# Favicon handler to avoid 404 errors when accessing '/favicon.ico'
@app.route('/favicon.ico')
def favicon():
    # Return an empty response or a default favicon image
    return '', 204  # 204 indicates a successful response with no content

# Endpoint for chatbot query processing
@app.route('/chatbot/query', methods=['POST'])
def process_chatbot_query():
    data = request.json
    user_query = data.get('query')
    context = data.get('context', '')

    # Configure RAG and Chain of Thought
    tokenizer, _, model = configure_rag("facebook/rag-sequence-nq")

    # Process the query with CoT
    response = process_query_with_chain_of_thought(model, tokenizer, user_query, context)

    # Return the chatbot response
    return jsonify({"response": response})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
