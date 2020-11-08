from riot_api_integration import check_current_game, convert_champion_id_to_champion_name
from database_integration import get_users_by_champion
import requests
import json
import os
import sys

webhook_url = os.environ['TL_HACKS_DISCORD_WEBHOOK']
encrypted_summoner_id = sys.argv[1]
stream_id = sys.argv[2]
#previously found game is used to make sure we don't report the same game notification twice
previously_found_game = sys.argv[3]

game_info = check_current_game(sys.argv[1])
if not game_info or game_info[1] == previously_found_game:
    quit()

subscribed_users = get_users_by_champion(game_info[0], stream_id)

# currently only works for one person, needs to be expanded to handle more notfications

if not subscribed_users:
    quit()

data = {
    'content': f'<@{subscribed_users[0][0]}> {subscribed_users[0][3]} is playing {convert_champion_id_to_champion_name(str(subscribed_users[0][1]))} in a {game_info[2]} on stream right now!'
}

requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
