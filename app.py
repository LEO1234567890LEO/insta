from flask import Flask, request, jsonify

app = Flask(__name__)

# Predefined valid API keys (in a real-world scenario, store these securely)
VALID_API_KEYS = {"12345-ABCDE-67890-FGHIJ", "09876-ZYXWV-54321-QWERT"}

@app.route('/authenticate', methods=['POST'])
def authenticate():
    # Get the API key from the request
    api_key = request.json.get('api_key')

    # Check if the API key is valid
    if api_key in VALID_API_KEYS:
        return jsonify({"status": "success", "message": "API key is valid"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid API key"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
