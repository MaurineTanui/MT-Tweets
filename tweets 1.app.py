import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Define a function to process chunks of data and plot the results
def process_data_in_chunks(url, chunk_size=10000):
    # Initialize empty dataframes to store results
    sentiment_counts = pd.DataFrame(columns=['sentiment', 'count'])
    airline_counts = pd.DataFrame(columns=['airline', 'count'])
    
    # Process the CSV in chunks
    for chunk in pd.read_csv(url, chunksize=chunk_size):
        # Process sentiment counts
        sentiment_chunk = chunk['airline_sentiment'].value_counts().reset_index()
        sentiment_chunk.columns = ['sentiment', 'count']
        sentiment_counts = pd.concat([sentiment_counts, sentiment_chunk], axis=0)
        
        # Process airline counts
        airline_chunk = chunk['airline'].value_counts().reset_index()
        airline_chunk.columns = ['airline', 'count']
        airline_counts = pd.concat([airline_counts, airline_chunk], axis=0)
    
    # After reading all chunks, aggregate counts
    sentiment_counts = sentiment_counts.groupby('sentiment')['count'].sum().reset_index()
    airline_counts = airline_counts.groupby('airline')['count'].sum().reset_index()

    return sentiment_counts, airline_counts

# URL to the CSV file
url = 'https://raw.githubusercontent.com/MaurineTanui/MT-Tweets/refs/heads/main/Tweets.csv'

# Process data in chunks
sentiment_counts, airline_counts = process_data_in_chunks(url)

# Plot the sentiment distribution using Plotly
fig = px.pie(sentiment_counts,
             values='count',
             names='sentiment',
             title='Sentiment Distribution')
fig.show()

# Plot the airline tweet counts using Seaborn
plt.figure(figsize=(10,6))
sns.barplot(x='airline', y='count', data=airline_counts, palette='pastel')
plt.xlabel('Airline')
plt.ylabel('Number of Tweets')
plt.title('Number of Tweets by Airline')
plt.show()
