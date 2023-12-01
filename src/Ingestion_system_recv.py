from flask import Flask, request

app = Flask(__name__)


@app.route('/system/<path:route>', methods=['POST'])
def receive_message(route):
    data = request.get_json()

    if 'message' in data:
        message = data['message']
        print(f"Received message for route '{route}': {message}")
        return {'status': 'success', 'message': 'Message received'}
    else:
        return {'status': 'error', 'message': 'Invalid request'}


if __name__ == '__main__':
    app.run(host='192.168.143.248', port=5000, debug=True)
