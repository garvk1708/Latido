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

def typed_text(text, delay=0.03):
    """Simulate typing animation effect."""
    container = st.empty()
    for i in range(len(text) + 1):
        container.markdown(f'<p class="typed-text">{text[:i]}</p>', unsafe_allow_html=True)
        time.sleep(delay)
    return container

def main():
    st.markdown('<h1 class="fade-in">🎵 Spotify Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Initialize Spotify client
    try:
        sp = create_spotify_client()
    except Exception as e:
        st.error("""
        Unable to connect to Spotify. Please make sure:
        1. You have provided valid Spotify API credentials
        2. The redirect URI matches your Spotify app settings
        3. You are logged into Spotify

        Error details: {}
        """.format(str(e)))
        st.stop()

    # Get user profile
    with st.spinner("Loading your profile..."):
        profile = get_user_profile(sp)
        if profile:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(
                    profile['images'][0]['url'] if profile.get('images') else None,
                    width=150,
                    use_column_width=False
                )
                st.markdown(
                    f'<h2 class="fade-in">Welcome, {profile["display_name"]}!</h2>',
                    unsafe_allow_html=True
                )

    # Time range selector with custom styling
    time_range = st.selectbox(
        "Select time range",
        options=[
            ("short_term", "Last 4 weeks"),
            ("medium_term", "Last 6 months"),
            ("long_term", "All time")
        ],
        format_func=lambda x: x[1]
    )[0]

    # Fetch and analyze data
    with st.spinner("Analyzing your music..."):
        top_tracks = get_top_tracks(sp, time_range)
        top_artists = get_top_artists(sp, time_range)
        recent_tracks = get_recent_tracks(sp)

        if all([top_tracks, top_artists, recent_tracks]):
            track_ids = [track['id'] for track in top_tracks['items']]
            audio_features = get_audio_features(sp, track_ids)

            if audio_features:
                # Process data
                audio_features_df = process_audio_features(audio_features)
                mood_analysis = analyze_mood(audio_features_df)
                genres = get_genre_distribution(top_artists)
                listening_trends = calculate_listening_trends(recent_tracks)

                # Display insights with typing animation
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.header("🎯 Your Music Profile")
                typed_text(mood_analysis)
                st.markdown('</div>', unsafe_allow_html=True)

                # Display statistics with animation
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    with st.container():
                        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                        st.metric("Peak Listening Hour", f"{listening_trends['peak_hour']}:00")
                        st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    with st.container():
                        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                        st.metric("Tracks Analyzed", listening_trends['total_tracks'])
                        st.markdown('</div>', unsafe_allow_html=True)

                with col3:
                    with st.container():
                        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
                        st.metric("Top Genre", genres[0][0].title() if genres else "N/A")
                        st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Visualizations with hover effects
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.header("📊 Music Analysis")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Audio Features")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(
                        create_audio_features_radar(audio_features_df),
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.subheader("Genre Distribution")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(
                        create_genre_bar_chart(genres),
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                st.subheader("Listening Pattern")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(
                    create_listening_time_chart(recent_tracks),
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # Top artists and tracks with animation
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                    st.subheader("🎤 Top Artists")
                    for i, artist in enumerate(top_artists['items'][:5], 1):
                        st.markdown(
                            f'<div class="stat-card" style="margin-bottom: 10px;">{i}. {artist["name"]}</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                    st.subheader("🎵 Top Tracks")
                    for i, track in enumerate(top_tracks['items'][:5], 1):
                        st.markdown(
                            f'<div class="stat-card" style="margin-bottom: 10px;">{i}. {track["name"]} - {track["artists"][0]["name"]}</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()