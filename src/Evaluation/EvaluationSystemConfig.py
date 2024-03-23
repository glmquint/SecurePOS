import json
import os

from src.JsonIO.JsonValidator import JSONValidator



class EvaluationSystemConfig:

    def __init__(self):
        self.sufficient_label_number = 0
        self.simulate_human_task = False
        self.state = 0
        self.path_config_validator = f"{os.path.dirname(__file__)}/config/validator.json"
        self.path_config = f"{os.path.dirname(__file__)}/config/config.json"
        self.tollerated_error = 0
        self.tollerated_consecutive_error = 0
        self.port = 0
        self.load()

    def write_state(self,state=0):
        with open(self.path_config, "r") as jsonFile:
            data = json.load(jsonFile)

        data["state"] = state

        with open(self.path_config, "w") as jsonFile:
            json.dump(data, jsonFile)

        self.state = state


    def load(self):
        validator = JSONValidator(self.path_config_validator)
        f = open(self.path_config)
        data = json.load(f)
        f.close()
        validator.validate_data(data)

        self.sufficient_label_number = data["sufficient_label_number"]
        self.state = data["state"]
        self.tollerated_error = data["tollerated_error"]
        self.tollerated_consecutive_error = data["tollerated_consecutive_error"]
        self.port = data["port"]
        if data["simulate_human_task"] == "True":
            self.simulate_human_task = True
        else:
            self.simulate_human_task = False
        f.close()
        return


#conf = EvaluationSystemConfig()
#conf.load()
#conf.write_state(0)
#conf.load()
#print(conf.tollerated_error)