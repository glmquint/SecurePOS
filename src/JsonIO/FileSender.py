import requests


class FileSender:
    """
        This class is responsible for sending files to a specified URL.

        Attributes:
            url: A string containing the URL to which the file should be sent.

        Methods:
            send: Sends a file to the specified URL. It sends a POST request with the file as a parameter.
            If the request fails, it prints the error and returns False. Otherwise, it returns True.
    """
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
