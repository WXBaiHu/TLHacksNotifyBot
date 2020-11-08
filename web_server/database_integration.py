import psycopg2
from twitch_integration import get_name_from_stream_id
import os

add_subscription_sql = '''INSERT INTO "subscriptions" ("stream_id", "expiration", "streamer_name") VALUES (%s, %s, %s)'''
get_users_where_champion_sql = '''SELECT * FROM "users" WHERE "champion_id" = %s AND "stream_id" = %s'''
insert_new_user_subscription_sql = '''INSERT INTO "users" ("user", "champion_id", "stream_id", "streamer_name") VALUES (%s, %s, %s, %s)'''
get_streamer_accounts_sql = '''SELECT * FROM "streamer_accounts" WHERE "stream_id" = %s'''

def connect_to_db():
    conn = None
    try:
        conn = psycopg2.connect(host=os.environ['TL_HACKS_DB_HOST'], database='testdb', user=os.environ['TL_HACKS_DB_USER'], password=os.environ['TL_HACKS_DB_PASS'], port='5432')
        return conn
    except Exception as e:
        print(f'Error connecting to database: {e}')
        raise RuntimeError()

def insert_new_subscription(stream_id, expiration):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(add_subscription_sql, (stream_id, expiration, get_name_from_stream_id(stream_id)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error in inserting new subscription, {e}")
        if conn is not None:
            cur.close()
            conn.rollback()
            conn.close()
        #deal with error somehow here

def get_users_by_champion(champion_id, stream_id):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(get_users_where_champion_sql, (champion_id, stream_id))
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error in getting users, {e}")
        if conn is not None:
            cur.close()
            conn.rollback()
            conn.close()
        #deal with error somehow here

def subscribe_a_new_user(user, stream_id, champion_ids, streamer_name):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        champion_ids = champion_ids.split("_")
        for champion_id in champion_ids:
            cur.execute(insert_new_user_subscription_sql, (user, champion_id, stream_id, streamer_name))
        conn.commit()
        cur.close()
        conn.close()
        return "Success"
    except Exception as e:
        print(f"Error in subscribing new user, {e}")
        if conn is not None:
            cur.close()
            conn.rollback()
            conn.close()
        #deal with error somehow here


def get_streamer_accounts(stream_id):
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(get_streamer_accounts_sql, (stream_id,))
        results = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        print(f"Error in getting streamer accounts, {e}")
        if conn is not None:
            cur.close()
            conn.rollback()
            conn.close()
        #deal with error somehow here
