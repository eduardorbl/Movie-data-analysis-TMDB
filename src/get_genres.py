import requests
import sys
import os
from dotenv import load_dotenv

def get_genres():
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")  # Get the API key from environment variables

    # API URL to get the genres
    url = "https://api.themoviedb.org/3/genre/movie/list"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Make the request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data from API: {response.status_code}")
        sys.exit(1)
    else:
        # Extract data from the response
        genres_data = response.json()
        genres_dict = {genre['id']: genre['name'] for genre in genres_data['genres']}
        return genres_dict
    
def replace_genre_ids_with_names(df, genres_dict):
    """
    Replaces genre IDs with corresponding names in the DataFrame.
    
    Args:
    - df (DataFrame): The original DataFrame containing the 'genre_ids' column.
    - genres_dict (dict): Dictionary mapping genre IDs to names.
    
    Returns:
    - df (DataFrame): DataFrame with the 'genre_names' column containing the genre names.
    """
    
    def map_genre_ids(genre_ids):
        try:
            if isinstance(genre_ids, list):
                return [genres_dict.get(genre_id, "Unknown") for genre_id in genre_ids]
            elif isinstance(genre_ids, str):
                genre_ids_list = eval(genre_ids)
                if isinstance(genre_ids_list, list):
                    return [genres_dict.get(genre_id, "Unknown") for genre_id in genre_ids_list]
            return []
        except:
            return []
    
    df['genre_names'] = df['genre_ids'].apply(map_genre_ids)
    
    return df