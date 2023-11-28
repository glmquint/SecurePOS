import requests
import json

def send_message(message):
    system = {"Ingestion_system", "Preparation_system", "Segregation_system", "Development_system",
              "Production_system", "Evaluation_system"}
    for sys in system:
        url = "http://localhost:5000/system/"+sys
        headers = {"Content-Type": "application/json"}
        data = {"message": message}

        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            print("Message sent successfully to " + sys)
        else:
            print(f"Failed to send  to "+sys+". Status code: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    send_message("startup")
