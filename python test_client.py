import requests

url = "http://0.0.0.0:8000/process_data"
data = {
    "question": "What is the weather today?",
    "chat_history": []
}

response = requests.post(url, json=data)
print(response.json())

