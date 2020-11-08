from crontab import CronTab
from database_integration import get_streamer_accounts
import time

def start_cron_job(stream_id):
    cron = CronTab()
    accounts = get_streamer_accounts(stream_id) #currently only handles one account per streamer

    job = cron.new(command=f'python riotapi_polling.py {accounts[0][1]} {stream_id} {accounts[0][2]}')

    job.second.every(10)

    cron.write()

    time.sleep(30)

    job.enable(False)
