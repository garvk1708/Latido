import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os

def get_redirect_uri():
    """Get the appropriate redirect URI based on the environment."""
    # For local development
    return "http://localhost:5000"

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

            # Display login page with styled button
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