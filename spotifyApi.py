import os
from dotenv import load_dotenv
import requests
import json
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_spotify_token():
    client_creds = f"{client_id}:{client_secret}"
    client_creds_base64 = base64.b64encode(client_creds.encode()).decode()
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {client_creds_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    
    if result.status_code != 200:
        print("Erro ao obter o token de autenticação:", result.status_code)
        print(result.content)
        return None
    
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_authorization_header():
    token = get_spotify_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    else:
        return None

def get_song_by_artist(artist_id):
    headers = get_authorization_header()
    if not headers:
        print("Erro: Não foi possível obter o cabeçalho de autorização.")
        return None
    
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=BR"
    result = requests.get(url, headers=headers)
    
    if result.status_code != 200:
        print("Erro ao obter as músicas do artista:", result.status_code)
        print(result.content)
        return None
    
    json_result = json.loads(result.content)["tracks"]
    tracks_info = []
    for track in json_result:
        track_info = {
            "id": track["id"],
            "name": track["name"],
            "href": track["href"],
            "link": track["external_urls"]["spotify"]
        }
        tracks_info.append(track_info)
    
    return tracks_info

# Exemplo de uso
artist_id = "6eUKZXaKkcviH0Ku9w2n3V"
songs = get_song_by_artist(artist_id)
for idx, song in enumerate(songs):
    print(f"{idx+1}. {song['name']}. Link externo: {song['link']}. HREF: {song['href']}")