import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
import matplotlib.pyplot as plt
import preprocessing
import get_genres

def elbow_method_formal(df, range_k=range(1, 300)):
    """
    Applies the Elbow Method in an automated way to find the optimal k.
    
    Args:
    - df (DataFrame): The pre-processed DataFrame
    
    Returns:
    - Best value of k based on the Elbow Method
    """
    distortions = []
    K = range_k
    
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df)
        distortions.append(kmeans.inertia_)
    
    # Plot of the Elbow Method
    plt.figure(figsize=(8, 6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Distortion (Inertia)')
    plt.title('Elbow Method for Optimal k')
    plt.savefig('./images/elbow_method.png')

    # Calculate the second derivative of distortions
    deltas = np.diff(distortions)
    second_deltas = np.diff(deltas)

    # Find the point where the second derivative is minimum (elbow)
    best_k = np.argmin(second_deltas) + 2
    
    print(f"The best value of k based on the Elbow Method is {best_k}")
    return best_k

def silhouette_method(df, range_k=range(2, 300)):
    """
    Determines the optimal number of clusters (k) using the Silhouette Score.
    
    Args:
    - df (DataFrame): The pre-processed DataFrame
    
    Returns:
    - Best value of k based on the Silhouette Score
    """
    silhouette_scores = []
    K = range_k
    
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(df)
        silhouette_avg = silhouette_score(df, labels)
        silhouette_scores.append(silhouette_avg)
    
    # Plot of Silhouette Score for each k
    plt.figure(figsize=(8, 6))
    plt.plot(K, silhouette_scores, 'bx-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score for Different Values of k')
    plt.savefig('./images/silhouette_score.png')
    
    # Return the best k (where the Silhouette Score is maximum)
    best_k = K[silhouette_scores.index(max(silhouette_scores))]
    print(f"The best value of k is {best_k} with Silhouette Score {max(silhouette_scores)}")
    return best_k

def apply_kmeans(df, n_clusters=3):
    """
    Applies K-Means to the processed DataFrame.
    
    Args:
    - df (DataFrame): The processed DataFrame
    - n_clusters (int): The number of clusters for K-Means
    
    Returns:
    - labels (array): Cluster labels for each data point
    - kmeans (KMeans object): The trained K-Means model
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(df)
    labels = kmeans.labels_
    return labels, kmeans

def save_kmeans_results(df_original, labels_silhouette, labels_elbow):
    """
    Saves the K-Means results in a CSV file along with the movie titles.
    
    Args:
    - df_original (DataFrame): The original movie data (including titles)
    - labels_silhouette (array): Cluster labels from the Silhouette method
    - labels_elbow (array): Cluster labels from the Elbow method
    
    Saves the CSV file with cluster labels for both methods.
    """
    genres_dict = get_genres.get_genres()
    df_original = get_genres.replace_genre_ids_with_names(df_original, genres_dict)
    
    result_df = df_original[['title', 'popularity', 'release_date', 'vote_average', 'vote_count', 'original_language', 'genre_names']].copy()
    result_df['Cluster_Silhouette'] = labels_silhouette
    result_df['Cluster_Elbow'] = labels_elbow
    
    result_df.to_csv('./data/movie_cluster_results_with_titles.csv', index=False)
    print("K-Means results saved in 'movie_cluster_results_with_titles.csv'.")

if __name__ == '__main__':
    df_processed = preprocessing.preprocessing(save=False)

    print("Determining the best k using Silhouette Score...")
    best_k_silhouette = silhouette_method(df_processed)

    print("Determining the best k using the formalized Elbow Method...")
    best_k_elbow = elbow_method_formal(df_processed)

    print(f"Best k according to Silhouette Score: {best_k_silhouette}")
    print(f"Best k according to the Elbow Method: {best_k_elbow}")
    
    print("Testing k from Silhouette")
    labels_k_silhouette, kmeans_model_k_silhouette = apply_kmeans(df_processed, n_clusters=best_k_silhouette)
    
    print("Testing k from Elbow")
    labels_k_elbow, kmeans_model_kelbow = apply_kmeans(df_processed, n_clusters=best_k_elbow)

    df_original = pd.read_csv('./data/movie_data.csv')

    save_kmeans_results(df_original, labels_k_silhouette, labels_k_elbow)