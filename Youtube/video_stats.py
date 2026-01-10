import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("Youtube\.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "jujalag"
maxResults = 50

def get_json(url: str):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

def get_play_list_id(url: str):
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&id={CHANNEL_HANDLE}&key={API_KEY}'
        data = get_json(url)

        chaneel_items = data["items"][0]
        channel_playlist_id = chaneel_items["contentDetails"]["relatedPlaylists"]['uploads']
        
        return channel_playlist_id
    except requests.exceptions.RequestException as e:
        raise e

def get_videos_play_ids(url: str):
    url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={channel_playlist_id}&key={API_KEY}'
    video_ids = []
    pageToken = None
    
    try:
        while True:
            if pageToken:
                base_url += f"pageToken={pageToken}"
            data = get_json(url)
            for item in data.get('items', []):
                video_id = item["items"][0]["contentDetails"]
                video_ids .append(video_id)
            pageToken = data.get('nextPageToken')

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
