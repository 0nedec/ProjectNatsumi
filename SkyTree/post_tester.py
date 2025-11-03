import requests
import json

url = 'http://127.0.0.1:5000/tasks'
json_payload = [{"task_type":"ping"}]

# requests automatically sets the Content-Type header to application/json
response = requests.post(url, json=json_payload)

print(response.text)
