import requests
import json
import os
from dotenv import load_dotenv

load_dotenv("Youtube\\.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "jujalag"   # si te falla, prueba "@jujalag"
maxResults = 50
MinResults = 1


def get_json(url: str):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e


def get_play_list_id(channel_handle=CHANNEL_HANDLE, api_key=API_KEY):
    try:
        url = (
            "https://youtube.googleapis.com/youtube/v3/channels"
            f"?part=contentDetails&forHandle={channel_handle}&key={api_key}"
        )
        data = get_json(url)

        channel_items = data["items"][0]
        return channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e


def get_videos_ids(channel_handle=CHANNEL_HANDLE, Results=MinResults, api_key=API_KEY):
    try:
        channel_playlist_id = get_play_list_id(channel_handle=channel_handle, api_key=api_key)

        video_ids = []
        pageToken = None

        while True:
            url = (
                "https://youtube.googleapis.com/youtube/v3/playlistItems"
                f"?part=contentDetails&maxResults={Results}&playlistId={channel_playlist_id}&key={api_key}"
            )
            if pageToken:
                url += f"&pageToken={pageToken}"

            data = get_json(url)

            for item in data.get("items", []):
                # playlistItems -> contentDetails.videoId
                video_ids.append(item["contentDetails"]["videoId"])

            pageToken = data.get("nextPageToken")
            if not pageToken:
                break

        return video_ids
    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e


def get_video_data(api_key=API_KEY, maxResults=maxResults):
    try:
        # esto te trae IDs desde la playlist uploads del canal
        video_ids = get_videos_ids(channel_handle=CHANNEL_HANDLE, Results=maxResults, api_key=api_key)
        videos = []
        # videos.list acepta máximo 50 ids por request
        for index in range(0, len(video_ids), maxResults):
            batch = video_ids[index:index + maxResults]
            ids_str = ",".join(batch) 
            
            url = (
                "https://youtube.googleapis.com/youtube/v3/videos"
                f"?part=contentDetails,snippet,statistics&id={ids_str}&key={api_key}"
            )

            data = get_json(url)

            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                details = item.get("contentDetails", {})
                stats = item.get("statistics", {})

                vid = item.get("id")
                videos.append({
                    "id": vid,
                    "title": snippet.get("title"),
                    "publishedAt": snippet.get("publishedAt"),
                    "channelTitle": snippet.get("channelTitle"),
                    "duration": details.get("duration"),
                    "views": int(stats.get("viewCount", 0)),
                    "likes": int(stats.get("likeCount", 0)),
                    "comments": int(stats.get("commentCount", 0)),
                    "thumb": snippet.get("thumbnails", {}).get("high", {}).get("url"),
                    "url": f"https://www.youtube.com/watch?v={vid}" if vid else None
                })

        return videos
    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e


if __name__ == "__main__":
    # IDs
    ids = get_videos_ids(channel_handle=CHANNEL_HANDLE, Results=maxResults, api_key=API_KEY)
    print("IDs encontrados:", len(ids))
    print(ids[:10])

    # Datos completos
    videos = get_video_data(api_key=API_KEY, maxResults=maxResults)
    print("Videos con data:", len(videos))
    print(videos[:2])
