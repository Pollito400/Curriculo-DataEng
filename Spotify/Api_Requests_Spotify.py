import os
import requests
from dotenv import load_dotenv

load_dotenv()

USER = "pollito400"
ACCESS_TOKEN = os.getenv("SPOTIFY_ACCESS_TOKEN")  # ponlo en tu .env

def get_json(url: str, headers: dict | None = None):
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()

def get_user(user: str):
    url = f"https://api.spotify.com/v1/users/{user}"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    return get_json(url, headers=headers)

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        raise ValueError("Falta SPOTIFY_ACCESS_TOKEN en tu .env")
    print(get_user(user = USER))