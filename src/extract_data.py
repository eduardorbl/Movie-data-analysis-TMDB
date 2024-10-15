import requests
import pandas as pd
import sys
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")  # Get the API key from environment variables

# Base URL of the API
base_url = "https://api.themoviedb.org/3/discover/movie"
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Request parameters
params = {
    "include_adult": "false",
    "include_video": "false",
    "language": "en-US",
    "sort_by": "vote_count.desc",
    "page": 1
}

# List to store the data
data_list = []

# Total number of pages to be read
total_pages = 100

# Loop to collect data from multiple pages
for page in range(1, total_pages + 1):
    params['page'] = page
    response = requests.get(base_url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for movie in data['results']:
            # Extract the necessary attributes
            movie_data = {
                'id': movie['id'],
                'title': movie['title'],
                'original_title': movie['original_title'],
                'original_language': movie['original_language'],
                'overview': movie['overview'],
                'popularity': movie['popularity'],
                'release_date': movie['release_date'],
                'vote_average': movie['vote_average'],
                'vote_count': movie['vote_count'],
                'genre_ids': movie['genre_ids'],
            }
            data_list.append(movie_data)
        
        # Calculate and print the percentage of pages read
        percent_complete = (page / total_pages) * 100
        sys.stdout.write(f"\rProgress: {percent_complete:.2f}%")
        sys.stdout.flush()
    else:
        print(f"Error on page {page}: {response.status_code}")

print("\nData collection completed.")

# Create DataFrame with the collected data
df = pd.DataFrame(data_list)

# Remove duplicate records
df.drop_duplicates(subset='id', inplace=True)

# Handle missing values
df['overview'].fillna('N/A', inplace=True)
df.dropna(subset=['release_date', 'vote_average'], inplace=True)

# Convert the 'release_date' column to datetime type
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Convert numeric columns to numeric type
df[['vote_average', 'vote_count', 'popularity']] = df[['vote_average', 'vote_count', 'popularity']].apply(pd.to_numeric, errors='coerce')

# Remove whitespace and convert the title to lowercase
df['title'] = df['title'].str.strip().str.lower()

# Save the data to a CSV file
df.to_csv("./data/movie_data.csv", index=False)

# Display the first records
print(df.head())