import json
from webbrowser import get
from dotenv import load_dotenv # type: ignore
import os
from requests import post # type: ignore
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_spotify_token():
    client_creds = f"{client_id}:{client_secret}"
    client_creds_bytes = client_creds.encode("utf-8")
    client_creds_base64 = str(base64.b64encode(client_creds_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {client_creds_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_authorization_header():
    token = get_spotify_token()
    return {"Authorization": f"Bearer {token}"}

#def get_playlist_tracks(playlist_id):
    token = get_spotify_token()
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_authorization_header()
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data) 
    json_result = json.loads(result.content)

    if "items" in json_result:
        return json_result["items"]
    else:
        print("Erro: A resposta da API não contém a chave 'items'.")
        print(json_result)
        return None

#playlist_id = "37i9dQZF1DXcBWIGoYBM5M"
#tracksID = get_playlist_tracks(playlist_id)

token = get_spotify_token()
print(token)

