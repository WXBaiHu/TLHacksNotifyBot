from flask import Flask, request
from twitch_integration import get_auth_token, revoke_auth_token,subscribe_to_stream, subscribe_by_login_name, get_id_from_stream_name
from database_integration import insert_new_subscription, subscribe_a_new_user
from cron_job import start_cron_job
from threading import Thread
from datetime import timedelta, datetime

app = Flask(__name__)

@app.route('/add_new_streamer', methods = ['POST'])
def add_new_streamer():
    return subscribe_by_login_name(request.form['streamer_name'])

@app.route('/add_new_streamer_manual')
def add_new_streamer_manual():
    return subscribe_by_login_name("")

@app.route('/subscribe_new_user', methods = ['POST'])
def subscribe_new_user():
    stream_id = get_id_from_stream_name(request.form['streamer_name'])
    if (subscribe_a_new_user(request.form['user'], stream_id, request.form['champion_ids'], request.form['streamer_name'])):
        return "Success"
    #Need to add error handling
    return "Fail"


@app.route('/stream_subscription', methods = ['POST', 'GET'])
def validate_webhook():
    if request.method == 'GET':
        stream_id = request.args.get('hub.topic').split('=')[-1]
        expiration = datetime.now() + timedelta(seconds=int(request.args.get('hub.lease_seconds')))
        Thread(target = insert_new_subscription(stream_id, expiration)).start()
        return request.args.get('hub.challenge')
        #this needs to be changed so that it is updatable in the future when needing to refresh susbscriptions
    else:
        if request.json['data'] and (request.json['data'][0]['type'] == 'live'):
            start_cron_job(request.args.get('stream_id'))
        else:
            #stop cron job, probably need to poll for stream uptime since it seems incsonsitent whether or not the end of stream actually triggers the webhook
            quit()

        return '', 200

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
