import os
from dotenv import load_dotenv
import requests

load_dotenv()

IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
IMGUR_CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET')
IMGUR_ESOXO_REFRESH_TOKEN = os.getenv('IMGUR_ESOXO_REFRESH_TOKEN')
IMGUR_API_URL = "https://api.imgur.com"

class ImgurClient() :
    def __init__(self, client_id, client_secret = None) :
        self.client_id = client_id
        self.client_secret = client_secret

    def set_client_secret(self, client_secret) :
        self.client_secret = client_secret

    def generate_access_token(self, refresh_token) :
        if not self.client_secret:
            raise Exception("Client secret needed for generating access token")
        url = f"{IMGUR_API_URL}/oauth2/token"
        body = {
            'refresh_token' : refresh_token,
            'client_id' : self.client_id,
            'client_secret' : self.client_secret,
            'grant_type' : 'refresh_token'
        }
        response : requests.Response = requests.post(url, json=body)
        response.raise_for_status()
        return response.json()['access_token']

    def get_user_albums(self, user: str, userToken: str = '') :
        url = f"{IMGUR_API_URL}/3/account/{user}/albums/"
        headers = { 'Authorization': f'Client-ID {IMGUR_CLIENT_ID}' } if not userToken else { 'Authorization': f'Bearer {userToken}' }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    
    def get_album_images(self, album_id: str, userToken: str = '') :
        url = f"{IMGUR_API_URL}/3/album/{album_id}/images"
        headers = { 'Authorization': f'Client-ID {IMGUR_CLIENT_ID}' } if not userToken else { 'Authorization': f'Bearer {userToken}' }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    
    def get_album_image(self, album_id: str, image_id, userToken: str = '') :
        url = f"{IMGUR_API_URL}/3/album/{album_id}/image/{image_id}"
        headers = { 'Authorization': f'Client-ID {IMGUR_CLIENT_ID}' } if not userToken else { 'Authorization': f'Bearer {userToken}' }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']


def get_relevant_albums() -> list :
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    access_token = client.generate_access_token(IMGUR_ESOXO_REFRESH_TOKEN)
    return [album for album in client.get_user_albums('esoxo', access_token) if album['title'].startswith('eeveeTelebot-')]

def generate_available_pets() -> dict :
    pet_albums = get_relevant_albums()
    pets = {}
    for album in pet_albums:
        pet = album['title'].removeprefix('eeveeTelebot-')
        pets.update({ pet : album['id'] })
    return pets

def get_album_images(album_id: str) -> list :
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    access_token = client.generate_access_token(IMGUR_ESOXO_REFRESH_TOKEN)
    return client.get_album_images(album_id, access_token)

def get_album_image(album_id: str, image_id: str) -> dict :
    client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
    access_token = client.generate_access_token(IMGUR_ESOXO_REFRESH_TOKEN)
    return client.get_album_image(album_id, image_id, access_token)


if __name__ == '__main__' :
    imgs = get_relevant_albums()
    print(imgs[3])