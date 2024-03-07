from threading import Thread
from unittest import TestCase
import pandas as pd
import json
import random

import requests

from src.DataObjects.Message import Message
from src.DataObjects.RawSession import RawSession
from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server
from src.Service.ServiceReceiver import ServiceReceiver


class TestServiceReceiver(TestCase):

    def self_server_setup(self):
        server = Server()
        test_callback = lambda json_data: print(f"Hello from test_callback. Received {json_data}")
        server.add_resource(JSONEndpoint, "/test_endpoint", recv_callback=test_callback,
                            json_schema_path="../DataObjects/Schema/RawSessionSchema.json")
        thread = Thread(target=server.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()

    @classmethod
    def service_server_setup(self):
        serviceRec = ServiceReceiver()
        thread = Thread(target=serviceRec.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()


    def test_run(self):
        self.service_server_setup()
        messageTest = Message("Hello World")
        req = requests.post("http://127.0.0.1:5000/MessagingSystem", json=messageTest.to_json())  # correct key
        assert req.status_code == 200
        # assert the content of log.txt is "Message: Hello World"
        with open("log.txt", "r") as log:
            assert log.read() == "Message: Hello World\n"
        # delete the content of log.txt
        with open("log.txt", "w") as log:
            log.write("")
        req = requests.post("http://127.0.0.1:5000/ClientSideSystem", json=messageTest.to_json())  # correct key
        assert req.status_code == 200
        # assert the content of log.txt is "Message: Hello World"
        with open("log.txt", "r") as log:
            assert log.read() == "Message: Hello World\n"
        # delete the content of log.txt
        with open("log.txt", "w") as log:
            log.write("")

        # delete log.txt
        import os
        os.remove("log.txt")

    def test_sender(self):
        self.self_server_setup()
        json_data = {
            "UUID": "a923-45b7-gh12-2869",
            "LABEL": "normal",
            "latitude": -18.0032216230982,
            "longitude": -84.4669574843863,
            "targetIP": "192.168.25.4",
            "destIP": "192.168.90.203",
            "ts": [7520.38693128729, 7540.01476282207, 7560.84201643904, 7525.55036998267, 7430.31526699634,
                   7582.75161317361, 7475.14787953081, 7531.53034928949, 7372.96400321726, 7610.16990766799],
            "am": [12.8505469215328, 13.5047152766449, 14.0224623386235, 14.9328568509386, 13.0022587486345,
                   15.9005029483746, 11.6345719786612, 14.4606348281486, 14.6495303464239, 14.0635376533773]
        }

        rawSession = RawSession.from_json(json_data)

        sender = JSONSender("../DataObjects/Schema/RawSessionSchema.json",
                            "http://127.0.0.1:5000/test_endpoint")
        print(rawSession.to_json())
        assert sender.send(rawSession.to_json()) == True


    def test_sender1(self):
        # create dataframe from csv files
        label_df = pd.read_csv('../data/labels.csv')
        localizationSys_df = pd.read_csv('../data/localizationSys.csv')
        networkMonitor_df = pd.read_csv('../data/networkMonitor.csv')
        transactionCloud_df = pd.read_csv('../data/transactionCloud.csv')

        csvFiles = ["labels", "localizationSys", "networkMonitor", "transactionCloud"]
        pandasFiles = [label_df, localizationSys_df, networkMonitor_df, transactionCloud_df]

        index = random.randint(0, len(csvFiles) - 1)
        df = pandasFiles[index]
        label = csvFiles[index]

        dic = (df.iloc[[random.randint(0, len(df))][0]].to_dict())
        dict1 = dict()

        #reformat the dictionary
        timestamp = []
        amount = []
        for i in dic:
            if "ts" in i:
                timestamp.append(dic[i])
            elif "am" in i:
                amount.append(dic[i])
            else:
                dict1[i] = dic[i]

            if len(timestamp) != 0:
                dict1["ts"] = timestamp
            if len(amount) != 0:
                dict1["am"] = amount

        dictToSend = dict()
        dictToSend["record"] = label
        dictToSend["content"] = dict1
        df = df.drop(index).reset_index(drop=True)

        # print(dictToSend)
        print(json.dumps(dictToSend))

        # dictToSend is the item to send





