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