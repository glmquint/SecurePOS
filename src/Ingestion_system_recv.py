from flask import Flask, request

app = Flask(__name__)

@app.route('/Ingestion_system', methods=['POST'])
def receive_message_ingestion():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

@app.route('/Preparation_system', methods=['POST'])
def receive_message_preparation():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

@app.route('/Segregation_system', methods=['POST'])
def receive_message_segregation():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

@app.route('/Development_system', methods=['POST'])
def receive_message_development():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

@app.route('/Production_system', methods=['POST'])
def receive_message_production():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

@app.route('/Evaluation_system', methods=['POST'])
def receive_message_evaluation():
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}
        print("Error")

if __name__ == '__main__':
    app.run(debug=True)
