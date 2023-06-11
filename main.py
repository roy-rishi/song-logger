import spotipy
from spotipy.oauth2 import SpotifyOAuth
import vars
from datetime import datetime
import json
import time
import subprocess


def authenticate():
    scope = "user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=vars.CLIENT_ID, client_secret= vars.CLIENT_SECRET, redirect_uri=vars.REDIRECT_URL, scope=scope))
    return sp

def raiseNetworkError():
    raise Exception("\033[91mERROR: Could not connect to Spotify. Device may be offline, or the network may be blocking this request")

def nowPlaying(sp):
    try:
        nowPlaying = sp.current_playback()
    except:
        raiseNetworkError()
    return nowPlaying

def artistNames(playing):
    artists = playing["item"]["artists"]
    names = []
    for artist in artists:
        names.append(artist["name"])
    return names

def artistURIs(playing):
    artists = playing["item"]["artists"]
    names = []
    for artist in artists:
        names.append(artist["uri"])
    return names

def albumName(playing):
    return playing["item"]["album"]["name"]

def albumURI(playing):
    return playing["item"]["album"]["uri"]

def trackName(playing):
    return playing["item"]["name"]

def trackURI(playing):
    return playing["item"]["uri"]

def context(playing):
    return playing["context"]["uri"]

def progressMs(playing):
    return playing["progress_ms"]

def durationMs(playing):
    return playing["item"]["duration_ms"]

def isPlaying(playing):
    return bool(playing["is_playing"])

def shuffleState(playing):
    return bool(playing["shuffle_state"])

def currentTimeFormatted():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

def songItem(ts, platform, msPlayed, trackName, artistName, albumName, trackURI, reasonStart, reasonEnd, shuffle, skipped, incognito):
    template = {
        "ts": ts,
        "username": "unknown",
        "platform": platform,
        "ms_played": msPlayed,
        "conn_country": "unknown",
        "ip_addr_decrypted": "unknown",
        "user_agent_decrypted": "unknown",
        "master_metadata_track_name": trackName,
        "master_metadata_album_artist_name": artistName,
        "master_metadata_album_album_name": albumName,
        "spotify_track_uri": trackURI,
        "episode_name": "unknown",
        "episode_show_name": "unknown",
        "spotify_episode_uri": "unknown",
        "reason_start": reasonStart,
        "reason_end": reasonEnd,
        "shuffle": shuffle,
        "skipped": skipped,
        "offline": "unknown",
        "offline_timestamp": "unknown",
        "incognito_mode": incognito
    }
    return template

def initSong(playing):

    artist_names = artistNames(playing)
    artist_uris = artistURIs(playing)
    album_name = albumName(playing)
    album_uri = albumURI(playing)
    track_name = trackName(playing)
    track_uri = trackURI(playing)
    context_uri = context(playing)
    ms_progress = progressMs(playing)
    ms_duration = durationMs(playing)
    is_playing = isPlaying(playing)
    shuffle = shuffleState(playing)
    ts = currentTimeFormatted()

    song = songItem(
        ts=ts,
        platform="unknown",
        msPlayed=0,
        trackName=track_name,
        artistName=artist_names,
        albumName = album_name,
        trackURI=track_uri,
        reasonStart="unknown",
        reasonEnd="unknown",
        shuffle=shuffle,
        skipped="unknown",
        incognito="unknown"
        )
    return song

def readLogs():
    logFile = open(vars.DATA_PATH)
    logs = json.load(logFile)
    logFile.close()
    return logs

def writeLogs(logs):
    logFile = open(vars.DATA_PATH, "w")
    json.dump(logs, logFile, indent=2)
    logFile.close()

def curTime():
    return time.time() * 1000


logs = readLogs()

sp = authenticate()
playing = nowPlaying(sp)
# if playing != None:
#     song = initSong(playing)
song = logs[-1]

ms_played = 0
interval = 2
lastPlayed = curTime()


while True:
    try:
        playing = nowPlaying(sp)

        if playing != None and isPlaying(playing):
            cur_time = curTime()
            ms_played += (cur_time - lastPlayed)
            lastPlayed = cur_time
            print(f"{int(ms_played)} ms")
        else:
            lastPlayed = curTime()

        if playing != None and trackURI(playing) != song["spotify_track_uri"]:
            song["ms_played"] = int(ms_played)
            lastPlayed = curTime()
            ms_played = 0

            logs.append(song)
            writeLogs(logs)

            song = initSong(playing)
            print(f"\nwatching {song['master_metadata_track_name']}")
    except Exception as e:
        print(e)
        subprocess.call(["osascript", "-e", f'tell application "Messages" to send "ERROR(song-logger): {e}" to buddy "{vars.IMESSAGE_USER}"'])
        print("reauthenticating")
        sp = authenticate()

    time.sleep(interval)
