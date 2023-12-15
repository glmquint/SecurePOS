from flask import Flask, request, render_template

app = Flask(__name__)

systems = {"Ingestion_system":None,
           "Preparation_system":None,
           "Segregation_system":None,
           "Development_system":None,
             "Production_system":None,
             "Evaluation_system":None}

class IngestionSystem:
    integer_param = 0
    string_param = ""
    string_param2 = ""
    def build(self):
        return {
            'url': '/system/Ingestion_system/config',
            'elements': [
                {'name': 'integer_param',
                 'type': 'number',
                 'value': self.integer_param},
                {'name': 'string_param',
                 'type': 'text',
                 'value': self.string_param},
                {'name': 'string_param2',
                    'type': 'text',
                    'value': self.string_param2}
            ]}
    def setup(self, data):
        self.integer_param = int(data.form['integer_param'])
        self.string_param = data.form['string_param']
        self.string_param2 = data.form['string_param2']
    def __str__(self):
        return f"Integer param: {self.integer_param} String param: {self.string_param}, {self.string_param2}"

class PreparationSystem:
    prepare_int = 0
    prepare_str = ""
    def build(self):
        return {
            'url': '/system/Preparation_system/config',
            'elements': [
                {'name': 'prepare_int',
                 'type': 'number',
                 'value': self.prepare_int},
                {'name': 'prepare_str',
                 'type': 'text',
                 'value': self.prepare_str}
            ]}
    def setup(self, data):
        self.prepare_int = int(data.form['prepare_int'])
        self.prepare_str = data.form['prepare_str']
    def __str__(self):
        return f"Integer param: {self.prepare_str} String param: {self.prepare_str}"

class SegregationSystem:
    config_file= None
    def build(self):
        return{
            'url': '/system/Segregation_system/config',
            'elements':[
                {
                    'name': 'config_file',
                    'type': 'file',
                    'value': self.config_file.filename if self.config_file is not None else ''
                }
            ]
        }
    def setup(self, data):
        self.config_file = data.files['config_file']
    def __str__(self):
        return f'type: {type(self.config_file)} content: {self.config_file}'


systems['Ingestion_system'] = IngestionSystem()
systems['Preparation_system'] = PreparationSystem()
systems['Segregation_system'] = SegregationSystem()


@app.route('/system/<path:route>', methods=['POST'])
def receive_message(route):
    data = request.get_json()

    if (route not in systems):
        # return a 404 error to the client
        return {'status': 'error', 'message': 'Invalid route'}, 404

    if 'message' in data:
        message = data['message']
        print(f"Received message for route '{route}': {message}")
        return {'status': 'success', 'message': 'Message received'}, 200
    else:
        return {'status': 'error', 'message': 'Invalid request'}, 400

@app.route('/system/<path:route>/config', methods=['GET'])
def get_config(route):
    if (route not in systems):
        # return a 404 error to the client
        return {'status': 'error', 'message': 'Invalid route'}, 404
    return render_template('config_form.html', vars=systems[route].build())

@app.route('/system/<path:route>/config', methods=['POST'])
def set_config(route):
    if (route not in systems):
        # return a 404 error to the client
        return {'status': 'error', 'message': 'Invalid route'}, 404
    systems[route].setup(request)
    print(f"{systems[route]}")
    return {'status': 'success', 'message': 'Config saved'}, 200

messages = []
@app.route('/messages', methods=['POST'])
def message():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        print(f"Received message: {message}")
        messages.append(message)
        return {'status': 'success', 'message': 'Message received'}, 200
    else:
        return {'status': 'error', 'message': 'Invalid request'}, 400

@app.route('/messages', methods=['GET'])
def list_messages():
    return {'status': 'success', 'messages': messages}, 200

@app.route('/messages', methods=['DELETE'])
def delete_messages():
    messages.clear()
    return {'status': 'success', 'messages': messages}, 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
