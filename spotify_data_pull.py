import os
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

#load API and DB credentials from .env file
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:4004/"

#connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("host"),
    dbname=os.getenv("dbname"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    port=os.getenv("port")
)
cursor = conn.cursor()

#set up Spotify API authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-library-read user-read-private user-top-read"
))

#fetch and insert artists
def fetch_artists(tracks):
    for track in tracks:
        for artist in track['artists']:
            cursor.execute("""
                INSERT INTO artists (id, name, followers, genres, popularity)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (artist['id'], artist['name'], None, None, None))  # Some fields might not be available
    conn.commit()

#fetch and insert albums (AFTER artists exist)
def fetch_albums(tracks):
    for track in tracks:
        album = track['album']
        cursor.execute("""
            INSERT INTO albums (id, name, artist_id, release_date, total_tracks)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (album['id'], album['name'], track['artists'][0]['id'], album['release_date'], album['total_tracks']))
    conn.commit()

#fetch and insert tracks (AFTER albums exist)
def fetch_top_tracks():
    results = sp.current_user_top_tracks(limit=10)
    tracks = results['items']

    #step 1: Insert artists first
    fetch_artists(tracks)
    
    #step 2: Insert albums after artists exist
    fetch_albums(tracks)

    #step 3: Insert tracks after albums exist
    for track in tracks:
        cursor.execute("""
            INSERT INTO tracks (id, name, album_id, artist_id, popularity, duration_ms)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (track['id'], track['name'], track['album']['id'], track['artists'][0]['id'], track['popularity'], track['duration_ms']))
    conn.commit()

#fetch playlists
def fetch_playlists():
    results = sp.current_user_playlists(limit=10)
    for playlist in results['items']:
        cursor.execute("""
            INSERT INTO playlists (id, name, owner, total_tracks)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (playlist['id'], playlist['name'], playlist['owner']['display_name'], playlist['tracks']['total']))
    conn.commit()

#run functions
fetch_top_tracks()
fetch_playlists()

#close connection
cursor.close()
conn.close()
print("Data successfully inserted into PostgreSQL!")
