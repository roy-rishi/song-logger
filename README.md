# song-logger
 Log songs playing on Spotify
 These logs can be processed with [https://github.com/roy-rishi/spotify-data-processor](roy-rishi/spotify-data-processor), or any other utility

## set-up
write the following to [vars.py](./vars.py)
```py
CLIENT_ID=""
CLIENT_SECRET=""
REDIRECT_URL="http://localhost:5173/callback"

DATA_PATH="data/streaming-history-2022-23-all.json"
```

## dependencies
`pip install spotipy==2.23.0`

## usage
the program with append logs to either files downloaded from [https://www.spotify.com/us/account/privacy/](Spotify's Extended streaming history), or the  template in [/data](/.data)
`python main.py`
