import json
from src.JsonIO.JsonValidator import JSONValidator


class EvaluationSystemConfig:

    def __init__(self):
        self.sufficient_label_number = 5
        self.simulate_human_task = False

    def load(self):
        validator = JSONValidator("../DataObjects/Schema/config.json")
        f = open('../config/config.json')
        data = json.load(f)
        validator.validate_data(data)

        print(data["sufficient_label_number"])
        print(data["simulate_human_task"])
        self.sufficient_label_number = data["sufficient_label_number"]
        self.simulate_human_task = data["simulate_human_task"]
        f.close()
        return


#conf = EvaluationSystemConfig()
#conf.load();
