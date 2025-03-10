import streamlit as st
import time
from spotify_client import (
    create_spotify_client, get_user_profile, get_top_tracks,
    get_top_artists, get_recent_tracks, get_audio_features
)
from analysis import (
    process_audio_features, analyze_mood, get_genre_distribution,
    calculate_listening_trends, analyze_music_patterns
)
from visualizations import (
    create_audio_features_radar, create_genre_bar_chart,
    create_listening_time_chart
)
from simulation import get_simulated_data

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

def create_hero_section():
    """Create an animated hero section."""
    st.markdown('''
        <div class="hero-section">
            <h1 style="font-size: 3.5rem; margin-bottom: 1.5rem;">
                <span class="gradient-text">Spotify Analytics</span>
            </h1>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; color: #888;">
                Discover your music personality through AI-powered insights
            </p>
        </div>
    ''', unsafe_allow_html=True)

def display_track_item(track, index):
    """Display a track with album art and hover effects."""
    st.markdown(f'''
        <div class="track-item">
            <div class="track-number">{index}</div>
            <img src="{track['album']['images'][0]['url']}" 
                 class="track-image" alt="{track['name']}">
            <div class="track-info">
                <div class="track-name">{track['name']}</div>
                <div class="track-artist">{track['artists'][0]['name']}</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

def main():
    create_hero_section()

    # Simulation mode toggle
    use_simulation = st.sidebar.checkbox("Use Demo Mode", value=True, 
                                       help="Try the dashboard with simulated data")

    if use_simulation:
        # Use simulated data
        data = get_simulated_data()
        profile = data['profile']
        top_tracks = data['top_tracks']
        top_artists = data['top_artists']
        recent_tracks = data['recent_tracks']
        audio_features = data['audio_features']
    else:
        # Initialize Spotify client and get real data
        try:
            sp = create_spotify_client()
            profile = get_user_profile(sp)
            time_range = st.sidebar.selectbox(
                "📅 Select time range",
                options=[
                    ("short_term", "Last 4 weeks"),
                    ("medium_term", "Last 6 months"),
                    ("long_term", "All time")
                ],
                format_func=lambda x: x[1]
            )[0]

            with st.spinner("🎼 Analyzing your music..."):
                top_tracks = get_top_tracks(sp, time_range)
                top_artists = get_top_artists(sp, time_range)
                recent_tracks = get_recent_tracks(sp)

                if all([top_tracks, top_artists, recent_tracks]):
                    track_ids = [track['id'] for track in top_tracks['items']]
                    audio_features = get_audio_features(sp, track_ids)
                else:
                    st.error("Failed to fetch your music data.")
                    st.stop()
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            st.stop()

    # Process and display data
    if profile and audio_features:
        st.markdown('<div class="scroll-fade">', unsafe_allow_html=True)

        # User profile section
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(
                profile['images'][0]['url'],
                width=150,
                use_container_width=True
            )
            st.markdown(
                f'<h2 class="gradient-text" style="text-align: center;">Welcome, {profile["display_name"]}!</h2>',
                unsafe_allow_html=True
            )

        # Process and analyze data
        audio_features_df = process_audio_features(audio_features)
        mood_analysis = analyze_mood(audio_features_df)
        music_patterns = analyze_music_patterns(audio_features_df)
        genres = get_genre_distribution(top_artists)
        listening_trends = calculate_listening_trends(recent_tracks)

        # Display mood insights
        st.markdown(
            f'''
            <div class="stat-card">
                <h3 class="gradient-text">Your Music Personality</h3>
                <p style="font-size: 1.2rem;">{mood_analysis['primary_mood']}</p>
                <div style="margin-top: 1rem;">
                    <span class="gradient-text" style="font-size: 1.5rem;">
                        {mood_analysis['mood_diversity_score']}%
                    </span>
                    <span style="color: #888;"> Mood Diversity Score</span>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Display visualizations
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_audio_features_radar(audio_features_df),
                use_container_width=True
            )

        with col2:
            st.plotly_chart(
                create_genre_bar_chart(genres['main_genres']),
                use_container_width=True
            )

        st.plotly_chart(
            create_listening_time_chart(recent_tracks),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Display top tracks with album art
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="scroll-fade">', unsafe_allow_html=True)
            st.subheader("🎵 Top Tracks")
            for i, track in enumerate(top_tracks['items'][:5], 1):
                display_track_item(track, i)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="scroll-fade">', unsafe_allow_html=True)
            st.subheader("👥 Top Artists")
            for i, artist in enumerate(top_artists['items'][:5], 1):
                display_track_item(artist, i)
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()