import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("Youtube\.env")

#we all know why nothing in apu key
API_KEY = os.getenv("API_KEY") 
CHANNEL_HANDLE = "jujalag"
url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

def get_json_channel(url: str):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

def get_play_list_id(url: str):
    try:
        data = get_json_channel(url)

        chaneel_items = data["items"][0]
        channel_playlist_id = chaneel_items["contentDetails"]["relatedPlaylists"]
        
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlists = get_play_list_id(url)
    print(playlists)