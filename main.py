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

def animated_text(text, animation_class="slide-in", delay=0.03):
    """Display text with animation effect."""
    st.markdown(f'<div class="{animation_class}">{text}</div>', unsafe_allow_html=True)
    time.sleep(delay)

def typed_text(text, delay=0.03):
    """Simulate typing animation effect."""
    container = st.empty()
    for i in range(len(text) + 1):
        container.markdown(f'<p class="typed-text">{text[:i]}</p>', unsafe_allow_html=True)
        time.sleep(delay)
    return container

def display_stat_card(title, value, icon="📊"):
    """Display a statistic in an animated card."""
    st.markdown(f'''
        <div class="stat-card slide-in">
            <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{icon} {title}</div>
            <div style="font-size: 2rem; font-weight: bold; 
                        background: linear-gradient(120deg, #1DB954, #1ed760);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;">
                {value}
            </div>
        </div>
    ''', unsafe_allow_html=True)

def main():
    # Header with animation
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown('''
        <h1 style="text-align: center; font-size: 3rem; margin-bottom: 2rem;">
            🎵 Spotify Analytics Dashboard
        </h1>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Initialize Spotify client
    try:
        sp = create_spotify_client()
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")
        st.stop()

    # Get user profile with loading animation
    with st.spinner("📻 Tuning in to your music..."):
        profile = get_user_profile(sp)
        if profile:
            st.markdown('<div class="fade-in">', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if profile.get('images'):
                    st.image(
                        profile['images'][0]['url'],
                        width=150,
                        use_column_width=False
                    )
                typed_text(f"Welcome back, {profile['display_name']}! 🎸")
            st.markdown('</div>', unsafe_allow_html=True)

    # Time range selector with custom styling
    time_range = st.selectbox(
        "📅 Select time range",
        options=[
            ("short_term", "Last 4 weeks"),
            ("medium_term", "Last 6 months"),
            ("long_term", "All time")
        ],
        format_func=lambda x: x[1]
    )[0]

    # Fetch and analyze data
    with st.spinner("🎼 Analyzing your music..."):
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
                music_patterns = analyze_music_patterns(audio_features_df)
                genres = get_genre_distribution(top_artists)
                listening_trends = calculate_listening_trends(recent_tracks)

                # Display mood insights with animation
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.header("🎯 Your Music Profile")

                # Display mood analysis
                mood_text = f"Your primary music mood is {mood_analysis['primary_mood']}!"
                typed_text(mood_text)

                # Display advanced statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    display_stat_card(
                        "Mood Diversity",
                        f"{mood_analysis['mood_diversity_score']}%",
                        "🎭"
                    )
                with col2:
                    display_stat_card(
                        "Listening Sessions",
                        listening_trends['listening_sessions'],
                        "🎧"
                    )
                with col3:
                    display_stat_card(
                        "Genre Diversity",
                        genres['genre_diversity'],
                        "🎵"
                    )

                # Display visualizations with animations
                st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                st.header("📊 Music Analysis")

                # Display charts in an animated grid
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🎼 Audio Features")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(
                        create_audio_features_radar(audio_features_df),
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.subheader("🎸 Genre Distribution")
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    st.plotly_chart(
                        create_genre_bar_chart(genres['main_genres']),
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                # Display listening pattern
                st.subheader("📈 Listening Pattern")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.plotly_chart(
                    create_listening_time_chart(recent_tracks),
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                # Display top artists and tracks with animations
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                    st.subheader("🎤 Top Artists")
                    for i, artist in enumerate(top_artists['items'][:5], 1):
                        st.markdown(
                            f'<div class="stat-card">{i}. {artist["name"]}</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                    st.subheader("💿 Top Tracks")
                    for i, track in enumerate(top_tracks['items'][:5], 1):
                        st.markdown(
                            f'<div class="stat-card">{i}. {track["name"]} - {track["artists"][0]["name"]}</div>',
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()