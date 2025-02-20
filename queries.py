import psycopg2
from dotenv import load_dotenv
import os

#load API credentials from .env file
load_dotenv()

#connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("host"),
    dbname=os.getenv("dbname"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    port=os.getenv("port")
)
cursor = conn.cursor()

#1. Top 10 Most Listened-To Tracks
cursor.execute("""
    SELECT name, popularity
    FROM tracks
    ORDER BY popularity DESC
    LIMIT 10;
""")
top_tracks = cursor.fetchall()
print("\nTop 10 Most Listened-To Tracks:")
for track in top_tracks:
    print(track)

#2. Top 5 Albums (Based on Total Tracks)
cursor.execute("""
    SELECT name, total_tracks
    FROM albums
    ORDER BY total_tracks DESC
    LIMIT 5;
""")
top_albums = cursor.fetchall()
print("\nTop 5 Albums by Number of Tracks:")
for album in top_albums:
    print(album)

#3. Top 5 Most Popular Artists
cursor.execute("""
    SELECT name, popularity
    FROM artists
    ORDER BY popularity DESC NULLS LAST
    LIMIT 5;
""")
top_artists = cursor.fetchall()
print("\nTop 5 Most Popular Artists:")
for artist in top_artists:
    print(artist)

#4. Most Followed Artists
cursor.execute("""
    SELECT name, followers
    FROM artists
    ORDER BY followers DESC NULLS LAST
    LIMIT 5;
""")
most_followed_artists = cursor.fetchall()
print("\nTop 5 Most Followed Artists:")
for artist in most_followed_artists:
    print(artist)

#5. Top 5 Most Popular Tracks Per Artist
cursor.execute("""
    SELECT a.name AS artist_name, t.name AS track_name, t.popularity
    FROM tracks t
    JOIN artists a ON t.artist_id = a.id
    ORDER BY a.name, t.popularity DESC
    LIMIT 5;
""")
top_tracks_by_artist = cursor.fetchall()
print("\nTop 5 Most Popular Tracks Per Artist:")
for track in top_tracks_by_artist:
    print(track)

#6. Most Popular Albums (Based on Track Popularity) - No Decimals
cursor.execute("""
    SELECT a.name, CAST(AVG(t.popularity) AS INTEGER) AS avg_popularity
    FROM albums a
    JOIN tracks t ON a.id = t.album_id
    GROUP BY a.name
    ORDER BY avg_popularity DESC
    LIMIT 5;
""")
most_popular_albums = cursor.fetchall()
print("\nTop 5 Most Popular Albums:")
for album in most_popular_albums:
    print(album)

#7. Longest and Shortest Tracks
cursor.execute("""
    (SELECT name, duration_ms FROM tracks ORDER BY duration_ms DESC LIMIT 1)
    UNION
    (SELECT name, duration_ms FROM tracks ORDER BY duration_ms ASC LIMIT 1);
""")
longest_shortest_tracks = cursor.fetchall()
print("\nLongest and Shortest Tracks:")
for track in longest_shortest_tracks:
    print(track)

#8. Average Popularity of Tracks per Artist (No Decimals)
cursor.execute("""
    SELECT a.name, CAST(AVG(t.popularity) AS INTEGER) AS avg_popularity
    FROM artists a
    JOIN tracks t ON a.id = t.artist_id
    GROUP BY a.name
    ORDER BY avg_popularity DESC
    LIMIT 5;
""")
avg_popularity_per_artist = cursor.fetchall()
print("\nTop 5 Artists with Highest Average Track Popularity:")
for artist in avg_popularity_per_artist:
    print(artist)

#9. Most Popular Playlists (by Total Tracks)
cursor.execute("""
    SELECT name, total_tracks
    FROM playlists
    ORDER BY total_tracks DESC
    LIMIT 5;
""")
most_popular_playlists = cursor.fetchall()
print("\nTop 5 Playlists by Number of Tracks:")
for playlist in most_popular_playlists:
    print(playlist)

#close connection
cursor.close()
conn.close()
