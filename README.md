
# Spotify Analytics Dashboard 🎵

An AI-powered Spotify analytics dashboard that provides deep insights into your music listening habits using machine learning and AI analysis.

![Spotify Analytics](https://github.com/yourusername/spotify-analytics-dashboard/raw/main/preview.png)

## Features
- **AI-Powered Analysis**: Get personalized insights about your music taste and listening patterns
- **Music Personality Profile**: Discover your unique listening personas based on your music choices
- **Smart Recommendations**: Receive tailored music suggestions that match your taste profile
- **Time-Based Filters**: Explore your listening trends with filters for 4 weeks, 6 months, and all time
- **Interactive Visualizations**: Visualize your music preferences with dynamic charts
- **Top Content Showcase**: View your top tracks, artists, and albums in a clean, modern interface
- **Mood Analysis**: Understand the emotional patterns in your music using ML clustering
- **Genre Distribution**: See a breakdown of your favorite music genres
- **Mobile Responsive**: Optimized for both desktop and mobile viewing

## Local Setup

### 1. Clone Repository
```bash
git clone <your-repository-url>
cd spotify-analytics-dashboard
```

### 2. Register a Spotify Developer Application
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Create a new app
4. Set the redirect URI to `http://localhost:5000`
5. Note your Client ID and Client Secret

### 3. Set Environment Variables
Create a `.env` file with:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
```

### 4. Install Dependencies
```bash
pip install streamlit spotipy pandas numpy scikit-learn plotly python-dotenv
```

### 5. Run Locally
```bash
streamlit run main.py
```

## Deploy to Vercel

### Prerequisites
- GitHub repository with your project
- Vercel account linked to your GitHub

### Deployment Steps

1. Push your code to GitHub:
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. Log into [Vercel](https://vercel.com) and import your GitHub repository

3. Configure the project:
   - The repository includes a `vercel.json` file that configures the build settings

4. Add Environment Variables:
   - Add `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` with your Spotify API credentials
   - Add `SPOTIPY_REDIRECT_URI` with your Vercel deployment URL (e.g., https://your-app-name.vercel.app)

5. Deploy!

6. After deployment, go back to your Spotify Developer Dashboard and add your Vercel URL as a redirect URI.

## Using the Dashboard

- Connect your Spotify account to see your personalized insights, or use "Demo Mode" to explore with simulated data
- Filter your music insights by time range (4 weeks, 6 months, or all time)
- Get AI-powered insights about your music taste and listening patterns
- Explore your top tracks, artists, and albums
- Discover song recommendations tailored to your unique preferences
- View your audio feature analysis through interactive visualizations

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

## License
MIT License

## Acknowledgements
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Streamlit](https://streamlit.io/)
- [Spotipy](https://spotipy.readthedocs.io/)
