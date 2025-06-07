from flask import Flask, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to your Personal Spotify Data API!"})

@app.route('/top-tracks')
def top_tracks():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read"
    ))

    results = sp.current_user_top_tracks(limit=10, time_range='short_term')

    tracks = []
    for item in results['items']:
        tracks.append({
            "name": item['name'],
            "artist": item['artists'][0]['name'],
            "album": item['album']['name'],
            "url": item['external_urls']['spotify']
        })

    return jsonify(tracks)

@app.route('/top-artists')
def top_artists():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-top-read"
    ))

    results = sp.current_user_top_artists(limit=10, time_range='short_term')

    artists = []
    for item in results['items']:
        artists.append({
            "name": item['name'],
            "genres": item['genres'],
            "url": item['external_urls']['spotify']
        })

    return jsonify(artists)

@app.route('/recently-played')
def recently_played():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-recently-played"
    ))

    results = sp.current_user_recently_played(limit=10)

    songs = []
    for item in results['items']:
        track = item['track']
        songs.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name'],
            "played_at": item['played_at'],
            "url": track['external_urls']['spotify']
        })

    return jsonify(songs)

@app.route('/profile')
def profile():
    sp = Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-read-private user-read-email"
    ))

    user_info = sp.current_user()

    profile = {
        "name": user_info['display_name'],
        "email": user_info['email'] if 'email' in user_info else 'Not available',
        "country": user_info['country'],
        "profile_url": user_info['external_urls']['spotify']
    }

    return jsonify(profile)

if __name__ == '__main__':
    app.run(debug=True)
