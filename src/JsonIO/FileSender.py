import requests


class FileSender:
    def __init__(self, url: str):
        self.url = url

    def send(self, file):
        try:
            files = {'uploaded': file}
            requests.post(self.url, files=files)
        except Exception as e:
            print(e)
            return False
        return True
