from flask import Flask, request, jsonify
import json  # Import the json module
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    data_str = json.dumps(data)  # Convert the list to a JSON string
    print("Data received from the pi: " + data_str)
    return jsonify({'message': 'Data received successfully', 'receivedData': data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
