import requests

subscribe_new_user_url = f"{os.environ['TL_HACKS_IP']}/subscribe_new_user"


def convert_champion_name_to_champion_id(champion_name):
    response = requests.get('https://ddragon.leagueoflegends.com/realms/na.json')

    if response.status_code != 200:
        print(f'Error finding realm info. Status code: {response.status_code}')
        raise RuntimeError()

    version_info = response.json()
    current_champion_version = version_info['n']['champion']
    champion_response = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{current_champion_version}/data/en_US/champion.json')
    if champion_response.status_code != 200:
        print(f'Error getting champion json info')
        raise RuntimeError()

    champion_json = champion_response.json()

    for champion in champion_json['data']:
        if champion_json['data'][champion]['name'] == champion_name:
            return champion_json['data'][champion]['key']

def send_new_user_subscriptions_to_db(user_id, streamer_name, champion_ids):
    payload = {
        'user': user_id,
        'streamer_name': streamer_name,
        'champion_ids': champion_ids
    }

    response = requests.post(url=subscribe_new_user_url, data=payload)

    return response.text
