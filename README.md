# Spotify Analytics Dashboard 🎵

An AI-powered Spotify analytics dashboard that provides deep insights into your music listening habits using machine learning.

## Features
- Advanced mood analysis using ML clustering
- Detailed music pattern recognition
- Genre distribution analysis
- Interactive visualizations
- Listening trend analysis

## Download and Setup

### 1. Download the Project
```bash
git clone <your-repository-url>
cd spotify-analytics-dashboard
```

### 2. Set Up Spotify API
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Set the redirect URI to:
   - For local development: `http://localhost:5000`
   - For Vercel deployment: `https://your-app-name.vercel.app`

### 3. Configure Environment Variables
Create a `.env` file with:
```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000  # or your Vercel URL
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

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Configure Environment Variables in Vercel:
- Go to your project settings
- Add the same environment variables as above
- Update SPOTIPY_REDIRECT_URI to your Vercel deployment URL

## Project Structure
- `main.py`: Main application file
- `analysis.py`: ML-based analysis functions
- `spotify_client.py`: Spotify API integration
- `visualizations.py`: Data visualization components
- `.streamlit/`: Streamlit configuration and styling

## Requirements
- Python 3.11+
- Streamlit
- Spotipy
- Pandas
- NumPy
- Scikit-learn
- Plotly
