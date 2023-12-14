from unittest import TestCase
import requests
import json


def send_message(endpoints, data):
    for sys in endpoints:
        url = "http://localhost:5000/system/" + sys
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Message sent successfully to " + sys)
            return True
        else:
            print(f"Failed to send  to " + sys + ". Status code: {response.status_code}")
            print(response.text)
            return False


systems = ["Ingestion_system", "Preparation_system", "Segregation_system", "Development_system",
           "Production_system", "Evaluation_system"]


class Test(TestCase):
    def test_receive_message(self):
        data = {"message": "startup"}
        self.assertTrue(send_message(systems, data))
        self.assertFalse(send_message(['not-a-valid-path'], data))
        data = {"malformed-message": "startup"}
        self.assertFalse(send_message(systems, data))
        # TODO: test also the builder classes

    def test_message(self):
        url = "http://localhost:5000/messages"
        response = requests.delete(url)
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['messages'], [])
        data = {"message": "hello message"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['status'], 'success')
        response = requests.get(url, headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)
        res = response.json()
        self.assertEqual(res['status'], 'success')
        self.assertEqual(res['messages'], ['hello message'])

