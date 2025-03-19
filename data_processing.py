import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.express as px
import pandas as pd

def filter_news_by_date(news_df, start_date, end_date):
    # Convert input strings to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the DataFrame (inclusive of both start_date and end_date)
    mask = (news_df['date'] >= start_date) & (news_df['date'] <= end_date)
    return news_df.loc[mask]



def plot_scores_over_time(filtered_df):
    """Generate plots for mean bias and positivity scores over time using Plotly."""
    # Ensure the 'date' column is in datetime format
    filtered_df['date'] = pd.to_datetime(filtered_df['date'])

    # Extract the date part (ignoring the time)
    filtered_df['date_only'] = filtered_df['date'].dt.date

    # Group by date and calculate mean scores
    daily_scores = filtered_df.groupby('date_only').agg({
        'bias': 'mean',
        'positivity': 'mean'
    }).reset_index()

    # Check if the DataFrame is empty
    if daily_scores.empty:
        return "<p>No data available for the selected date range.</p>"

    # Reshape the data into long format for Plotly
    daily_scores_long = pd.melt(daily_scores, id_vars=['date_only'], 
                                value_vars=['bias', 'positivity'],
                                var_name='score_type', value_name='score_value')

    # Create a Plotly figure
    fig = px.line(daily_scores_long, x='date_only', y='score_value', color='score_type',
                  title='Daily Mean Bias and Positivity Scores',
                  labels={'score_value': 'Mean Score', 'date_only': 'Date'})
    fig.update_layout(legend_title_text='Score Type')

    # Convert the figure to HTML
    graph_html = fig.to_html(full_html=False)
    return graph_html
