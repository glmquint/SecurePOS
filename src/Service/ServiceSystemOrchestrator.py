from threading import Thread

from src.Service.ServiceReceiver import ServiceReceiver


class ServiceSystemOrchestator:
    def __init__(self):
        self.serviceReceiver = ServiceReceiver()


    def start(self):
        thread = Thread(target=self.serviceReceiver.run)
        thread.daemon = True  # this will allow the main thread to exit even if the server is still running
        thread.start()




if __name__ == "__main__":
    orchestrator = ServiceSystemOrchestator()
    orchestrator.start()
    while True:
        pass