import sqlalchemy
import pandas
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime, time
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite://played_tracks.sqlite"
TOKEN = "BQBhUX4NJBojYKveeqnYapLriqfltABqMtqmblIF9UsLPSvBGY-qYCZDoIG6oJ1hlz6NZBivp3vYAtBU0kom3wuKJJsybt1yk8xMjz1tbR2yiOZ4BO8hK1GNJs4dtUd6OrtGwrsyGjLLjE1-r-JLZQ"

def check_if_valid_data(df: pandas.DataFrame) -> bool:
    if df.empty:
        print("No songs downloaded.")
        return False
    
    if pandas.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Priamry Key check is violated")

    if df.isnull().values.any():
        raise Exception("Null values found")

    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.replace(hour=0,minute=0,second=0,microsecond=0)

    # timestamps = df["timestamp"].tolist()
    # for ts in timestamps:
    #     if datetime.datetime.strptime(ts, "%Y-%m-%d") != yesterday:
    #         raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True


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

    # print(data)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pandas.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)

    if check_if_valid_data(song_df):
        print("Data valid")
