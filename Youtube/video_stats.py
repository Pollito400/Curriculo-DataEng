import requests
import json

#we all know why nothing in apu key
API_KEY = "" 
CHANNEL_HANDLE = "jujalag"
url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

response = requests.get(url)
print(response)

data = response.json()
print(data)
print(json.dumps(data, indent=4))