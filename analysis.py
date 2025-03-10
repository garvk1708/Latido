import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from collections import Counter

def process_audio_features(audio_features):
    """Process audio features into a DataFrame with advanced feature extraction."""
    features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 
                'instrumentalness', 'liveness', 'speechiness']
    df = pd.DataFrame(audio_features)[features]
    return df

def analyze_mood(audio_features_df):
    """Advanced mood analysis using ML clustering and emotional valence."""
    # Standardize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(audio_features_df)

    # Perform PCA for dimension reduction
    pca = PCA(n_components=2)
    features_pca = pca.fit_transform(features_scaled)

    # Cluster the tracks
    kmeans = KMeans(n_clusters=4, random_state=42)
    clusters = kmeans.fit_predict(features_pca)

    # Calculate cluster centers and mood characteristics
    cluster_centers = kmeans.cluster_centers_

    # Analyze emotional characteristics
    avg_valence = audio_features_df['valence'].mean()
    avg_energy = audio_features_df['energy'].mean()
    avg_danceability = audio_features_df['danceability'].mean()

    # Determine dominant mood patterns
    mood_patterns = []
    if avg_valence > 0.6 and avg_energy > 0.6:
        mood_patterns.append("Euphoric & Energetic")
    if avg_valence > 0.6 and avg_danceability > 0.6:
        mood_patterns.append("Upbeat & Dancing")
    if avg_valence < 0.4 and avg_energy > 0.6:
        mood_patterns.append("Intense & Emotional")
    if avg_valence < 0.4 and avg_energy < 0.4:
        mood_patterns.append("Melancholic & Reflective")

    # Calculate mood diversity score
    mood_diversity = np.std(features_scaled, axis=0).mean()

    return {
        'primary_mood': mood_patterns[0] if mood_patterns else "Balanced & Neutral",
        'mood_patterns': mood_patterns,
        'mood_diversity_score': round(mood_diversity * 100, 2),
        'cluster_distribution': Counter(clusters),
        'emotional_stats': {
            'valence': avg_valence,
            'energy': avg_energy,
            'danceability': avg_danceability
        }
    }

def analyze_music_patterns(audio_features_df):
    """Analyze complex music patterns and characteristics."""
    # Calculate temporal patterns
    tempo_patterns = {
        'avg_tempo': audio_features_df['tempo'].mean(),
        'tempo_variation': audio_features_df['tempo'].std(),
        'tempo_range': audio_features_df['tempo'].max() - audio_features_df['tempo'].min()
    }

    # Analyze acoustic vs electronic balance
    acoustic_electronic_ratio = (
        audio_features_df['acousticness'].mean() / 
        (1 - audio_features_df['instrumentalness'].mean())
    )

    return {
        'tempo_patterns': tempo_patterns,
        'acoustic_electronic_ratio': round(acoustic_electronic_ratio, 2),
        'complexity_score': round(
            (audio_features_df['instrumentalness'].mean() + 
             audio_features_df['speechiness'].std()) * 100, 
            2
        )
    }

def get_genre_distribution(top_artists):
    """Analyze genre distribution from top artists."""
    # Extract all genres
    all_genres = []
    for artist in top_artists['items']:
        all_genres.extend(artist['genres'])

    # Count genre occurrences
    genre_counts = {}
    for genre in all_genres:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    # Sort by count
    sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

    # Return top 8 genres in format compatible with visualization
    main_genres = []
    for genre, count in sorted_genres[:8]:
        main_genres.append(('Genre', genre, count))

    # Return as a list for direct use in visualization
    return [(genre, count) for genre, count in sorted_genres[:8]]


def calculate_listening_trends(recent_tracks):
    """Calculate detailed listening trends and patterns."""
    df = pd.DataFrame([{
        'played_at': pd.to_datetime(track['played_at']),
        'track_name': track['track']['name'],
        'artist_name': track['track']['artists'][0]['name']
    } for track in recent_tracks['items']])

    df['hour'] = df['played_at'].dt.hour
    df['day'] = df['played_at'].dt.day_name()

    hourly_distribution = df.groupby('hour').size()
    daily_distribution = df.groupby('day').size()

    # Calculate listening sessions
    df['time_diff'] = df['played_at'].diff()
    session_threshold = pd.Timedelta(hours=2)
    df['new_session'] = df['time_diff'] > session_threshold
    session_counts = df['new_session'].sum()

    return {
        'peak_hour': hourly_distribution.idxmax(),
        'peak_day': daily_distribution.idxmax(),
        'total_tracks': len(df),
        'unique_artists': df['artist_name'].nunique(),
        'listening_sessions': session_counts,
        'avg_session_length': round(len(df) / max(session_counts, 1), 1)
    }

def cluster_tracks(audio_features_df):
    """Cluster tracks based on audio features."""
    kmeans = KMeans(n_clusters=4, random_state=42)
    features = ['danceability', 'energy', 'valence']
    clusters = kmeans.fit_predict(audio_features_df[features])
    return clusters