import streamlit as st
import time
import base64
from spotify_client import (
    create_spotify_client, get_user_profile, get_top_tracks,
    get_top_artists, get_recent_tracks, get_audio_features,
    get_top_albums, get_recommendations
)
from analysis import (
    process_audio_features, analyze_mood, get_genre_distribution,
    calculate_listening_trends, analyze_music_patterns, cluster_tracks,
    analyze_taste_profile
)
from visualizations import (
    create_audio_features_radar, create_genre_bar_chart,
    create_listening_time_chart
)
from simulation import get_simulated_data

# Import os for file operations
import os

# Set favicon
favicon_path = "generated-icon.png"
# If no favicon file exists, create one
if not os.path.exists(favicon_path):
    from PIL import Image, ImageDraw
    # Create a heartbeat logo favicon
    img = Image.new('RGBA', (64, 64), color=(18, 18, 18, 255))
    draw = ImageDraw.Draw(img)
    # Draw a heartbeat line
    points = [(8, 32), (16, 32), (20, 16), (28, 48), (36, 24), (44, 32), (56, 32)]
    draw.line(points, fill=(255, 51, 102, 255), width=3)
    img.save(favicon_path, 'PNG')

st.set_page_config(
    page_title="Latido - Musical Heart Rhythm",
    page_icon=favicon_path,
    layout="wide",
    initial_sidebar_state="collapsed"
)


# Import os for file operations
import os

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add custom logo styling
from visualizations import add_logo_styling
add_logo_styling()

# Inline SVG logo for Latido - Using a simplified approach that works better with Streamlit
latido_logo = '''
<div style="text-align: center; margin-bottom: 1rem;">
  <svg width="120" height="48" viewBox="0 0 120 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M20.5 8.5C17.5 11.5 6.5 28.5 5 30.5C3.5 32.5 4 38 9 38C14 38 18 33.5 20.5 30.5C23 27.5 26.5 22 28 20C29.5 18 35.5 10 40 10C44.5 10 44.5 13.5 43 17C41.5 20.5 38 25 36.5 27C35 29 31 34 29.5 35.5C28 37 23 42 23 42" stroke="#FF3366" stroke-width="3" stroke-linecap="round"/>
  </svg>
  <div style="font-family: Arial, sans-serif; font-size: 22px; font-weight: 700; color: #FF3366; margin-top: -30px;">LATIDO</div>
</div>
'''

def get_base64_of_bin_file(bin_file):
    """Get base64 encoding of binary file"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def create_hero_section():
    """Create an animated hero section with Latido branding."""
    st.markdown(f'''
        <div class="hero-section">
            <div class="logo-container">
                <svg width="120" height="48" viewBox="0 0 120 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M20.5 8.5C17.5 11.5 6.5 28.5 5 30.5C3.5 32.5 4 38 9 38C14 38 18 33.5 20.5 30.5C23 27.5 26.5 22 28 20C29.5 18 35.5 10 40 10C44.5 10 44.5 13.5 43 17C41.5 20.5 38 25 36.5 27C35 29 31 34 29.5 35.5C28 37 23 42 23 42" stroke="#FF3366" stroke-width="3" stroke-linecap="round"/>
                </svg>
                <div class="latido-text">LATIDO</div>
            </div>
            <h2 class="tagline-container">
                <span class="tagline">The rhythm of your musical heart</span>
            </h2>
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

def init_session_state():
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    # Other initializations...

def main():
    # Initialize session state first
    init_session_state()
    
    # Always use dark theme for Latido
    st.markdown("""
        <style>
            [data-testid="stHeader"] {background-color: #121212;}
        </style>
    """, unsafe_allow_html=True)

    create_hero_section()

    # Create top navigation controls in a container
    with st.container():
        st.markdown('<div class="controls-container">', unsafe_allow_html=True)
        col1, col2 = st.columns([1,2]) #Removed col3 as mobile view is removed

        with col1:
            #Time range filter with styled dropdown
            time_range = st.selectbox(
                "📅 Time Period",
                options=[
                    ("short_term", "Last 4 weeks"),
                    ("medium_term", "Last 6 months"),
                    ("long_term", "All time")
                ],
                format_func=lambda x: x[1],
                index=1  # Default to medium_term
            )[0]

        with col2:
            # Simulation mode toggle with styled button
            use_simulation = st.checkbox("✨ Demo Mode", value=False, 
                                        help="Try the dashboard with simulated data")

        st.markdown('</div>', unsafe_allow_html=True)

        # Add a separator line
        st.markdown('<hr class="separator">', unsafe_allow_html=True)

    # Display loading animation
    with st.container():
        if use_simulation:
            with st.spinner("🎵 Loading your musical profile..."):
                # Add small delay to show loading animation
                time.sleep(1)
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
                # Show a customized loading spinner
                with st.spinner("🎵 Connecting to Spotify..."):
                    sp = create_spotify_client()
                    if not sp:
                        st.error("Spotify authentication failed. Try using Demo Mode instead.")
                        st.info("If you're trying to authenticate, make sure you've registered http://0.0.0.0:5000/callback as a redirect URI in your Spotify Developer account.")
                        st.stop()
                    
                    profile = get_user_profile(sp)
                    if not profile:
                        st.error("Could not retrieve user profile. Try using Demo Mode instead.")
                        st.stop()

                # Use a different spinner for analyzing music
                with st.spinner("🎼 Analyzing your musical heartbeat..."):
                    top_tracks = get_top_tracks(sp, time_range)
                    top_artists = get_top_artists(sp, time_range)
                    top_albums = get_top_albums(sp, time_range)
                    recent_tracks = get_recent_tracks(sp)

                    if all([top_tracks, top_artists, recent_tracks]):
                        track_ids = [track['id'] for track in top_tracks['items']]
                        audio_features = get_audio_features(sp, track_ids)
                    else:
                        st.error("Failed to fetch your music data. Try using Demo Mode instead.")
                        st.stop()
            except Exception as e:
                st.error(f"Authentication failed: {str(e)}")
                st.warning("Please try using Demo Mode or check your Spotify Developer credentials.")
                st.stop()

    # Process and display data
    if profile and audio_features:
        st.markdown('<div class="scroll-fade">', unsafe_allow_html=True)

        # User profile section
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="{profile["images"][0]["url"]}" width="150px"></div>',
                unsafe_allow_html=True
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

        # Get detailed taste analysis
        taste_profile = analyze_taste_profile(audio_features_df, genres, top_artists)

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

        # Display personalized insights about user's taste
        if taste_profile and taste_profile['insights']:
            st.markdown("<h3 class='section-header'>AI Insights About Your Music Taste</h3>", unsafe_allow_html=True)

            # Create a container for insights with a nicer style
            st.markdown('''
                <div class="insights-container">
            ''', unsafe_allow_html=True)

            # Display each insight with a nice style
            for insight in taste_profile['insights'][:5]:  # Limit to top 5 insights
                st.markdown(f'''
                    <div class="insight-card">
                        <span class="insight-icon">💡</span>
                        <p>{insight}</p>
                    </div>
                ''', unsafe_allow_html=True)

            # Display personality traits
            if taste_profile['personality_traits']:
                traits_text = ", ".join(taste_profile['personality_traits'])
                st.markdown(f'''
                    <div class="personality-traits">
                        <p><strong>Your listening personas:</strong> {traits_text}</p>
                    </div>
                ''', unsafe_allow_html=True)

            st.markdown('''
                </div>
            ''', unsafe_allow_html=True)

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


        # Removed mobile view conditional rendering as it's no longer needed.  All layouts should be responsive via CSS.

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

        # Song recommendations section
        st.markdown("<h2 class='section-header'>Recommended For You</h2>", unsafe_allow_html=True)

        if top_tracks and top_artists:
            # Get seed data for recommendations
            seed_track_ids = [track['id'] for track in top_tracks['items'][:2]]
            seed_artist_ids = [artist['id'] for artist in top_artists['items'][:3]]

            if use_simulation:
                # Simulated recommendations
                recommendations = get_simulated_data(time_range)['recommendations']
            else:
                # Get real recommendations with audio features for personalization
                recommendations = get_recommendations(
                    sp, 
                    seed_tracks=seed_track_ids, 
                    seed_artists=seed_artist_ids,
                    limit=10,
                    audio_features_df=audio_features_df
                )

            if recommendations and 'tracks' in recommendations:
                # Responsive grid layout based on screen size
                columns = 5  # Default column count, CSS will handle responsive behavior
                rows = (len(recommendations['tracks']) + columns - 1) // columns

                # Create grid
                for row in range(rows):
                    cols = st.columns(columns)
                    for col in range(columns):
                        idx = row * columns + col
                        if idx < len(recommendations['tracks']):
                            track = recommendations['tracks'][idx]
                            with cols[col]:
                                st.markdown(f'''
                                    <div class="recommendation-card" style="--i: {idx}">
                                        <img src="{track['album']['images'][0]['url']}" alt="{track['name']}" 
                                             style="width: 100%; border-radius: 8px;">
                                        <p style="font-weight: bold; margin: 5px 0 0 0; white-space: nowrap; 
                                                  overflow: hidden; text-overflow: ellipsis;">
                                            {track['name']}
                                        </p>
                                        <p style="margin: 0; color: var(--text-secondary); white-space: nowrap; 
                                                  overflow: hidden; text-overflow: ellipsis;">
                                            {track['artists'][0]['name']}
                                        </p>
                                    </div>
                                ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()