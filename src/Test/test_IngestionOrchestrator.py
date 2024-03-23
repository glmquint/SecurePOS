from random import random, randint, choice
from threading import Thread
from time import sleep
from uuid import uuid1

import requests

from src.DataObjects.Record import Label, Record, TransactionCloudRecord, NetworkMonitorRecord, LocalizationSysRecord
from src.DataObjects.RecordOld import RecordOld
from src.DataObjects.Session import PreparedSession, RawSession
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.IngestionOrchestrator import PreparationSystemOrchestrator
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus

DATAOBJ_PATH = "../DataObjects/Schema"

TEST_PORT = 4000
SELF_PORT = 5002

message_bus = MessageBus([])
test_everything = True

server = None
local_test = False

def listener_setup(prepared_session_creator, message_bus=None):
    global server
    server = Server()
    for endpoint, val in prepared_session_creator.items():
        url = val['url'].split('/')[-1]
        print(f"adding {url}")
        if message_bus:
            message_bus.addTopic(url)
        def builder(url):
            def callback(json_data):
                print(f"hello from {url} received {json_data}")
                if message_bus:
                    message_bus.pushTopic(url, json_data)
            return callback
        schema = {'segregationSystem':'PreparedSessionSchema', 'PreparedSession':'PreparedSessionSchema', 'label': 'RecordSchema'}.get(url, None)
        server.add_resource(JSONEndpoint, f"/{url}", recv_callback=builder(url), json_schema_path=f"../DataObjects/Schema/{schema}.json")
    Thread(target=server.run, daemon=True, kwargs={'debug':True, 'port':TEST_PORT}).start()

class TestPreparationSystemOrchestrator:
    def test_components(self):
        global message_bus
        config = PreparationSystemConfig(f"{DATAOBJ_PATH}/PreparationSystemConfigSchema.json")
        config.init_from_file("PreparationSystemConfig.json")
        c: dict = config.prepared_session_creator
        c.update({'label_receiver': config.raw_session_creator['label_receiver']})
        listener_setup(c, message_bus)
        for endpoint, val in c.items():
            url = val['url'].split('/')[-1]
            print(f"Sending to {url}")
            objtype = {'segregation_system': PreparedSession, 'PreparedSession': PreparedSession,
                       'label': Label}.get(url, None)
            objsent = objtype().to_json()
            r = requests.post(f"http://127.0.0.1:{TEST_PORT}/{url}", json=objsent)
            assert r.status_code == 200, f"got {r.status_code} while sending to {url}"
            assert message_bus.popTopic(url) == objsent, "raw_session not received"

        # ok, now let's start our system orchestrator
        orchestrator = PreparationSystemOrchestrator(config)
        Thread(target=orchestrator.run, daemon=True).start()

        # before testing it, we check the internal receiver
        for endpoint, url in config.raw_session_creator[
            'raw_session_receiver'].items():  # should be only raw session receiver
            url = url.split('/')[-1]
            rs = RawSession()
            r = requests.post(f"http://127.0.0.1:{SELF_PORT}/{url}", json=rs.to_json())
            assert r.status_code == 200, f"got {r.status_code} while sending to {url}"

    def test_run(self):
        global message_bus
        config = PreparationSystemConfig(f"{DATAOBJ_PATH}/PreparationSystemConfigSchema.json")
        config.init_from_file("PreparationSystemConfig.json")
        c:dict = config.prepared_session_creator
        c.update({'label_receiver': config.raw_session_creator['label_receiver']})
        listener_setup(c, message_bus)

        # ok, now let's start our system orchestrator
        orchestrator = PreparationSystemOrchestrator(config)
        print(f"storage controller count = {orchestrator.storage_controller.count()}")
        orchestrator.storage_controller.remove_all()
        assert orchestrator.storage_controller.count() == 0
        Thread(target=orchestrator.run, daemon=True).start()

        sufficient_records = config.raw_session_creator['number_of_systems']
        num_of_runs = 30
        for j in range(num_of_runs):
            uuid = str(uuid1())
            for i in range(sufficient_records): # simulate client-side systems
                url = "record"
                record = [ LocalizationSysRecord, NetworkMonitorRecord, TransactionCloudRecord, Label][i](**{
                    "uuid":uuid,
                    "location_longitude":random()*360-180,
                    "location_latitude":random()*180-90,
                    "target_ip":'.'.join([str(randint(0, 255)),str(randint(0, 255)),str(randint(0, 255)),str(randint(0, 255))]),
                    "dest_ip":'.'.join([str(randint(0, 255)),str(randint(0, 255)),str(randint(0, 255)),str(randint(0, 255))]),
                    "timestamp":[randint(1, 100) for i in range(10)],
                    "amount":[randint(1, 100) for i in range(10)],
                    "label": choice(["normal", "moderate", "high"])})
                r = requests.post(f"http://127.0.0.1:{SELF_PORT}/{url}", json=record.__dict__) # this is intended to be unstructured (like for a client)
                assert r.status_code == 200, f"got {r.status_code} while sending to {url}"
        #for i in range(num_of_runs):
            if local_test:
                result = message_bus.popTopic("segregationSystem")
                assert result is not None, "raw_session not received"
                assert len(message_bus.messageQueues['segregationSystem'].queue) == 0, "still something in queue"
        if not local_test: # we need to wait for the orchestrator to finish
            input('press a key to exit...')


if __name__ == '__main__':
    TestPreparationSystemOrchestrator().test_run()