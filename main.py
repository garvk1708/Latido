import streamlit as st
import time
from spotify_client import (
    create_spotify_client, get_user_profile, get_top_tracks,
    get_top_artists, get_recent_tracks, get_audio_features,
    get_top_albums
)
from analysis import (
    process_audio_features, analyze_mood, get_genre_distribution,
    calculate_listening_trends, analyze_music_patterns, cluster_tracks
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

def display_artist_item(artist, index):
    """Display an artist with image and hover effects."""
    st.markdown(f'''
        <div class="track-item">
            <div class="track-number">{index}</div>
            <img src="{artist['images'][0]['url']}" 
                 class="track-image" alt="{artist['name']}">
            <div class="track-info">
                <div class="track-name">{artist['name']}</div>
                <div class="track-artist">Artist</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
def display_album_item(album, index):
    """Display an album with cover art and hover effects."""
    st.markdown(f'''
        <div class="track-item">
            <div class="track-number">{index}</div>
            <img src="{album['images'][0]['url']}" 
                 class="track-image" alt="{album['name']}">
            <div class="track-info">
                <div class="track-name">{album['name']}</div>
                <div class="track-artist">{album['artists'][0]['name']}</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

def main():
    # Set responsive layout based on viewport
    if 'mobile_view' not in st.session_state:
        st.session_state.mobile_view = False
        
    # Allow manual toggle for testing
    mobile_view = st.sidebar.checkbox("Mobile View", value=False)
    st.session_state.mobile_view = mobile_view
    
    create_hero_section()

    # Simulation mode toggle
    use_simulation = st.sidebar.checkbox("Use Demo Mode", value=True, 
                                       help="Try the dashboard with simulated data")

    # Time range filter
    time_range = st.sidebar.selectbox(
        "📅 Select time range",
        options=[
            ("short_term", "Last 4 weeks"),
            ("medium_term", "Last 6 months"),
            ("long_term", "All time")
        ],
        format_func=lambda x: x[1],
        index=1  # Default to medium_term
    )[0]
    
    if use_simulation:
        # Use simulated data
        data = get_simulated_data(time_range)
        profile = data['profile']
        top_tracks = data['top_tracks']
        top_artists = data['top_artists']
        top_albums = data['top_albums']
        recent_tracks = data['recent_tracks']
        audio_features = data['audio_features']
    else:
        # Initialize Spotify client and get real data
        try:
            sp = create_spotify_client()
            profile = get_user_profile(sp)

            with st.spinner("🎼 Analyzing your music..."):
                top_tracks = get_top_tracks(sp, time_range)
                top_artists = get_top_artists(sp, time_range)
                top_albums = get_top_albums(sp, time_range)
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
        
        # AI-powered track clusters
        track_clusters = cluster_tracks(audio_features_df)
        
        # Define music personality types based on analysis
        personality_types = {
            'explorer': mood_analysis['mood_diversity_score'] > 70,
            'enthusiast': mood_analysis['emotional_stats']['energy'] > 0.7,
            'analyst': music_patterns['complexity_score'] > 60,
            'nostalgic': music_patterns['acoustic_electronic_ratio'] > 2.0,
            'rhythm_driven': music_patterns['tempo_patterns']['tempo_variation'] < 10
        }
        
        # Determine top traits
        top_traits = [k for k, v in personality_types.items() if v]
        if not top_traits:
            top_traits = ['balanced']
            
        music_personality = {
            'explorer': "Music Explorer: You seek diverse sounds and experiences.",
            'enthusiast': "Energy Enthusiast: You gravitate toward high-energy music.",
            'analyst': "Sonic Analyst: You appreciate musical complexity and detail.",
            'nostalgic': "Acoustic Nostalgic: You prefer traditional sounds over electronic.",
            'rhythm_driven': "Rhythm Driven: You connect with consistent beats and tempos.",
            'balanced': "Musical Omnivore: You have a balanced and diverse taste profile."
        }
        
        # Extract primary and secondary traits
        primary_trait = top_traits[0] if top_traits else 'balanced'
        primary_description = music_personality[primary_trait]
        
        # Additional AI insights
        listening_personality = f"Based on your {listening_trends['listening_sessions']} listening sessions, you enjoy {genres[0][0] if genres else 'diverse'} music most during {listening_trends['peak_hour']}:00."
        
        # Display enhanced AI insights in a responsive layout
        st.markdown(
            f'''
            <div class="stat-card">
                <h3 class="gradient-text">Your AI Music Personality</h3>
                <p style="font-size: 1.2rem;">{primary_description}</p>
                <p style="font-size: 0.9rem; color: #888; margin-top: 0.5rem;">{listening_personality}</p>
                <div style="margin-top: 1rem; display: flex; justify-content: space-between; flex-wrap: wrap;">
                    <div>
                        <span class="gradient-text" style="font-size: 1.5rem;">
                            {mood_analysis['mood_diversity_score']}%
                        </span>
                        <span style="color: #888;"> Diversity</span>
                    </div>
                    <div>
                        <span class="gradient-text" style="font-size: 1.5rem;">
                            {music_patterns['complexity_score']}%
                        </span>
                        <span style="color: #888;"> Complexity</span>
                    </div>
                </div>
            </div>
            ''',
            unsafe_allow_html=True
        )

        # Display visualizations
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Use responsive columns based on screen size
        use_container_width = True
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(
                create_audio_features_radar(audio_features_df),
                use_container_width=use_container_width
            )

        with col2:
            # Fix the genre chart error - genres should be a list of tuples
            st.plotly_chart(
                create_genre_bar_chart(genres),
                use_container_width=use_container_width
            )

        st.plotly_chart(
            create_listening_time_chart(recent_tracks),
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Responsive layout for tracks, artists, and albums
        # For larger screens use columns, for mobile stack vertically
        if st.session_state.get("mobile_view", False):
            # Mobile view - stacked layout
            st.markdown('<div class="scroll-fade mobile-view">', unsafe_allow_html=True)
            st.subheader("🎵 Top Tracks")
            for i, track in enumerate(top_tracks['items'][:5], 1):
                display_track_item(track, i)
                
            st.subheader("👥 Top Artists")
            for i, artist in enumerate(top_artists['items'][:5], 1):
                display_artist_item(artist, i)
                
            st.subheader("💿 Top Albums")
            for i, album in enumerate(top_albums['items'][:5], 1):
                display_album_item(album, i)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Desktop view - side by side
            st.markdown("<h2 class='section-header'>Your Top Music</h2>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
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
                    display_artist_item(artist, i)
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col3:
                st.markdown('<div class="scroll-fade">', unsafe_allow_html=True)
                st.subheader("💿 Top Albums")
                for i, album in enumerate(top_albums['items'][:5], 1):
                    display_album_item(album, i)
                st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()