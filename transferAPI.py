import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import time
from dotenv import load_dotenv

# Spotify API credentials
# Register Spotify API on: https://developer.spotify.com/dashboard

SPOTIFY_CLIENT_ID = secret['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = secret['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'
SPOTIFY_SCOPE = 'user-library-read'

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
))

# See https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html
ytmusic = YTMusic('browser.json')

# Retrieve liked songs 
def get_spotify_liked_songs():
    results = sp.current_user_saved_tracks(limit=50)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    liked_songs = []
    for item in tracks:
        track = item['track']
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        song = {
            'name': track['name'],
            'artists': artist_names
        }
        liked_songs.append(song)
    return liked_songs

# Add songs to YouTube Music liked songs
def add_songs_to_ytmusic_liked_songs(songs):
    for song in songs:
        query = f"{song['name']} {song['artists']}"
        search_results = ytmusic.search(query, filter='songs')
        
        if search_results:
            song_id = search_results[0]['videoId']
            ytmusic.rate_song(song_id, 'LIKE')
            print(f"Added to YouTube Music: {song['name']} by {song['artists']}")
        else:
            print(f"Song not found on YouTube Music: {song['name']} by {song['artists']}")
        
        time.sleep(1)  # 1-second delay between each request to prevent being throttled

def main():
    spotify_songs = get_spotify_liked_songs()
    print(f"Found {len(spotify_songs)} liked songs on Spotify.")
   
    print(f"Adding liked songs to YouTube Music...")
    add_songs_to_ytmusic_liked_songs(spotify_songs)
    
    print("Done!")


if __name__ == '__main__':
    main()
