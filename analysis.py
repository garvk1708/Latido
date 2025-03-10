import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter

def process_audio_features(audio_features):
    """Process audio features into a DataFrame."""
    features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness']
    df = pd.DataFrame(audio_features)[features]
    return df

def analyze_mood(audio_features_df):
    """Analyze mood based on audio features."""
    avg_valence = audio_features_df['valence'].mean()
    avg_energy = audio_features_df['energy'].mean()
    
    if avg_valence > 0.6 and avg_energy > 0.6:
        return "Your music taste is very upbeat and energetic!"
    elif avg_valence > 0.6 and avg_energy <= 0.6:
        return "You enjoy happy, relaxed music!"
    elif avg_valence <= 0.6 and avg_energy > 0.6:
        return "You tend to listen to intense, moody music!"
    else:
        return "Your music taste leans towards mellow, contemplative songs."

def cluster_tracks(audio_features_df):
    """Cluster tracks based on audio features."""
    kmeans = KMeans(n_clusters=4, random_state=42)
    features = ['danceability', 'energy', 'valence']
    clusters = kmeans.fit_predict(audio_features_df[features])
    return clusters

def get_genre_distribution(top_artists):
    """Get distribution of genres from top artists."""
    genres = []
    for artist in top_artists['items']:
        genres.extend(artist['genres'])
    return Counter(genres).most_common(10)

def calculate_listening_trends(recent_tracks):
    """Calculate listening trends from recent tracks."""
    df = pd.DataFrame([{
        'played_at': pd.to_datetime(track['played_at']),
        'track_name': track['track']['name']
    } for track in recent_tracks['items']])
    
    df['hour'] = df['played_at'].dt.hour
    hourly_distribution = df.groupby('hour').size()
    
    return {
        'peak_hour': hourly_distribution.idxmax(),
        'total_tracks': len(df)
    }
