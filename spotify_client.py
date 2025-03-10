import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_redirect_uri():
    """Get the appropriate redirect URI based on the environment."""
    # For local development with callback path
    return "http://0.0.0.0:5000/callback"

def create_spotify_client():
    """Create and return an authenticated Spotify client."""
    try:
        redirect_uri = get_redirect_uri()

        # Initialize OAuth Manager
        auth_manager = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=redirect_uri,
            scope="user-top-read user-read-recently-played user-library-read",
            show_dialog=True  # Force display of auth dialog
        )

        # Check if we need to start the auth flow
        if not st.session_state.get('token_info'):
            # Get the auth URL
            auth_url = auth_manager.get_authorize_url()

            # Display clean login page with styled button
            st.markdown(
                f"""
                <div style="text-align: center; padding: 2rem;">
                    <h2 style="color: #1DB954; margin-bottom: 1.5rem;">Welcome to Spotify Analytics!</h2>
                    <p style="margin-bottom: 2rem;">Connect your Spotify account to see your personalized music insights.</p>
                    <a href="{auth_url}" target="_self" 
                       style="background-color: #1DB954; 
                              color: white; 
                              padding: 12px 24px; 
                              border-radius: 24px; 
                              text-decoration: none; 
                              font-weight: bold;
                              transition: all 0.3s ease;
                              display: inline-block;">
                        Connect with Spotify
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()

        # Create and return Spotify client
        sp = spotipy.Spotify(auth_manager=auth_manager)
        sp.current_user()  # Test the connection
        return sp

    except Exception as e:
        if "invalid_grant" in str(e):
            # Clear the session state and redirect to login
            st.session_state.token_info = None
            st.experimental_rerun()
        raise Exception(f"Authentication failed: {str(e)}")

def get_user_profile(sp):
    """Get the user's Spotify profile."""
    try:
        return sp.current_user()
    except Exception as e:
        st.error(f"Error fetching user profile: {str(e)}")
        return None

def get_top_tracks(sp, time_range='medium_term', limit=20):
    """Get user's top tracks."""
    try:
        return sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
    except Exception as e:
        st.error(f"Error fetching top tracks: {str(e)}")
        return None

def get_top_artists(sp, time_range='medium_term', limit=20):
    """Get user's top artists."""
    try:
        return sp.current_user_top_artists(limit=limit, offset=0, time_range=time_range)
    except Exception as e:
        st.error(f"Error fetching top artists: {str(e)}")
        return None

def get_recent_tracks(sp, limit=50):
    """Get user's recently played tracks."""
    try:
        return sp.current_user_recently_played(limit=limit)
    except Exception as e:
        st.error(f"Error fetching recent tracks: {str(e)}")
        return None

def get_audio_features(sp, track_ids):
    """Get audio features for tracks."""
    try:
        return sp.audio_features(track_ids)
    except Exception as e:
        st.error(f"Error fetching audio features: {str(e)}")
        return None

def get_top_albums(sp, time_range='medium_term', limit=10):
    """Get user's top albums based on their top tracks."""
    try:
        top_tracks = sp.current_user_top_tracks(limit=limit*2, offset=0, time_range=time_range)
        
        # Extract unique albums from top tracks
        albums = {}
        for track in top_tracks['items']:
            album_id = track['album']['id']
            if album_id not in albums:
                albums[album_id] = track['album']
        
        # Convert to list and limit to requested number
        album_list = list(albums.values())[:limit]
        return {'items': album_list}
    except Exception as e:
        st.error(f"Error fetching top albums: {str(e)}")
        return None

import random
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_recommendations(sp, seed_tracks=None, seed_artists=None, limit=10, audio_features_df=None):
    """Get personalized track recommendations based on user's listening patterns."""
    try:
        # Prepare seed parameters
        params = {'limit': limit}
        
        if seed_tracks:
            params['seed_tracks'] = seed_tracks[:5]  # Maximum 5 seeds allowed
        
        if seed_artists and (not seed_tracks or len(seed_tracks) < 5):
            max_artists = 5 - (len(seed_tracks) if seed_tracks else 0)
            params['seed_artists'] = seed_artists[:max_artists]
        
        # Add audio feature parameters if available for more personalized recommendations
        if audio_features_df is not None:
            # Calculate averages of key audio features
            avg_danceability = audio_features_df['danceability'].mean()
            avg_energy = audio_features_df['energy'].mean()
            avg_valence = audio_features_df['valence'].mean()
            avg_tempo = audio_features_df['tempo'].mean()
            avg_acousticness = audio_features_df['acousticness'].mean()
            
            # Add target parameters based on user's preferences
            # We add slight variations to discover new but still relevant music
            params.update({
                'target_danceability': min(1.0, avg_danceability * random.uniform(0.85, 1.15)),
                'target_energy': min(1.0, avg_energy * random.uniform(0.85, 1.15)),
                'target_valence': min(1.0, avg_valence * random.uniform(0.85, 1.15)),
                'min_tempo': max(0, avg_tempo * 0.85),
                'max_tempo': avg_tempo * 1.15,
                'target_acousticness': min(1.0, avg_acousticness * random.uniform(0.85, 1.15))
            })
            
        # Get recommendations
        recommendations = sp.recommendations(**params)
        return recommendations
    except Exception as e:
        st.error(f"Error fetching recommendations: {str(e)}")
        return None

# This duplicate method is removed as it's already defined above

def get_user_profile(sp):
    """Get the user's Spotify profile."""
    try:
        return sp.current_user()
    except Exception as e:
        st.error(f"Error fetching user profile: {str(e)}")
        return None

def get_top_tracks(sp, time_range="medium_term"):
    """Get the user's top tracks."""
    try:
        return sp.current_user_top_tracks(
            limit=50,
            time_range=time_range
        )
    except Exception as e:
        st.error(f"Error fetching top tracks: {str(e)}")
        return None

def get_top_artists(sp, time_range="medium_term"):
    """Get the user's top artists."""
    try:
        return sp.current_user_top_artists(
            limit=50,
            time_range=time_range
        )
    except Exception as e:
        st.error(f"Error fetching top artists: {str(e)}")
        return None

def get_top_albums(sp, time_range="medium_term"):
    """Extract top albums from top tracks."""
    try:
        # Get top tracks first
        top_tracks = get_top_tracks(sp, time_range)
        if not top_tracks:
            return None
            
        # Extract album info from tracks
        albums = {}
        for track in top_tracks['items']:
            album = track['album']
            album_id = album['id']
            
            # Count album occurrences
            if album_id in albums:
                albums[album_id]['count'] += 1
            else:
                albums[album_id] = {
                    'album': album,
                    'count': 1
                }
        
        # Sort by count
        sorted_albums = sorted(albums.values(), key=lambda x: x['count'], reverse=True)
        
        # Format the response like a Spotify API response
        return {
            'items': [album['album'] for album in sorted_albums[:20]]
        }
    except Exception as e:
        st.error(f"Error processing top albums: {str(e)}")
        return None

def get_recent_tracks(sp):
    """Get the user's recently played tracks."""
    try:
        return sp.current_user_recently_played(limit=50)
    except Exception as e:
        st.error(f"Error fetching recent tracks: {str(e)}")
        return None

def get_audio_features(sp, track_ids):
    """Get audio features for a list of tracks."""
    try:
        if not track_ids:
            return None
            
        # Spotify API only allows 100 tracks per request
        audio_features = []
        
        # Process in batches of 100
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            batch_features = sp.audio_features(batch)
            if batch_features:
                audio_features.extend(batch_features)
        
        return audio_features
    except Exception as e:
        st.error(f"Error fetching audio features: {str(e)}")
        return None