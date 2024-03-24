import json
import math
import os
import time
from threading import Thread

import pandas as pd
import requests

from src.Development.DevelopmentSystemMasterOrchestrator import DevelopmentSystemMasterOrchestrator
from src.Evaluation.EvaluationSystemOrchestrator import EvaluationSystemOrchestrator
from src.Ingestion.IngestionOrchestrator import PreparationSystemOrchestrator
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus
from src.Production.ProductionSystemOrchestrator import ProductionSystemOrchestrator
from src.Segregation.SegregationSystemOrchestrator import SegregationSystemOrchestrator

''' factory map

ingestion 		- 5005
	/record
	/raw_session
segregation 	- 5001
	/segregationSystem
development		- 5002
	/learning_set
production 		- 5003
	/Classifier
	/PreparedSession
evaluation 		- 5004
	/evaluation_security_label
	/evaluation_label


messaging		- 6000
	/messaging_system
	/performance_sampler
clientside		- 6001
	/client
	
'''

class Service:
    def __init__(self):
        self.message_bus = MessageBus()
        self.load_data()
        self.setup_client_listener()
        self.setup_messaging_listener()

    def setup_messaging_listener(self):
        self.messaging_system = Server()
        self.messaging_system.add_resource(JSONEndpoint, '/messaging_system', recv_callback=self.messaging_system_callback, json_schema_path=f'{os.path.dirname(__file__)}/../DataObjects/Schema/empty.json')
        self.message_bus.addTopic('messaging_system')
        self.messaging_system.add_resource(JSONEndpoint, '/performance_sampler', recv_callback=self.performance_sampler_callback, json_schema_path=f'{os.path.dirname(__file__)}/../DataObjects/Schema/empty.json')
        self.message_bus.addTopic('performance_sampler')

    def messaging_system_callback(self, json_data):
        print(f"Received data from messaging system: {json_data}")
        self.message_bus.pushTopic('messaging_system', json_data)
        return {"status": "ok"}

    def performance_sampler_callback(self, json_data):
        print(f"Received performance data: {json_data}")
        self.message_bus.pushTopic('performance_sampler', json_data)
        return {"status": "ok"}

    def setup_client_listener(self):
        self.server = Server()
        self.server.add_resource(JSONEndpoint, '/client', recv_callback=self.client_callback, json_schema_path=f'{os.path.dirname(__file__)}/../DataObjects/Schema/empty.json')
        self.message_bus.addTopic('client')

    def client_callback(self, json_data):
        print(f"Received data from client: {json_data}")
        self.message_bus.pushTopic('client', json_data)
        return {"status": "ok"}

    def load_data(self):
        csv_files = [f for f in os.listdir('input_samples') if f.endswith('.csv')]
        pandas_dfs = [pd.read_csv(f'{os.path.dirname(__file__)}/input_samples/{f}') for f in csv_files]
        self.df = pd.concat(pandas_dfs)
        #transform columns am1 to am10 to a single array
        self.df['amount'] = self.df[['am1', 'am2', 'am3', 'am4', 'am5', 'am6', 'am7', 'am8', 'am9', 'am10']].values.tolist()
        self.df.drop(columns=[f'am{i}' for i in range(1, 11)], inplace=True)
        # same thing for timestamps
        self.df['timestamp'] = self.df[['ts1', 'ts2', 'ts3', 'ts4', 'ts5', 'ts6', 'ts7', 'ts8', 'ts9', 'ts10']].values.tolist()
        self.df.drop(columns=[f'ts{i}' for i in range(1, 11)], inplace=True)
        # shuffle samples
        # self.df = self.df.sample(frac=1).reset_index(drop=True) # TODO: at the end, actually shuffle instead of sorting
        # sort over UUID
        self.df = self.df.sort_values(by='UUID')

    def start_clientside_server(self):
        # start the server on another thread
        Thread(target=self.server.run, daemon=True, name="self.server.run", kwargs={'port': 6001}).start()
        time.sleep(1)

    def start_messaging_server(self):
        # start the server on another thread
        Thread(target=self.messaging_system.run, daemon=True, name="self.messaging_system.run", kwargs={'port': 6000}).start()
        time.sleep(1)

    def send_data(self):
        i = 0
        for _, row in self.df.iterrows():
            # remove nan values and lists with only nan values
            df_row_cleaned = row.dropna()
            for col in df_row_cleaned.keys():
                if isinstance(df_row_cleaned[col], list) and all(
                        math.isnan(x) for x in df_row_cleaned[col]):
                    del df_row_cleaned[col]
            print(f"Sending row {i} to the ingestion system: {df_row_cleaned.to_dict()}")
            start = time.time()
            #self.ingestion_system.preparation_sys_receiver.receiveRecord(df_row_cleaned.to_dict())
            requests.post("http://127.0.0.1:5005/record", json=df_row_cleaned.to_dict())
            print(f"Sent row in {time.time() - start} seconds")
            i += 1

    def run(self):
        self.start_clientside_server()
        self.start_messaging_server()
        self.start_factory()
        self.send_data()

    def start_factory(self):
        self.start_ingestion_system()
        self.start_segregation_system()
        self.start_development_system()
        self.start_production_system()
        self.start_evaluation_system()

    def start_ingestion_system(self):
        print("starting ingestion system...")
        self.ingestion_system = PreparationSystemOrchestrator()
        self.ingestion_system.storage_controller.remove_all() # reset db
        Thread(target=self.ingestion_system.run, name="self.ingestion_system.run", daemon=True).start()
        time.sleep(1) # wait for the server to start
        time.sleep(1)

    def start_segregation_system(self):
        print("starting segregation system...")
        self.segregation_system = SegregationSystemOrchestrator()
        self.segregation_system.storage_controller.remove_all() # reset db
        Thread(target=self.segregation_system.run, name="self.segregation_system.run", daemon=True).start()
        time.sleep(1) # wait for the server to start
        time.sleep(1)

    def start_development_system(self):
        print("starting development system...")
        # delete all files inside the classifiers folder
        for f in os.listdir(f"{os.path.dirname(__file__)}/../Development/classifiers"):
            os.remove(f"{os.path.dirname(__file__)}/../Development/classifiers/{f}")
        self.development_system = DevelopmentSystemMasterOrchestrator()
        Thread(target=self.development_system.start, name="self.development_system.start", daemon=True).start()
        time.sleep(1) # wait for the server to start
        time.sleep(1)

    def start_production_system(self):
        print("starting production system...")
        with open(f"{os.path.dirname(__file__)}/../Ingestion/config/PreparationSystemConfig.json", 'r') as f:
            config = json.load(f)
        if config['phase_tracker']['phase'] == 'Development':
            try:
                os.remove(f"{os.path.dirname(__file__)}/../Production/classifier.sav")
            except FileNotFoundError:
                pass
        elif config['phase_tracker']['phase'] == 'Production':
            assert os.path.isfile(f"{os.path.dirname(__file__)}/../Production/classifier.sav")
        else:
            raise Exception("Invalid phase")
        self.production_system = ProductionSystemOrchestrator()
        Thread(target=self.production_system.run, name="self.production_system.run", daemon=True).start()
        time.sleep(1) # wait for the server to start
        time.sleep(1)

    def start_evaluation_system(self):
        print("starting evaluation system...")
        self.evaluation_system = EvaluationSystemOrchestrator()
        Thread(target=self.evaluation_system.main, name="self.evaluation_system.main", daemon=True).start()
        time.sleep(1) # wait for the server to start
        time.sleep(1)


if __name__ == '__main__':
    with open(f"{os.path.dirname(__file__)}/../Ingestion/config/PreparationSystemConfig.json", 'r') as f:
        config = json.load(f)
    config['phase_tracker']['phase'] = 'Development'
    with open(f"{os.path.dirname(__file__)}/../Ingestion/config/PreparationSystemConfig.json", 'w') as f:
        json.dump(config, f, indent=4)
    service = Service()
    service.run()
    print("Done with development, now switching to production...")
    time.sleep(2)
    with open(f"{os.path.dirname(__file__)}/../Ingestion/config/PreparationSystemConfig.json", 'r') as f:
        config = json.load(f)
    config['phase_tracker']['phase'] = 'Production'
    with open(f"{os.path.dirname(__file__)}/../Ingestion/config/PreparationSystemConfig.json", 'w') as f:
        json.dump(config, f, indent=4)
    service.run()
