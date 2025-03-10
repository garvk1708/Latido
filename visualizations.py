import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_audio_features_radar(audio_features_df):
    """Create radar chart for audio features."""
    features = ['danceability', 'energy', 'valence', 'acousticness']
    avg_features = audio_features_df[features].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=avg_features.values,
        theta=features,
        fill='toself',
        name='Average Features'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    return fig

def create_genre_bar_chart(genre_counts):
    """Create bar chart for genre distribution."""
    df = pd.DataFrame(genre_counts, columns=['Genre', 'Count'])
    
    fig = px.bar(
        df,
        x='Count',
        y='Genre',
        orientation='h',
        color='Count',
        color_continuous_scale=['#1DB954', '#1ed760']
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

def create_listening_time_chart(recent_tracks):
    """Create line chart for listening times."""
    df = pd.DataFrame([{
        'played_at': pd.to_datetime(track['played_at'])
    } for track in recent_tracks['items']])
    
    hourly_counts = df.groupby(df['played_at'].dt.hour).size().reset_index()
    hourly_counts.columns = ['Hour', 'Count']
    
    fig = px.line(
        hourly_counts,
        x='Hour',
        y='Count',
        line_shape='spline'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig
