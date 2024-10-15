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

    # One-Hot Encoding for 'original_language'
    encoder = OneHotEncoder()
    encoded_languages = encoder.fit_transform(df_selected[['original_language']]).toarray()
    language_cols = encoder.get_feature_names_out(['original_language'])
    df_encoded_languages = pd.DataFrame(encoded_languages, columns=language_cols)
    df_selected = pd.concat([df_selected, df_encoded_languages], axis=1)
    df_selected.drop('original_language', axis=1, inplace=True)

    # Convert 'release_date' to numeric (days since 1970-01-01)
    df_selected['release_date'] = pd.to_datetime(df_selected['release_date'], errors='coerce')
    df_selected['release_date'] = (df_selected['release_date'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')

    # Normalize numeric attributes
    scaler = StandardScaler()
    df_selected[['popularity', 'vote_average', 'vote_count', 'release_date']] = scaler.fit_transform(
        df_selected[['popularity', 'vote_average', 'vote_count', 'release_date']])

    # One-Hot Encoding for 'genre_ids'
    df_selected['genre_ids'] = df_selected['genre_ids'].apply(lambda x: [int(i) for i in x.strip('[]').split(',')])
    df_genres_encoded = pd.get_dummies(df_selected['genre_ids'].apply(pd.Series).stack().astype(int)).groupby(level=0).max()
    df_selected = pd.concat([df_selected, df_genres_encoded], axis=1)
    df_selected.drop('genre_ids', axis=1, inplace=True)
    df_selected.drop('title', axis=1, inplace=True)
    df_selected.columns = df_selected.columns.astype(str)

    # Save the processed DataFrame if the save=True parameter is passed
    if save:
        df_selected.to_csv('./data/processed_movie_data.csv', index=False)
        print("File saved as 'processed_movie_data.csv'")

    return df_selected

if __name__ == '__main__':
    preprocessing(save=True)