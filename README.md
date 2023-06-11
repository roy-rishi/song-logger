# song-logger
 Log songs playing on Spotify

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
`python main.py`
