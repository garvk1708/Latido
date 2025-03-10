import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_simulated_profile():
    """Generate a simulated user profile."""
    return {
        'display_name': 'Demo User',
        'images': [{
            'url': 'https://picsum.photos/200'
        }],
        'followers': {'total': random.randint(50, 500)},
        'country': 'US'
    }

def generate_track(index):
    """Generate a simulated track."""
    genres = ['Pop', 'Rock', 'Hip-Hop', 'Electronic', 'Jazz', 'Classical']
    artists = ['The Digital Dreams', 'Electronic Echo', 'Midnight Pulse', 
              'Neon Wave', 'Cyber Symphony', 'Virtual Voltage']

    return {
        'id': f'track_{index}',
        'name': f'Simulated Track {index}',
        'artists': [{
            'name': random.choice(artists),
            'genres': [random.choice(genres)]
        }],
        'album': {
            'images': [{
                'url': f'https://picsum.photos/seed/{index}/300'
            }]
        },
        'popularity': random.randint(30, 100)
    }

import random
from datetime import datetime, timedelta

def generate_audio_features():
    """Generate simulated audio features."""
    return {
        'danceability': random.uniform(0.3, 0.9),
        'energy': random.uniform(0.4, 0.95),
        'valence': random.uniform(0.2, 0.8),
        'tempo': random.uniform(70, 180),
        'acousticness': random.uniform(0.1, 0.9),
        'instrumentalness': random.uniform(0, 0.8),
        'liveness': random.uniform(0.1, 0.8),
        'speechiness': random.uniform(0.03, 0.6)
    }

def generate_track(idx=None):
    """Generate a simulated track."""
    # Sample artist names
    artist_names = ["The Heartbeats", "Rhythm Pulse", "Sonic Wave", "Electric Echo", 
                    "Melody Flow", "Beat Makers", "Sound Craft", "Tune Creators",
                    "Harmonic Blend", "Audio Architects", "Frequency Shapers"]
    
    # Sample track names
    track_names = ["Heartbeat", "Pulse", "Rhythm of Life", "Electric Dreams", 
                   "Sonic Journey", "Melodic Path", "Harmonic Waves", "Frequency",
                   "Ambient Flow", "Digital Soul", "Analog Heart", "Resonance"]
    
    # Sample album names
    album_names = ["Vibrations", "Waveforms", "Resonance", "Spectrum", 
                   "Amplitude", "Harmony", "Frequency", "Soundscapes",
                   "Pulse", "Rhythm Section", "Beat Patterns"]
    
    # Generate random artist and track details
    artist_name = random.choice(artist_names)
    track_name = random.choice(track_names)
    if random.random() < 0.3:  # Sometimes add a descriptor
        track_name += f" {random.choice(['Mix', 'Edit', 'Version', 'Remix', 'Reprise'])}"
    
    album_name = random.choice(album_names)
    
    # Generate a random ID if not provided
    if idx is None:
        idx = random.randint(100000, 999999)
    
    # Generate random durations
    duration_ms = random.randint(180000, 360000)  # 3-6 minutes
    
    # Generate track object
    track = {
        'id': f'track_{idx}',
        'name': track_name,
        'duration_ms': duration_ms,
        'popularity': random.randint(30, 95),
        'artists': [
            {
                'id': f'artist_{idx}',
                'name': artist_name
            }
        ],
        'album': {
            'id': f'album_{idx}',
            'name': album_name,
            'images': [
                {
                    'url': f'https://picsum.photos/seed/{idx}/300',
                    'height': 300,
                    'width': 300
                }
            ]
        }
    }
    
    return track

def generate_recent_tracks(count=50):
    """Generate simulated recent tracks with timestamps."""
    now = datetime.now()
    tracks = []

    for i in range(count):
        track_time = now - timedelta(hours=random.randint(1, 168))
        track = generate_track(i)
        tracks.append({
            'track': track,
            'played_at': track_time.isoformat()
        })

    return {'items': sorted(tracks, key=lambda x: x['played_at'], reverse=True)}

def generate_artists(count=20):
    """Generate simulated artists."""
    # Sample artist names and genres
    artist_names = ["The Heartbeats", "Rhythm Pulse", "Sonic Wave", "Electric Echo", 
                    "Melody Flow", "Beat Makers", "Sound Craft", "Tune Creators",
                    "Harmonic Blend", "Audio Architects", "Frequency Shapers",
                    "The Soundscapers", "Waveform Collective", "Sonic Architects",
                    "Pulse Theory", "Amplitude", "The Resonators", "Echo Chamber",
                    "Digital Ensemble", "Analog Collective", "Beat Scientists"]
    
    genres = ["pop", "rock", "electronic", "indie", "hip-hop", "r&b", "jazz", 
              "classical", "ambient", "folk", "metal", "soul", "blues", "lo-fi",
              "experimental", "chill", "edm", "synthwave", "house", "techno"]
    
    artists = []
    for i in range(count):
        # Assign 1-3 random genres
        artist_genres = random.sample(genres, random.randint(1, 3))
        
        # Create artist object
        artist = {
            'id': f'artist_{i}',
            'name': artist_names[i % len(artist_names)],  # Cycle through names if we run out
            'popularity': random.randint(30, 95),
            'genres': artist_genres,
            'images': [
                {
                    'url': f'https://picsum.photos/seed/artist_{i}/300',
                    'height': 300,
                    'width': 300
                }
            ],
            'followers': {
                'total': random.randint(1000, 1000000)
            }
        }
        
        artists.append(artist)
    
    return {'items': artists}

def generate_albums(count=15):
    """Generate simulated albums."""
    # Sample album names
    album_names = ["Vibrations", "Waveforms", "Resonance", "Spectrum", 
                   "Amplitude", "Harmony", "Frequency", "Soundscapes",
                   "Pulse", "Rhythm Section", "Beat Patterns", "Echo Chamber",
                   "Digital Dreams", "Analog Heart", "Sonic Landscapes"]
    
    # Sample artist names
    artist_names = ["The Heartbeats", "Rhythm Pulse", "Sonic Wave", "Electric Echo", 
                    "Melody Flow", "Beat Makers", "Sound Craft", "Tune Creators"]
    
    albums = []
    for i in range(count):
        # Create album object
        album = {
            'id': f'album_{i}',
            'name': album_names[i % len(album_names)],  # Cycle through names if we run out
            'release_date': f"2022-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'total_tracks': random.randint(8, 16),
            'artists': [
                {
                    'id': f'artist_{i}',
                    'name': artist_names[i % len(artist_names)]
                }
            ],
            'images': [
                {
                    'url': f'https://picsum.photos/seed/album_{i}/300',
                    'height': 300,
                    'width': 300
                }
            ]
        }
        
        albums.append(album)
    
    return {'items': albums}

def generate_tracks(count=30):
    """Generate simulated tracks for top tracks."""
    tracks = []
    
    for i in range(count):
        track = generate_track(i)
        tracks.append(track)
    
    return {'items': tracks}

def get_simulated_data(time_range="medium_term"):
    """Get a complete set of simulated data for the Latido dashboard."""
    # Generate profile data
    profile = {
        'display_name': random.choice(["Alex", "Sam", "Jordan", "Taylor", "Casey"]),
        'id': 'user_12345',
        'images': [{
            'url': 'https://picsum.photos/seed/user/300',
            'height': 300,
            'width': 300
        }],
        'followers': {
            'total': random.randint(10, 500)
        }
    }
    
    # Generate tracks, artists and albums
    top_tracks = generate_tracks(30)
    top_artists = generate_artists(20)
    top_albums = generate_albums(15)
    recent_tracks = generate_recent_tracks(50)
    
    # Generate audio features for top tracks
    audio_features = []
    for track in top_tracks['items']:
        features = generate_audio_features()
        features['id'] = track['id']
        audio_features.append(features)
    
    # Generate recommendations
    recommendations = {
        'tracks': generate_tracks(10)['items']
    }
    
    return {
        'profile': profile,
        'top_tracks': top_tracks,
        'top_artists': top_artists,
        'top_albums': top_albums,
        'recent_tracks': recent_tracks,
        'audio_features': audio_features,
        'recommendations': recommendations
    }

def generate_artist(index):
    """Generate a simulated artist with genres."""
    genres = ['Pop', 'Rock', 'Hip-Hop', 'Electronic', 'Jazz', 'Classical',
              'Indie', 'Folk', 'R&B', 'Metal', 'Ambient', 'Blues']
    sub_genres = ['Synthwave', 'Dream Pop', 'Alternative', 'Neo-Soul', 
                 'Post-Rock', 'Trip-Hop', 'Lo-Fi', 'Future Bass']

    return {
        'id': f'artist_{index}',
        'name': f'Artist {index}',
        'genres': [random.choice(genres)] + random.sample(sub_genres, k=2),
        'images': [{
            'url': f'https://picsum.photos/seed/artist_{index}/300'
        }],
        'popularity': random.randint(30, 100)
    }

def generate_album(index):
    """Generate a simulated album."""
    album_types = ['Album', 'EP', 'Single', 'Compilation']
    album_names = ['Neon Dreams', 'Digital Horizons', 'Quantum Pulse', 
                  'Synthetic Memories', 'Virtual Reality', 'Electric Forest']

    return {
        'id': f'album_{index}',
        'name': f'{random.choice(album_names)} {index}',
        'album_type': random.choice(album_types),
        'release_date': f"202{random.randint(0, 3)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
        'total_tracks': random.randint(5, 15),
        'images': [{
            'url': f'https://picsum.photos/seed/album_{index}/300'
        }],
        'artists': [{
            'name': f'Artist {random.randint(1, 10)}'
        }]
    }

def get_simulated_data(time_range='medium_term'):
    """Get all simulated data for the application."""
    track_count = 20
    artist_count = 20
    album_count = 10

    tracks = [generate_track(i) for i in range(track_count)]
    artists = [generate_artist(i) for i in range(artist_count)]
    albums = [generate_album(i) for i in range(album_count)]
    audio_features = [generate_audio_features() for _ in range(track_count)]
    profile = generate_simulated_profile()
    top_tracks = {'items': tracks}
    top_artists = {'items': artists}
    top_albums = {'items': albums}
    recent_tracks = generate_recent_tracks()

    # Generate simulated recommendations
    recommendations = {
        'tracks': [
            generate_track(i) 
            for i in range(10)
        ]
    }

    return {
        'profile': profile,
        'top_tracks': top_tracks,
        'top_artists': top_artists,
        'top_albums': top_albums,
        'recent_tracks': recent_tracks,
        'audio_features': audio_features,
        'recommendations': recommendations
    }