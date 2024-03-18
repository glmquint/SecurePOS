from threading import Thread

from src.DataObjects.Content import Content
from src.DataObjects.Label import Label
from src.DataObjects.LocalizationSys import LocalizationSys
from src.DataObjects.NetworkMonitor import NetworkMonitor
from src.DataObjects.TransactionCloud import TransactionCloud
from src.JsonIO.JSONSender import JSONSender
from src.Service.ClassMapper import ClassMapper
from src.Service.ClientSideReceiver import ClientSideReceiver
from src.Service.RawInputLoader import RawInputLoader
from src.Service.ServiceReceiver import ServiceReceiver
import pandas as pd
import random
import json

class ServiceSystemOrchestator:
    def __init__(self):
        self.clientSideReceiver = ClientSideReceiver()

    def start(self):
        thread_client_side = Thread(target=self.MessagingReceiver.run)
        #thread_client_side = Thread(target=self.MessagingReceiver.run,kwargs={'port':5001})
        thread_client_side.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread_client_side.start()

        path_to_files = ["../../data/labels.csv", "../../data/localizationSys.csv",
                         "../../data/networkMonitor.csv", "../../data/transactionCloud.csv"]

        raw_input_loader = RawInputLoader(path_to_files)
        pandasFiles, csvFiles = raw_input_loader.load()
        while True:
            if len(pandasFiles) == 0:
                # All the record of all file has been sent
                break
            # extract random index
            index = random.randint(1, len(csvFiles)) -1
            # select the dataframe
            df = pandasFiles[index]
            # select the name of file extracted
            chosen_df_name = csvFiles[index]
            if len(df) == 0:
                # The record of all file has been sent
                pandasFiles.pop(index)
                csvFiles.pop(index)
                continue
            randomInt = random.randint(1, len(df)) - 1
            # refactor the data
            refactor_dic = (df.iloc[[randomInt][0]].to_dict())
            dict1 = dict()
            # reformat the dictionary
            timestamp = []
            amount = []
            for i in refactor_dic:
                if "ts" in i:
                    timestamp.append(refactor_dic[i])
                elif "am" in i:
                    amount.append(refactor_dic[i])
                else:
                    dict1[i] = refactor_dic[i]

                if len(timestamp) != 0:
                    dict1["ts"] = timestamp
                if len(amount) != 0:
                    dict1["am"] = amount
            # drop the current sample extracted
            pandasFiles[index] = df.drop(randomInt).reset_index(drop=True)
            mapped_class = None
            # dictToSend is the item to send
            mapped_class = ClassMapper.map_to_class(chosen_df_name, dict1)
                #print("Mapped class:", mapped_class.to_json())
            #record = Content(chosen_df_name, mapped_class)

            print("Record: ", mapped_class.to_json())
            # Remove comment to print the record for testing without sending
            #continue
            sender = JSONSender("",
                                "http://127.0.0.1:5000/ingestionSystem")
            #sender.send(mapped_class.to_json())

        # The system awaits for user input to stop
        input("Press Enter to stop the system")

if __name__ == "__main__":
    orchestrator = ServiceSystemOrchestator()
    orchestrator.start()

