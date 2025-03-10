
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np

def create_audio_features_radar(audio_features_df):
    """Create a radar chart of audio features."""
    try:
        # Extract the relevant features for the radar chart
        features = [
            'danceability', 'energy', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence'
        ]
        
        # Calculate the average for each feature
        avg_features = audio_features_df[features].mean().tolist()
        
        # Create the radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=avg_features,
            theta=features,
            fill='toself',
            name='Your Music Profile',
            line=dict(color='#1DB954'),
            fillcolor='rgba(29, 185, 84, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=False,
            margin=dict(l=80, r=80, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888')
        )
        
        return fig
    except Exception as e:
        # Fallback to a simple placeholder
        fig = go.Figure()
        fig.add_annotation(text=f"Could not generate radar chart: {str(e)}", 
                          showarrow=False)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888')
        )
        return fig

def create_genre_bar_chart(genres):
    """Create a bar chart of top genres."""
    try:
        # If genres is None or empty, create placeholder data
        if not genres:
            genres = [("Pop", 5), ("Rock", 4), ("Hip-Hop", 3), 
                      ("Electronic", 2), ("Jazz", 1)]
        
        # Convert to dataframe
        df = pd.DataFrame(genres, columns=['genre', 'count'])
        
        # Sort by count descending
        df = df.sort_values('count', ascending=False).head(5)
        
        # Create the bar chart
        fig = px.bar(
            df,
            x='count',
            y='genre',
            orientation='h',
            color='count',
            color_continuous_scale=['#1DB954', '#52E07C', '#86E8A3', '#BAEFC9', '#EDFCF0'],
        )
        
        fig.update_layout(
            title=dict(
                text='Your Top Genres',
                font=dict(size=16),
                y=0.95
            ),
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888'),
            xaxis=dict(title=''),
            yaxis=dict(title=''),
            coloraxis_showscale=False
        )
        
        return fig
    except Exception as e:
        # Fallback to a simple placeholder
        fig = go.Figure()
        fig.add_annotation(text=f"Could not generate genre chart: {str(e)}", 
                          showarrow=False)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888')
        )
        return fig

import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import random

def create_audio_features_radar(audio_features_df):
    """Create a radar chart of audio features."""
    # Extract mean values for key features
    mean_values = audio_features_df[['danceability', 'energy', 'valence', 
                                     'acousticness', 'instrumentalness']].mean()
    
    # Create radar chart data
    categories = ['Danceability', 'Energy', 'Positivity', 'Acousticness', 'Instrumentalness']
    values = mean_values.values.tolist()
    
    # Create figure
    fig = px.line_polar(
        r=values,
        theta=categories,
        line_close=True,
        range_r=[0, 1],
        template="plotly_dark"
    )
    
    # Update layout and styling
    fig.update_traces(
        fill='toself',
        fillcolor='rgba(255, 51, 102, 0.2)',
        line=dict(color='rgba(255, 51, 102, 0.8)', width=2)
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickfont=dict(size=10),
                tickvals=[0.2, 0.4, 0.6, 0.8]
            ),
            angularaxis=dict(
                tickfont=dict(size=12),
                rotation=90,
                direction="clockwise"
            )
        ),
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title="Your Musical DNA",
        title_font=dict(size=20),
        title_x=0.5,
        showlegend=False,
        margin=dict(l=80, r=80, t=100, b=80)
    )
    
    return fig

def create_genre_bar_chart(genres):
    """Create a bar chart of top genres."""
    # Handle empty data
    if not genres:
        genres = [("No genre data", 0)]
    
    # Limit to top 8 genres
    genres = genres[:8]
    
    # Create dataframe
    df = pd.DataFrame({
        'genre': [genre[0] for genre in genres],
        'count': [genre[1] for genre in genres]
    })
    
    # Sort by count
    df = df.sort_values('count', ascending=True)
    
    # Create bar chart
    fig = px.bar(
        df,
        y='genre',
        x='count',
        orientation='h',
        template="plotly_dark"
    )
    
    # Update layout and styling
    fig.update_traces(
        marker_color='rgba(255, 51, 102, 0.7)',
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        title="Your Top Genres",
        title_font=dict(size=20),
        title_x=0.5,
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=60, b=40)
    )
    
    return fig

def create_listening_time_chart(recent_tracks):
    """Create a chart showing listening patterns by hour of day."""
    try:
        # Extract timestamps and convert to datetime
        if not recent_tracks:
            # Create simulated data if no data available
            hours = list(range(24))
            counts = np.random.randint(0, 10, size=24)
            df = pd.DataFrame({'hour': hours, 'count': counts})
        else:
            timestamps = [item['played_at'] for item in recent_tracks['items']]
            # Convert timestamps to datetime objects
            datetimes = [datetime.fromisoformat(ts.replace('Z', '+00:00')) 
                         if 'Z' in ts else datetime.fromisoformat(ts) 
                         for ts in timestamps]
            
            # Extract hour of day
            hours = [dt.hour for dt in datetimes]
            
            # Count tracks by hour
            hour_counts = {}
            for hour in range(24):
                hour_counts[hour] = hours.count(hour)
            
            # Convert to dataframe
            df = pd.DataFrame({
                'hour': list(hour_counts.keys()),
                'count': list(hour_counts.values())
            })
        
        # Create time labels (12 AM, 1 AM, etc.)
        time_labels = [f"{h%12 or 12} {'AM' if h<12 else 'PM'}" for h in range(24)]
        df['time_label'] = [time_labels[hour] for hour in df['hour']]
        
        # Create the line chart
        fig = px.line(
            df,
            x='hour',
            y='count',
            markers=True,
            template="plotly_dark"
        )
        
        # Update layout and styling
        fig.update_traces(
            line=dict(color='rgba(255, 51, 102, 0.8)', width=3),
            marker=dict(size=8, color='rgba(255, 204, 0, 0.8)'),
            hovertemplate='<b>%{customdata}</b><br>Tracks: %{y}<extra></extra>'
        )
        
        fig.update_traces(customdata=df['time_label'])
        
        fig.update_layout(
            paper_bgcolor='rgba(0, 0, 0, 0)',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            title="When You Listen",
            title_font=dict(size=20),
            title_x=0.5,
            xaxis_title=None,
            yaxis_title="Tracks played",
            xaxis=dict(
                showgrid=False,
                tickmode='array',
                tickvals=list(range(0, 24, 3)),
                ticktext=[time_labels[h] for h in range(0, 24, 3)]
            ),
            yaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=60, b=40)
        )
        
        # Add a subtle area fill under the line
        fig.add_scatter(
            x=df['hour'],
            y=df['count'],
            mode='none',
            fill='tozeroy',
            fillcolor='rgba(255, 51, 102, 0.1)',
            showlegend=False
        )
        
        return fig
    except Exception as e:
        # Return a simple placeholder chart if there's an error
        hours = list(range(24))
        counts = np.random.randint(1, 5, size=24)
        fig = px.line(x=hours, y=counts, template="plotly_dark")
        fig.update_layout(title="Listening Patterns (Demo)")
        return fig
            y='count',
            markers=True,
            line_shape='spline',
        )
        
        # Add customization
        fig.update_traces(
            line=dict(color='#1DB954', width=3),
            marker=dict(color='#1DB954', size=8)
        )
        
        fig.update_layout(
            title=dict(
                text='Your Listening Schedule',
                font=dict(size=16),
                y=0.95
            ),
            xaxis=dict(
                title='Time of Day',
                tickmode='array',
                tickvals=list(range(0, 24, 3)),
                ticktext=[time_labels[h] for h in range(0, 24, 3)]
            ),
            yaxis=dict(title='Number of Tracks'),
            margin=dict(l=20, r=20, t=40, b=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888'),
        )
        
        return fig
    except Exception as e:
        # Fallback to a simple placeholder
        fig = go.Figure()
        fig.add_annotation(text=f"Could not generate listening chart: {str(e)}", 
                          showarrow=False)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888')
        )
        return fig
