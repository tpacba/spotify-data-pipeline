import sqlalchemy
import pandas
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime, time
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite://played_tracks.sqlite"
TOKEN = "BQDNf9396JSJntm6onR6BFcwfkHsiis5hgwlPOkQvuEt9RbKXyXxDeADKXkHJ01rgmenivyvL6uak6-5EB6oA5-tGUG0Gkfun0qI_RhwewuQP4RKAnUDN9dGhYRfqFx1JFEnZdeIxX7HDYKtvAg_zw"

if __name__ == "__main__":

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    print(data)

    # song_names = []
    # artist_names = []
    # played_at_list = []
    # timestamps = []

    # for song in data["items"]:
    #     song_names.append(song["track"]["name"])
    #     artist_names.append(song["track"]["album"]["artists"][0]["name"])
    #     played_at_list.append(song["played_at"])
    #     timestamps.append(song["played_at"][0:10])

    # song_dict = {
    #     "song_name": song_names,
    #     "artist_name": artist_names,
    #     "played_at": played_at_list,
    #     "timestamp": timestamps

    # }

