import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_audio_features_radar(audio_features_df):
    """Create an enhanced radar chart for audio features."""
    features = ['danceability', 'energy', 'valence', 'acousticness']
    avg_features = audio_features_df[features].mean()

    fig = go.Figure()

    # Add main trace with gradient fill
    fig.add_trace(go.Scatterpolar(
        r=avg_features.values,
        theta=features,
        fill='toself',
        fillcolor='rgba(29, 185, 84, 0.2)',
        line=dict(color='#1DB954', width=2),
        name='Average Features'
    ))

    # Add dynamic range markers
    fig.add_trace(go.Scatterpolar(
        r=[0.25] * len(features),
        theta=features,
        fill=None,
        line=dict(color='rgba(255, 255, 255, 0.1)', dash='dot'),
        showlegend=False
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0.75] * len(features),
        theta=features,
        fill=None,
        line=dict(color='rgba(255, 255, 255, 0.1)', dash='dot'),
        showlegend=False
    ))

    # Update layout with modern styling
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                showline=False,
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.1)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Montserrat',
            color='white',
            size=12
        ),
        margin=dict(l=80, r=80, t=40, b=40)
    )
    return fig

def create_genre_bar_chart(genre_counts):
    """Create an enhanced bar chart for genre distribution."""
    df = pd.DataFrame(genre_counts, columns=['Genre', 'Count'])

    fig = px.bar(
        df,
        x='Count',
        y='Genre',
        orientation='h',
        color='Count',
        color_continuous_scale=['#1DB954', '#1ed760']
    )

    # Update layout with modern styling
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Montserrat',
            color='white',
            size=12
        ),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True,
            zeroline=False,
            showline=False
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=False,
            zeroline=False,
            showline=False
        ),
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=40, b=20),
        hoverlabel=dict(
            bgcolor='rgba(40,40,40,0.8)',
            font=dict(family='Montserrat', size=12)
        )
    )

    # Add hover effects
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>',
        marker_line_color='rgba(255,255,255,0.2)',
        marker_line_width=1
    )

    return fig

def create_listening_time_chart(recent_tracks):
    """Create an enhanced line chart for listening times."""
    df = pd.DataFrame([{
        'played_at': pd.to_datetime(track['played_at'])
    } for track in recent_tracks['items']])

    hourly_counts = df.groupby(df['played_at'].dt.hour).size().reset_index()
    hourly_counts.columns = ['Hour', 'Count']

    # Create area chart for better visualization
    fig = go.Figure()

    # Add gradient area
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Count'],
        fill='tozeroy',
        fillcolor='rgba(29, 185, 84, 0.2)',
        line=dict(color='#1DB954', width=2),
        mode='lines',
        name='Listening Activity'
    ))

    # Update layout with modern styling
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family='Montserrat',
            color='white',
            size=12
        ),
        xaxis=dict(
            title='Hour of Day',
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            showline=False,
            tickmode='array',
            ticktext=['12am', '3am', '6am', '9am', '12pm', '3pm', '6pm', '9pm'],
            tickvals=[0, 3, 6, 9, 12, 15, 18, 21]
        ),
        yaxis=dict(
            title='Number of Tracks',
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False,
            showline=False
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        hoverlabel=dict(
            bgcolor='rgba(40,40,40,0.8)',
            font=dict(family='Montserrat', size=12)
        )
    )

    # Add hover effects
    fig.update_traces(
        hovertemplate='<b>Hour: %{x}</b><br>Tracks: %{y}<extra></extra>'
    )

    return fig