import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("Youtube\.env")

#we all know why nothing in apu key
API_KEY = os.getenv("API_KEY") 
CHANNEL_HANDLE = "jujalag"
maxResults = 50

def get_json(base_url: str, params: dict):
    try:
        r = requests.get(base_url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise e

def get_uploads_playlist_id(api_key: str, channel_handle: str) -> str:
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "contentDetails",
        "forHandle": channel_handle,
        "key": api_key,
    }

    data = get_json(base_url, params)
    channel_item = data["items"][0]
    return channel_item["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_ids_from_playlist(api_key: str, playlist_id: str, max_results: int = 50) -> list[str]:
    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    video_ids = []
    page_token = None

    while True:
        params = {
            "part": "contentDetails",
            "playlistId": playlist_id,
            "maxResults": max_results,
            "key": api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        data = get_json(base_url, params)

        for item in data.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return video_ids

if __name__ == "__main__":
    uploads_playlist_id = get_uploads_playlist_id(API_KEY, CHANNEL_HANDLE)
    print("Uploads playlist id:", uploads_playlist_id)

    video_ids = get_video_ids_from_playlist(API_KEY, uploads_playlist_id, maxResults)
    print("Total videos:", len(video_ids))
    print("Primeros 5:", video_ids[:5])