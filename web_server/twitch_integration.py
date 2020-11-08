import requests
import os


AUTH_URL = "https://id.twitch.tv/oauth2/token"
REVOKE_URL = "https://id.twitch.tv/oauth2/revoke"
WEBHOOKS_URL = "https://api.twitch.tv/helix/webhooks/hub"
GET_ID_URL = "https://api.twitch.tv/helix/users"
ACCESS_TOKEN = os.environ['TWITCH_ACCESS_TOKEN']


def subscribe_by_login_name(stream_name):
    stream_id = get_id_from_stream_name(stream_name)
    subscribe_to_stream(stream_id)
    return "done"

def get_auth_token():
    payload = {
        'client_id': os.environ['TL_HACKS_TWITCH_CLIENT_ID'],
        'client_secret': os.environ['TL_HACKS_TWITCH_CLIENT_SECRET'],
        'grant_type': 'client_credentials'
    }
    response = requests.post(AUTH_URL, params=payload)

def revoke_auth_token(token):
    payload = {
        'client_id': os.environ['TL_HACKS_TWITCH_CLIENT_ID'],
        'token': token
    }

    response = requests.post(REVOKE_URL, params=payload)


def subscribe_to_stream(stream_id):
    headers = {
        'Client-ID': os.environ['TL_HACKS_TWITCH_CLIENT_ID'],
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {
        'hub.callback': f'{os.environ['TL_HACKS_IP']}/stream_subscription?stream_id={stream_id}',
        'hub.mode': 'subscribe',
        'hub.topic': f'https://api.twitch.tv/helix/streams?user_id={stream_id}',
        'hub.lease_seconds': 864000,
        'hub.secret': os.environ['TL_HACKS_TWITCH_CLIENT_SECRET']
    }

    response = requests.post(WEBHOOKS_URL, headers=headers, data=payload)
    print(response.text)

def get_id_from_stream_name(stream_name):
    headers = {
        'Client-Id': os.environ['TL_HACKS_TWITCH_CLIENT_ID'],
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    payload = {
        'login': stream_name
    }

    response = requests.get(GET_ID_URL, headers=headers, params=payload)
    return response.json()['data'][0]['id']

def get_name_from_stream_id(stream_id):
    headers = {
        'Client-Id': os.environ['TL_HACKS_TWITCH_CLIENT_ID'],
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }

    payload = {
        'id': stream_id
    }

    response = requests.get(GET_ID_URL, headers=headers, params=payload)
    return response.json()['data'][0]['display_name']
