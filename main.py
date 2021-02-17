import sqlalchemy
import pandas
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime, time
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///played_tracks.sqlite"
TOKEN = "BQBxO3rV8UCRVrgCsMfsEXZ2nwrwsAvBN3oD_F_9O8x4EaIbYyU5zMtcipz6x77JW5EWT5RYgN-uo_X1voNVB0OpFkywirqdigqI0t_IUvm7M7ntc5ixb-_hol926TI8-Dq34RzXBnCY44jhwUJDmg"

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


    if check_if_valid_data(song_df):
        print("Data valid")
        # print(song_df)

    engine  = sqlalchemy.create_engine(DATABASE_LOCATION)
    connection = sqlite3.connect("played_tracks.sqlite")
    cursor = connection.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfuly")

    try:
        song_df.to_sql("played_tracks", engine, index=False, if_exists='append')
        print("Added to database successfully")
    except:
        print("Data already exists")

    connection.close()
    print("Database closed successfully")