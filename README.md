
# Latido 💓 - El ritmo de tu corazón musical

![Latido Logo](generated-icon.png)

## Overview
Latido is an AI-powered web application that reveals the unique heartbeat of your musical tastes through advanced analysis and elegant visualizations. Discover insights about your Spotify listening habits and get personalized recommendations.

## Features
- **AI-Powered Analysis**: Get personalized insights about your music tastes and listening patterns
- **Unique Musical Profile**: Discover your musical personality based on your song choices
- **Smart Recommendations**: Receive music suggestions tailored to your taste profile
- **Time Filters**: Explore your trends with filters for 4 weeks, 6 months, and all time
- **Interactive Visualizations**: Visualize your musical preferences with dynamic charts
- **Featured Content**: See your favorite songs, artists, and albums in an elegant interface
- **Mood Analysis**: Understand emotional patterns in your music
- **Genre Distribution**: View a breakdown of your favorite music genres
- **Responsive Design**: Optimized for both desktop and mobile devices

## Demo Mode

Don't want to connect your Spotify account? Use the Demo Mode to explore the dashboard with simulated data!

## Quick Start

1. Click the Run button at the top of the page
2. The app will start automatically with the Streamlit server
3. Optional: Connect your Spotify account or use Demo Mode

## Using the Dashboard

- **Connect Spotify**: Connect your Spotify account to see your personalized insights, or use "Demo Mode"
- **Filter by Time**: Filter your music insights by time range (4 weeks, 6 months, or all time)
- **Explore Stats**: View your top tracks, artists, and albums
- **Get Insights**: Discover AI-powered insights about your music taste
- **Responsive Design**: App automatically adapts to all screen sizes from mobile to desktop

## Project Structure
- `main.py`: Main application and UI components
- `analysis.py`: ML-based analysis and insight generation
- `spotify_client.py`: Spotify API integration and data retrieval
- `visualizations.py`: Interactive data visualization components
- `simulation.py`: Demo data generation for testing
- `.streamlit/`: Streamlit configuration and custom styling

## Dependencies
- Python 3.11+
- Streamlit
- Spotipy (Spotify API client)
- Pandas & NumPy (Data processing)
- Scikit-learn (Machine learning for insights)
- Plotly (Interactive visualizations)
- Python-dotenv (Environment management)

## Development

To modify this application:
1. Edit the `.streamlit/style.css` file to change the appearance
2. Modify `visualizations.py` to update or add new data visualizations
3. Extend `analysis.py` to implement new data analysis methods
4. Update `main.py` to change the UI layout and components

## Deployment

The app is set up for easy deployment:

1. The app will run automatically on Replit
2. For public sharing, click the "Run" button at the top of the page
3. Share the provided URL with others

## Troubleshooting

Common issues and solutions:

- **Authentication Errors**: Make sure your Spotify credentials are correctly set in the .env file
- **Missing Data**: If charts or recommendations don't appear, try using Demo Mode to verify the app functionality
- **Display Issues**: Clear your browser cache or try a different browser if visualizations don't render properly

## License
MIT License
