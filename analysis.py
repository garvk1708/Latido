
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import datetime
import collections
import random

def analyze_taste_profile(audio_features_df, genres, top_artists):
    """Generate personalized taste profile and insights based on audio features and genres."""
    # Initialize result dictionary
    profile = {
        'insights': [],
        'personality_traits': []
    }
    
    # Skip if no data
    if audio_features_df.empty or not genres:
        return profile
    
    # Extract mean values for key features
    mean_danceability = audio_features_df['danceability'].mean()
    mean_energy = audio_features_df['energy'].mean()
    mean_valence = audio_features_df['valence'].mean()
    mean_tempo = audio_features_df['tempo'].mean()
    mean_acousticness = audio_features_df['acousticness'].mean()
    
    # Generate insights based on audio features
    # Danceability insights
    if mean_danceability > 0.7:
        profile['insights'].append("You gravitate toward rhythmic, danceable music that keeps you moving.")
        profile['personality_traits'].append("Dance Enthusiast")
    elif mean_danceability < 0.4:
        profile['insights'].append("You prefer music with complex, less predictable rhythmic structures.")
        profile['personality_traits'].append("Rhythm Explorer")
    
    # Energy insights
    if mean_energy > 0.7:
        profile['insights'].append("High-energy tracks dominate your playlist, suggesting you use music for motivation.")
        profile['personality_traits'].append("Energy Seeker")
    elif mean_energy < 0.4:
        profile['insights'].append("You tend to enjoy more relaxed, calming music that creates atmosphere.")
        profile['personality_traits'].append("Ambience Lover")
    
    # Mood (valence) insights
    if mean_valence > 0.7:
        profile['insights'].append("Your music choices reflect a preference for uplifting, positive sounds.")
        profile['personality_traits'].append("Positivity Seeker")
    elif mean_valence < 0.4:
        profile['insights'].append("You're drawn to more melancholic, reflective, and emotionally complex music.")
        profile['personality_traits'].append("Emotional Depth Explorer")
    
    # Tempo insights
    if mean_tempo > 120:
        profile['insights'].append("Fast-paced music features prominently in your listening habits.")
    elif mean_tempo < 90:
        profile['insights'].append("You tend to enjoy music with a more leisurely, relaxed pace.")
    
    # Acousticness insights
    if mean_acousticness > 0.6:
        profile['insights'].append("Acoustic elements and organic instruments resonate strongly with you.")
        profile['personality_traits'].append("Acoustic Enthusiast")
    elif mean_acousticness < 0.3:
        profile['insights'].append("You prefer contemporary production with electronic and processed sounds.")
        profile['personality_traits'].append("Production Enthusiast")
    
    # Genre insights
    top_genres = [g[0] for g in genres[:3]] if genres else []
    if top_genres:
        profile['insights'].append(f"Your top genres ({', '.join(top_genres)}) reveal a taste for {random.choice(['diverse', 'distinctive', 'characteristic'])} musical styles.")
    
    # Shuffle insights to create variety
    random.shuffle(profile['insights'])
    
    return profile

def process_audio_features(audio_features):
    """Process the audio features data and convert to a DataFrame."""
    try:
        if not audio_features:
            # Return a dummy dataframe with default values if no data
            return pd.DataFrame({
                'danceability': [0.5], 'energy': [0.5], 'key': [0], 
                'loudness': [-10], 'speechiness': [0.1], 'acousticness': [0.5],
                'instrumentalness': [0.1], 'liveness': [0.1], 'valence': [0.5],
                'tempo': [120], 'duration_ms': [200000]
            })
        
        # Clean None values
        audio_features = [af for af in audio_features if af is not None]
        
        # Create DataFrame
        df = pd.DataFrame(audio_features)
        
        # Fill any missing values
        df = df.fillna({
            'danceability': 0.5, 'energy': 0.5, 'key': 0, 
            'loudness': -10, 'speechiness': 0.1, 'acousticness': 0.5,
            'instrumentalness': 0.1, 'liveness': 0.1, 'valence': 0.5,
            'tempo': 120, 'duration_ms': 200000
        })
        
        return df
    except Exception as e:
        # Return a dummy dataframe with default values if error
        return pd.DataFrame({
            'danceability': [0.5], 'energy': [0.5], 'key': [0], 
            'loudness': [-10], 'speechiness': [0.1], 'acousticness': [0.5],
            'instrumentalness': [0.1], 'liveness': [0.1], 'valence': [0.5],
            'tempo': [120], 'duration_ms': [200000]
        })

def analyze_mood(audio_features_df):
    """Analyze mood based on audio features."""
    try:
        # Calculate mood metrics
        valence = audio_features_df['valence'].mean()
        energy = audio_features_df['energy'].mean()
        danceability = audio_features_df['danceability'].mean()
        
        # Determine mood diversity
        mood_diversity_score = round(
            (audio_features_df['valence'].std() + 
             audio_features_df['energy'].std()) * 100, 
            2
        )
        
        return {
            'primary_mood': get_mood_label(valence, energy),
            'emotional_stats': {
                'valence': round(valence, 2),
                'energy': round(energy, 2),
                'danceability': round(danceability, 2)
            },
            'mood_diversity_score': mood_diversity_score
        }
    except Exception as e:
        # Return default values if error
        return {
            'primary_mood': 'Balanced',
            'emotional_stats': {
                'valence': 0.5,
                'energy': 0.5,
                'danceability': 0.5
            },
            'mood_diversity_score': 50
        }

def get_mood_label(valence, energy):
    """Get mood label based on valence and energy."""
    if valence > 0.6 and energy > 0.6:
        return "Euphoric"
    elif valence > 0.6 and energy < 0.4:
        return "Peaceful"
    elif valence < 0.4 and energy > 0.6:
        return "Angry/Tense"
    elif valence < 0.4 and energy < 0.4:
        return "Sad/Depressive"
    else:
        return "Balanced"

def get_genre_distribution(top_artists):
    """Get genre distribution from top artists."""
    try:
        if not top_artists or 'items' not in top_artists:
            # Return default genres if no data
            return [("Pop", 5), ("Rock", 4), ("Hip-Hop", 3), 
                   ("Electronic", 2), ("Jazz", 1)]
        
        # Extract all genres
        all_genres = []
        for artist in top_artists['items']:
            if 'genres' in artist:
                all_genres.extend(artist['genres'])
        
        # Count genre occurrences
        genre_counts = collections.Counter(all_genres)
        
        # Convert to list of tuples (genre, count)
        genres = [(genre, count) for genre, count in genre_counts.most_common()]
        
        return genres
    except Exception as e:
        # Return default genres if error
        return [("Pop", 5), ("Rock", 4), ("Hip-Hop", 3), 
               ("Electronic", 2), ("Jazz", 1)]

def calculate_listening_trends(recent_tracks):
    """Calculate listening trends from recent tracks."""
    try:
        if not recent_tracks or 'items' not in recent_tracks:
            # Return default values if no data
            return {
                'peak_hour': 20,
                'listening_sessions': 15,
                'favorite_day': 'Saturday'
            }
        
        # Extract timestamps
        timestamps = [item['played_at'] for item in recent_tracks['items']]
        
        # Convert timestamps to datetime objects
        datetimes = [datetime.fromisoformat(ts.replace('Z', '+00:00')) 
                     if 'Z' in ts else datetime.fromisoformat(ts) 
                     for ts in timestamps]
        
        # Extract hour of day and day of week
        hours = [dt.hour for dt in datetimes]
        days = [dt.strftime('%A') for dt in datetimes]
        
        # Find peak hour
        hour_counts = collections.Counter(hours)
        peak_hour = hour_counts.most_common(1)[0][0]
        
        # Find favorite day
        day_counts = collections.Counter(days)
        favorite_day = day_counts.most_common(1)[0][0]
        
        # Estimate listening sessions (simplistic)
        listening_sessions = len(recent_tracks['items'])
        
        return {
            'peak_hour': peak_hour,
            'listening_sessions': listening_sessions,
            'favorite_day': favorite_day
        }
    except Exception as e:
        # Return default values if error
        return {
            'peak_hour': 20,
            'listening_sessions': 15,
            'favorite_day': 'Saturday'
        }

def analyze_music_patterns(audio_features_df):
    """Analyze complex music patterns and characteristics."""
    try:
        # Calculate temporal patterns
        tempo_patterns = {
            'avg_tempo': audio_features_df['tempo'].mean(),
            'tempo_variation': audio_features_df['tempo'].std(),
            'tempo_range': audio_features_df['tempo'].max() - audio_features_df['tempo'].min()
        }
        
        # Analyze acoustic vs electronic balance
        acoustic_electronic_ratio = (
            audio_features_df['acousticness'].mean() / 
            max(0.01, 1 - audio_features_df['instrumentalness'].mean())  # Avoid division by zero
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
    except Exception as e:
        # Return default values if error
        return {
            'tempo_patterns': {
                'avg_tempo': 120,
                'tempo_variation': 10,
                'tempo_range': 40
            },
            'acoustic_electronic_ratio': 1.5,
            'complexity_score': 50
        }

def analyze_taste_profile(audio_features_df, top_genres, top_artists):
    """Generate detailed analysis of user's taste profile with specific comments."""
    try:
        # Analyze key characteristics
        avg_danceability = audio_features_df['danceability'].mean()
        avg_energy = audio_features_df['energy'].mean()
        avg_valence = audio_features_df['valence'].mean()
        avg_acousticness = audio_features_df['acousticness'].mean()
        avg_instrumentalness = audio_features_df['instrumentalness'].mean()
        
        # Generate insights based on these values
        insights = []
        
        # Danceability insights
        if avg_danceability > 0.7:
            insights.append("You gravitate toward rhythmic, danceable music that moves you physically.")
        elif avg_danceability < 0.4:
            insights.append("You prefer music with less emphasis on steady rhythm and more on artistic expression.")
        
        # Energy insights
        if avg_energy > 0.7:
            insights.append("High-energy, intense tracks dominate your listening habits.")
        elif avg_energy < 0.4:
            insights.append("You appreciate more mellow, relaxed musical experiences.")
        
        # Mood insights from valence
        if avg_valence > 0.7:
            insights.append("Your music choices reflect a positive, upbeat emotional preference.")
        elif avg_valence < 0.4:
            insights.append("Your playlist often explores deeper, sometimes melancholic emotional territories.")
        
        # Acoustic vs. electronic preferences
        if avg_acousticness > 0.6:
            insights.append("You have a strong preference for organic, acoustic sounds over electronic production.")
        elif avg_acousticness < 0.3:
            insights.append("Modern electronic production elements feature heavily in your favorite music.")
        
        # Vocals vs. instrumental
        if avg_instrumentalness > 0.5:
            insights.append("You appreciate instrumental compositions where melody speaks without lyrics.")
        
        # Genre insights
        if top_genres and len(top_genres) > 0:
            top_genre = top_genres[0][0] if isinstance(top_genres[0], tuple) else top_genres[0]
            insights.append(f"Your passion for {top_genre} stands out in your listening patterns.")
            
            # Genre diversity
            if len(top_genres) > 5:
                insights.append("You're a musical explorer, enjoying diverse genres rather than staying in one lane.")
        
        # Artist loyalty
        if top_artists and 'items' in top_artists and len(top_artists['items']) > 0:
            artist_count = len(top_artists['items'])
            if artist_count > 15:
                insights.append("You enjoy discovering many different artists rather than focusing on a few favorites.")
            elif artist_count < 8:
                insights.append("You show strong loyalty to a core group of favorite artists.")
        
        # Overall listening personality
        personality_traits = []
        if avg_danceability > 0.6 and avg_energy > 0.6:
            personality_traits.append("The Life of the Party")
        if avg_valence < 0.4 and avg_energy < 0.5:
            personality_traits.append("The Deep Thinker")
        if avg_acousticness > 0.6:
            personality_traits.append("The Traditionalist")
        if avg_danceability > 0.6 and avg_valence > 0.6:
            personality_traits.append("The Optimist")
        if avg_instrumentalness > 0.5:
            personality_traits.append("The Purist")
            
        # Default trait if none assigned
        if not personality_traits:
            personality_traits.append("The Balanced Listener")
            
        return {
            'insights': insights,
            'personality_traits': personality_traits
        }
    except Exception as e:
        # Return default values if error occurs
        return {
            'insights': ["You have an eclectic taste spanning various moods and styles."],
            'personality_traits': ["The Balanced Listener"]
        }

def cluster_tracks(audio_features_df):
    """Use K-means clustering to group tracks by audio features."""
    try:
        # Select features for clustering
        features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
        X = audio_features_df[features].values
        
        # Determine optimal number of clusters (simplified)
        n_clusters = min(3, len(X))
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X)
        
        # Get cluster centers
        centers = kmeans.cluster_centers_
        
        # Assign mood labels to clusters
        cluster_moods = []
        for center in centers:
            # Unpack center values based on the order of features
            dance, energy, valence, acoustic, instrument = center
            
            # Determine mood based on valence and energy
            mood = get_mood_label(valence, energy)
            
            # Add additional characteristics
            characteristics = []
            if dance > 0.7:
                characteristics.append("Danceable")
            if acoustic > 0.6:
                characteristics.append("Acoustic")
            elif instrument > 0.6:
                characteristics.append("Instrumental")
            
            cluster_moods.append({
                'mood': mood,
                'characteristics': characteristics
            })
        
        # Count tracks in each cluster
        cluster_counts = collections.Counter(clusters)
        
        result = []
        for i in range(n_clusters):
            if i in cluster_counts:
                result.append({
                    'cluster_id': i,
                    'count': cluster_counts[i],
                    'percentage': round((cluster_counts[i] / len(clusters)) * 100, 1),
                    'mood': cluster_moods[i]['mood'],
                    'characteristics': cluster_moods[i]['characteristics']
                })
        
        return result
    except Exception as e:
        # Return default values if error
        return [
            {
                'cluster_id': 0,
                'count': 5,
                'percentage': 50,
                'mood': 'Balanced',
                'characteristics': ['Danceable']
            },
            {
                'cluster_id': 1,
                'count': 5,
                'percentage': 50,
                'mood': 'Peaceful',
                'characteristics': ['Acoustic']
            }
        ]
