import json


class DevSystemStatus:
    status: str
    should_validate: bool
    path: str

    def __init__(self, path: str = "status.json"):
        self.path = path

    def load_status(self):
        self.status = "receive_learning_set"
        self.should_validate = False
        with open(self.path, 'r') as json_file:
            data = json.load(json_file)
            self.status = data['status']
            self.should_validate = data['should_validate']

    def save_status(self, status: str, should_validate: bool):
        self.status = status
        self.should_validate = should_validate
        with open(self.path, 'w') as json_file:
            json.dump(self.__dict__, json_file)

# dev_status = DevSystemStatus()
# print(dev_status.__dict__)
# dev_status.save_status("2", True)
# dev_status2 = DevSystemStatus()
# dev_status2.load_status()
# print(dev_status2.__dict__)