
# Spotify Analytics Dashboard 🎵

An AI-powered Spotify analytics dashboard that provides deep insights into your music listening habits using machine learning.

## Features
- View your top tracks, artists, and albums
- Explore your listening trends with time-based filters (4 weeks, 6 months, all time)
- Advanced mood analysis using ML clustering
- Detailed music pattern recognition
- Genre distribution analysis
- Interactive visualizations
- AI-generated music personality profile

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
pip install streamlit spotipy pandas numpy scikit-learn plotly
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
   - Build Command: Leave empty (uses vercel.json configuration)
   - Output Directory: Leave empty
   - Install Command: Leave empty (uses vercel.json configuration)

4. Add Environment Variables:
   - Add `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` with your Spotify API credentials
   - Add `SPOTIPY_REDIRECT_URI` with your Vercel deployment URL (e.g., https://your-app-name.vercel.app)

5. Deploy!

6. After deployment, go back to your Spotify Developer Dashboard and add your Vercel URL as a redirect URI.

## Using the Dashboard

- Switch between real data and simulated data using the "Use Demo Mode" toggle
- Filter your music insights by time range (4 weeks, 6 months, or all time)
- Explore your top tracks, artists, and albums
- Discover your AI-generated music personality

## Project Structure
- `main.py`: Main application file
- `analysis.py`: ML-based analysis functions
- `spotify_client.py`: Spotify API integration
- `visualizations.py`: Data visualization components
- `simulation.py`: Demo data generation
- `.streamlit/`: Streamlit configuration and styling

## Dependencies
- Python 3.11+
- Streamlit
- Spotipy
- Pandas
- NumPy
- Scikit-learn
- Plotly
