import requests
import os
from riotwatcher import LolWatcher, ApiError

lol_watcher = LolWatcher(os.environ['TL_HACKS_RIOT_KEY'])
queue_info_url = "http://static.developer.riotgames.com/docs/lol/queues.json"

def check_current_game(summoner_id):
    try:
        result = lol_watcher.spectator.by_summoner('na1', summoner_id)
    except Exception as e:
        # probably not in game, deal with other errors differently
        return None

    if 'gameQueueConfigId' in result:
        queue_type = convert_queue_id_to_type(result['gameQueueConfigId'])
    else:
        queue_type = result['gameType']

    game_id = result['gameId']
    champion_id = None
    for player in result['participants']:
        if player['summonerId'] == summoner_id:
            champion_id = player['championId']

    return (champion_id, game_id, queue_type)

def convert_queue_id_to_type(queue_id):
    if queue_id == 0:
        return "Custom Game"
    queues_info = requests.get(queue_info_url)
    for queue in queues_info.json():
        if queue_id == queue['queueId']:
            return queue['description']
    return "Null game type"



def convert_champion_id_to_champion_name(champion_id):
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
        if champion_json['data'][champion]['key'] == champion_id:
            return champion_json['data'][champion]['name']
