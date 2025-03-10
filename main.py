import streamlit as st
import time
from spotify_client import (
    create_spotify_client, get_user_profile, get_top_tracks,
    get_top_artists, get_recent_tracks, get_audio_features
)
from analysis import (
    process_audio_features, analyze_mood, get_genre_distribution,
    calculate_listening_trends, cluster_tracks
)
from visualizations import (
    create_audio_features_radar, create_genre_bar_chart,
    create_listening_time_chart
)

# Page configuration
st.set_page_config(
    page_title="Spotify Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("🎵 Spotify Analytics Dashboard")
    
    # Initialize Spotify client
    try:
        sp = create_spotify_client()
    except Exception as e:
        st.error("Failed to initialize Spotify client. Please check your credentials.")
        st.stop()
    
    # Get user profile
    with st.spinner("Loading your profile..."):
        profile = get_user_profile(sp)
        if profile:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    profile['images'][0]['url'] if profile['images'] else None,
                    width=150
                )
                st.header(f"Welcome, {profile['display_name']}!")
    
    # Time range selector
    time_range = st.selectbox(
        "Select time range",
        options=[
            ("short_term", "Last 4 weeks"),
            ("medium_term", "Last 6 months"),
            ("long_term", "All time")
        ],
        format_func=lambda x: x[1]
    )[0]
    
    # Fetch data
    with st.spinner("Analyzing your music..."):
        top_tracks = get_top_tracks(sp, time_range)
        top_artists = get_top_artists(sp, time_range)
        recent_tracks = get_recent_tracks(sp)
        
        if top_tracks and top_artists and recent_tracks:
            track_ids = [track['id'] for track in top_tracks['items']]
            audio_features = get_audio_features(sp, track_ids)
            
            if audio_features:
                # Process data
                audio_features_df = process_audio_features(audio_features)
                mood_analysis = analyze_mood(audio_features_df)
                genres = get_genre_distribution(top_artists)
                listening_trends = calculate_listening_trends(recent_tracks)
                
                # Display insights
                st.header("🎯 Your Music Profile")
                st.write(mood_analysis)
                
                # Display statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Peak Listening Hour", f"{listening_trends['peak_hour']}:00")
                with col2:
                    st.metric("Tracks Analyzed", listening_trends['total_tracks'])
                with col3:
                    st.metric("Top Genre", genres[0][0].title() if genres else "N/A")
                
                # Visualizations
                st.header("📊 Music Analysis")
                
                # Audio features radar chart
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Audio Features")
                    st.plotly_chart(
                        create_audio_features_radar(audio_features_df),
                        use_container_width=True
                    )
                
                with col2:
                    st.subheader("Genre Distribution")
                    st.plotly_chart(
                        create_genre_bar_chart(genres),
                        use_container_width=True
                    )
                
                # Listening time chart
                st.subheader("Listening Pattern")
                st.plotly_chart(
                    create_listening_time_chart(recent_tracks),
                    use_container_width=True
                )
                
                # Top artists and tracks
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🎤 Top Artists")
                    for i, artist in enumerate(top_artists['items'][:5], 1):
                        st.write(f"{i}. {artist['name']}")
                
                with col2:
                    st.subheader("🎵 Top Tracks")
                    for i, track in enumerate(top_tracks['items'][:5], 1):
                        st.write(f"{i}. {track['name']} - {track['artists'][0]['name']}")

if __name__ == "__main__":
    main()
