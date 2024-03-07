from random import random
from threading import Thread
from time import sleep

import requests

from src.DataObjects.AttackRiskLabel import AttackRiskLabel
from src.DataObjects.Record import Record
from src.DataObjects.Session import PreparedSession, RawSession
from src.Ingestion.PreparationSystemConfig import PreparationSystemConfig
from src.Ingestion.IngestionOrchestrator import PreparationSystemOrchestrator
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.Server import Server
from src.MessageBus.MessageBus import MessageBus

DATAOBJ_PATH = "../DataObjects/Schema"

TEST_PORT = 4000

message_bus = MessageBus([])
test_everything = False

def listener_setup(prepared_session_creator):
    global message_bus
    server = Server()
    for endpoint, val in prepared_session_creator.items():
        url = val['url'].split('/')[-1]
        print(f"adding {url}")
        message_bus.addTopic(url)
        def builder(url):
            def callback(json_data):
                print(f"hello from {url} received {json_data}")
                message_bus.pushTopic(url, json_data)
            return callback
        schema = {'segregation_system':'PreparedSessionSchema', 'production_system':'PreparedSessionSchema', 'label': 'AttackRiskLabelSchema'}.get(url, None)
        server.add_resource(JSONEndpoint, f"/{url}", recv_callback=builder(url), json_schema_path=f"../DataObjects/Schema/{schema}.json")
    Thread(target=server.run, daemon=True, kwargs={'port':TEST_PORT}).start()

class TestPreparationSystemOrchestrator:
    def test_run(self):
        global message_bus
        config = PreparationSystemConfig(f"{DATAOBJ_PATH}/PreparationSystemConfigSchema.json")
        config.init_from_file("PreparationSystemConfig.json")
        c:dict = config.prepared_session_creator
        c.update({'label_receiver': config.raw_session_creator['label_receiver']})
        listener_setup(c)
        if test_everything:
            for endpoint, val in c.items():
                url = val['url'].split('/')[-1]
                print(f"Sending to {url}")
                objtype = {'segregation_system': PreparedSession, 'production_system': PreparedSession,
                          'label': AttackRiskLabel}.get(url, None)
                r = requests.post(f"http://127.0.0.1:{TEST_PORT}/{url}", json=objtype().to_json())
                assert r.status_code == 200, f"got {r.status_code} while sending to {url}"
                assert message_bus.popTopic(url) is not None, "raw_session not received"

        # ok, now let's start our system orchestrator
        orchestrator = PreparationSystemOrchestrator(config)
        Thread(target=orchestrator.run, daemon=True).start()

        if test_everything:
            # before testing it, we check the internal receiver
            for endpoint, url in config.raw_session_creator['raw_session_receiver'].items(): # should be only raw session receiver
                url = url.split('/')[-1]
                rs = RawSession()
                r = requests.post(f"http://127.0.0.1:5000/{url}", json=rs.to_json())
                assert r.status_code == 200, f"got {r.status_code} while sending to {url}"

        for i in range(10): # simulate client-side systems
            url = "record"
            r = requests.post(f"http://127.0.0.1:5000/{url}", json=Record(**{'device_src':str(random())}).to_json())
            assert r.status_code == 200, f"got {r.status_code} while sending to {url}"
        for i in range(1): # simulate client-side systems
            result = message_bus.popTopic("segregation_system")
            assert result is not None, "raw_session not received"