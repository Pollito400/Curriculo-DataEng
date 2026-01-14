import os
import requests
from dotenv import load_dotenv

load_dotenv()

USER = "pollito400"
ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")

def get_json(url: str, headers: dict | None = None, timeout: int = 15):
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

def get_user(user: str, acess_token: str):
    try:
        url = f"https://api.spotify.com/v1/users/{user}"
        headers = {"Authorization": f"Bearer {acess_token}"}
        user_data = get_json(url, headers=headers)
        return user_data
    
    except requests.exceptions.RequestException as e:
        raise e


def get_artist(id_artist: str, access_token: str):
    try:
        url = f"https://api.spotify.com/v1/artists/{id_artist}"
        headers = {"Authorization": f"Bearer {access_token}"}
        artist_data = get_json(url, headers=headers)
        return artist_data

    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e

def get_artis_album(id_artist: str, acess_token: str):
    try:
        url = f'https://api.spotify.com/v1/artists/{id_artist}/albums?include_groups=album%2Csingle%2Cappears_on%2Ccompilation&limit=50'
        headers = {"Authorization": f"Bearer {acess_token}"}
        artist_album_data = get_json(url, headers=headers)
        return artist_album_data
    
    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e
 
def get_album_tracks(album_id:str, acess_token: str):
    try:
        url = f'https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50'
        headers = {"Authorization": f"Bearer {acess_token}"}
        album_data = get_json(url, headers=headers)
        return album_data
    except (requests.exceptions.RequestException, KeyError, ValueError, TypeError, IndexError) as e:
        raise e
 
    
if __name__ == "__main__":
    if not ACCESS_TOKEN:
        raise ValueError("Falta SPOTIFY_ACCESS_TOKEN en .env")
    print(get_user(user = USER))