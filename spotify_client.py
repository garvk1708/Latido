import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
import os

def get_redirect_uri():
    """Get the appropriate redirect URI based on the environment."""
    is_production = os.environ.get('VERCEL_ENV') == 'production'
    if is_production:
        # Use the Vercel deployment URL
        vercel_url = os.environ.get('VERCEL_URL')
        return f"https://{vercel_url}"
    return "http://localhost:5000"

def create_spotify_client():
    """Create and return an authenticated Spotify client."""
    # Cache the token info in Streamlit's session state
    if not hasattr(st.session_state, 'spotify_token_info'):
        st.session_state.spotify_token_info = None

    try:
        redirect_uri = get_redirect_uri()
        oauth_manager = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=redirect_uri,
            scope="user-top-read user-read-recently-played user-library-read",
            cache_handler=None  # Disable file caching
        )

        if st.session_state.spotify_token_info is None:
            auth_url = oauth_manager.get_authorize_url()
            st.markdown(
                f"""
                <div class="fade-in">
                    <h3>Welcome to Spotify Analytics!</h3>
                    <p>Please authenticate with Spotify to continue.</p>
                    <a href="{auth_url}" target="_self" 
                       style="background-color: #1DB954; color: white; padding: 10px 20px; 
                              border-radius: 20px; text-decoration: none; display: inline-block;
                              margin-top: 10px; font-weight: bold;">
                        Login with Spotify
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()

        sp = spotipy.Spotify(auth_manager=oauth_manager)
        # Test the connection
        sp.current_user()
        return sp

    except Exception as e:
        if "invalid_grant" in str(e):
            # Clear the session state and redirect to login
            st.session_state.spotify_token_info = None
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