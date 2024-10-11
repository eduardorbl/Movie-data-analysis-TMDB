import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def preprocessing(save=False):
    """
    Movie data preprocessing function.
    
    Args:
    - save (bool): If True, saves the processed DataFrame to a CSV file. Otherwise, just returns the DataFrame.
    
    Returns:
    - df_selected (DataFrame): Processed DataFrame ready for analysis.
    """
    # Load data from CSV
    df = pd.read_csv('./data/movie_data.csv')

    # Select relevant attributes
    df_selected = df[['title', 'original_language', 'popularity', 'release_date', 'vote_average', 'vote_count', 'genre_ids']]

    # 1. One-Hot Encoding for 'original_language'
    encoder = OneHotEncoder()
    encoded_languages = encoder.fit_transform(df_selected[['original_language']]).toarray()

    # Convert the result to a DataFrame and merge with the original data
    language_cols = encoder.get_feature_names_out(['original_language'])
    df_encoded_languages = pd.DataFrame(encoded_languages, columns=language_cols)

    # Concatenate the encoded columns with the original DataFrame
    df_selected = pd.concat([df_selected, df_encoded_languages], axis=1)

    # Remove the original 'original_language' column
    df_selected.drop('original_language', axis=1, inplace=True)

    # 2. Normalize numerical attributes
    scaler = StandardScaler()

    # Apply normalization to numerical columns
    df_selected[['popularity', 'vote_average', 'vote_count']] = scaler.fit_transform(
        df_selected[['popularity', 'vote_average', 'vote_count']])

    # 3. Apply One-Hot Encoding to genre_ids

    # Transform the lists of genre_ids into binary columns
    df_selected['genre_ids'] = df_selected['genre_ids'].apply(lambda x: [int(i) for i in x.strip('[]').split(',')])

    # Expand the list of genre_ids into individual columns, ensuring the type is integer
    df_genres_encoded = pd.get_dummies(df_selected['genre_ids'].apply(pd.Series).stack().astype(int)).groupby(level=0).max()

    # Concatenate the genres with the original DataFrame
    df_selected = pd.concat([df_selected, df_genres_encoded], axis=1)

    # Remove the original genre_ids column
    df_selected.drop('genre_ids', axis=1, inplace=True)

    # Save the DataFrame if the save=True parameter is passed
    if save:
        df_selected.to_csv('./data/processed_movie_data.csv', index=False)
        print("File saved as 'processed_movie_data.csv'")
    
    # Remove the 'title' column
    df_selected.drop('title', axis=1, inplace=True)

    # Return the processed DataFrame
    return df_selected

# Example usage
# df_processed = preprocessing(save=True)  # Will save the CSV
# df_processed = preprocessing()  # Just returns the DataFrame without saving

if __name__ == '__main__':
    preprocessing(save=True)
