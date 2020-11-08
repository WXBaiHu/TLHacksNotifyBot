import os
import discord
from utils import convert_champion_name_to_champion_id, send_new_user_subscriptions_to_db

token = os.environ['BLUE_BOT_TOKEN']
testing_channel_ids = set([753100663256383632, 774830491832025121])

help_text = "Subscribe to a streamer using a set of champions and be notified anytime they are playing them on stream\rCommand Structure: !subscribe {streamer name} {list of champions seperated by commas}\rFor Example: !subscribe Jensen Orianna,Galio,Zed"

client = discord.Client()


@client.event
async def on_message(message):
    channel = message.channel

    if message.channel.id not in testing_channel_ids:
        return
    if message.author == client.user:
        return
    if message.content[0] != ("!"):
        return

    user_command = message.content[1:].split()

    if not user_command:
        return

    if user_command[0] == "help":
        await channel.send(help_text)
        return
    if user_command[0] == "subscribe":
        if len(user_command) != 3:
            await channel.send(f"Invalid structure for subscribe\r{help_text}")
            return

        streamer_name = user_command[1]
        champion_list = user_command[2].replace("_", " ").split(",")
        champion_id_list = []

        for champion_name in champion_list:
            champion_key = convert_champion_name_to_champion_id(champion_name)
            champion_id_list.append(champion_key)

        champion_ids = "_".join(champion_id_list)

        user_id = message.author.id
        if send_new_user_subscriptions_to_db(user_id, streamer_name, champion_ids) == "Success":
            await channel.send("Your subscription was succesful =)")
        else:
            await channel.send("Your subscription failed =(")
        return








client.run(token)
