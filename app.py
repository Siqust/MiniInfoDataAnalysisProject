from flask import Flask, render_template, request
from data_processing import filter_news_by_date, plot_scores_over_time
import pandas as pd

app = Flask(__name__)

# Load your DataFrame here
# Replace 'path_to_your_news_data.csv' with the actual path to your CSV file
news_df = pd.read_csv('database.csv')
news_df['date'] = pd.to_datetime(news_df['date'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the selected dates from the form
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Filter the news DataFrame based on the selected dates
        filtered_df = filter_news_by_date(news_df, start_date, end_date)

        # Extract the date part (ignoring the time)
        filtered_df['date_only'] = pd.to_datetime(filtered_df['date']).dt.date

        # Group news articles by date
        grouped_news = filtered_df.groupby('date_only').apply(
            lambda x: x[['title', 'bias', 'positivity','link']].to_dict('records')
        ).to_dict()

        # Generate the Plotly graph for mean scores over time
        graph_html = plot_scores_over_time(filtered_df)

        # Render the template with the grouped news and graph HTML
        return render_template('index.html', grouped_news=grouped_news, graph_html=graph_html)

    # If it's a GET request, just render the template without any data
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
