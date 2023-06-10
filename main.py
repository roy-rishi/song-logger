import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred


def raiseNetworkError():
    raise Exception("\033[91mERROR: Could not connect to Spotify. Device may be offline, or the network may be blocking this request")

def nowPlaying():
    nowPlaying = sp.current_playback()
    print(nowPlaying)


scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))

nowPlaying()
