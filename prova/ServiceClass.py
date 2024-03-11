import csv
from threading import Thread

from src.JsonIO.JSONEndpoint import JSONEndpoint
from src.JsonIO.JSONSender import JSONSender
from src.JsonIO.Server import Server


def serviceCallback(json_data):
    #message recived will be {system:"x", timestamp:'y', label:"k"}

    itemresults = json_data["system"], json_data["timestamp"], json_data["label"]

    filename = 'serviceFile.csv'
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(itemresults)


def messagingSystemCallback(json_data):
    # message recived will be {system:"x", timestamp:'y', label:"k"}

    itemresults = json_data["system"], json_data["content"]

    filename = 'messagingFile.csv'
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(itemresults)


def orchestrator():
    server = Server()
    server.add_resource(JSONEndpoint, "/serviceSystem", recv_callback=serviceCallback,
                        json_schema_path="")
    server.add_resource(JSONEndpoint, "/messagingSystem", recv_callback=messagingSystemCallback,
                        json_schema_path="")

    thread = Thread(target=server.run)
    thread.daemon = True  # this will allow the main thread to exit even if the server is still running
    thread.start()

    sender = JSONSender("", "http://127.0.0.1:5000/serviceSystem")
    sender.send({"system": "x", "timestamp": 'y', "label": "k"})
    sender = JSONSender("", "http://127.0.0.1:5000/messagingSystem")
    sender.send({"system": "x", "content": "y"})

def readFromCsv():
    #read from serviceFile
    with open('serviceFile.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        data = []
        for row in spamreader:
            data.append(row)
        print(data)

readFromCsv()