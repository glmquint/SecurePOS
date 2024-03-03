import requests
r = requests.post('http://127.0.0.1:5000/segregationSystem',json={"key": "value"})
print(r.json())
r = requests.get('http://127.0.0.1:5000/')
print(r.json())
