from threading import Thread

from src.DataObjects.Content import Content
from src.DataObjects.Label import Label
from src.DataObjects.LocalizationSys import LocalizationSys
from src.DataObjects.NetworkMonitor import NetworkMonitor
from src.DataObjects.TransactionCloud import TransactionCloud
from src.JsonIO.JSONSender import JSONSender
from src.Service.ServiceReceiver import ServiceReceiver
import pandas as pd
import random
import json

class ServiceSystemOrchestator:
    def __init__(self):
        self.serviceReceiver = ServiceReceiver()

    def start(self):
        """
        thread = Thread(target=self.serviceReceiver.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()
        """
        label_df = pd.read_csv('../../data/labels.csv')
        localizationSys_df = pd.read_csv('../../data/localizationSys.csv')
        networkMonitor_df = pd.read_csv('../../data/networkMonitor.csv')
        transactionCloud_df = pd.read_csv('../../data/transactionCloud.csv')

        csvFiles = ["labels", "localizationSys", "networkMonitor", "transactionCloud"]
        pandasFiles = [label_df, localizationSys_df, networkMonitor_df, transactionCloud_df]

        while True:
            # extract random index
            index = random.randint(0, len(csvFiles) - 1)
            # select the dataframe
            df = pandasFiles[index]
            # select the name of file extracted
            chosen_df_name = csvFiles[index]

            # refactor the data
            dic = (df.iloc[[random.randint(0, len(df))][0]].to_dict())
            dict1 = dict()

            # reformat the dictionary
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

            #drop the current sample extracted
            pandasFiles[index] = df.drop(index).reset_index(drop=True)

            mapped_class = None
            # dictToSend is the item to send
            if chosen_df_name == 'labels':
                mapped_class = Label(dict1['UUID'], dict1['LABEL'])
            elif chosen_df_name == 'localizationSys':
                # Assuming you have a class called LocalizationSys
                mapped_class = LocalizationSys(dict1['UUID'], dict1['longitude'],
                                               dict1['latitude'])
            elif chosen_df_name == 'networkMonitor':
                # Assuming you have a class called NetworkMonitor
                mapped_class = NetworkMonitor(dict1['UUID'], dict1['targetIP'],
                                              dict1['destIP'])
            elif chosen_df_name == 'transactionCloud':
                # Assuming you have a class called TransactionCloud
                mapped_class = TransactionCloud(dict1['UUID'], dict1['ts'],
                                                dict1['am'])

            print("Mapped class:", mapped_class.to_json())

            record = Content(chosen_df_name, mapped_class)

            print("Record: ", record.to_json())

            sender = JSONSender("",
                                "http://127.0.0.1:5000/ingestionSystem")
            sender.send(record.to_json())



if __name__ == "__main__":
    orchestrator = ServiceSystemOrchestator()
    orchestrator.start()
    while True:
        pass
