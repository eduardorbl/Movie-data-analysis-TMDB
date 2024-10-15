import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import os

# Load the CSV file
df = pd.read_csv('./data/movie_cluster_results_with_titles.csv')

# Convert 'release_date' to datetime format, if necessary
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Ensure all numeric columns are present
df = df.dropna(subset=['popularity', 'vote_average', 'vote_count'])

# Define clustering methods
cluster_methods = ['Cluster_Silhouette', 'Cluster_Elbow']
cluster_titles = {
    'Cluster_Silhouette': 'Silhouette Clustering',
    'Cluster_Elbow': 'Elbow Clustering'
}

# Create the plots directory if it doesn't exist
plots_dir = './plots'
os.makedirs(plots_dir, exist_ok=True)

# Loop to create plots for each clustering method
for method in cluster_methods:
    print(f"Generating plots for {cluster_titles[method]}...")

    # Pairwise Plot (Scatter Matrix)
    print(f"Generating Pairwise Plot for {cluster_titles[method]}...")
    columns_to_plot = ['popularity', 'vote_average', 'vote_count']
    fig_pairwise = px.scatter_matrix(
        df,
        dimensions=columns_to_plot,
        color=method,
        hover_data=['title', 'genre_names', 'release_date'],
        title=f'Pairwise Relationships Between Features ({cluster_titles[method]})'
    )
    fig_pairwise.write_html(f"{plots_dir}/pairwise_plot_{method}.html")
    fig_pairwise.show()

    # 3D Scatter Plot
    print(f"Generating 3D Scatter Plot for {cluster_titles[method]}...")
    fig_3d = px.scatter_3d(
        df, 
        x='popularity', 
        y='vote_average', 
        z='vote_count', 
        color=method,
        hover_data=['title', 'genre_names', 'release_date'],
        title=f'3D Scatter Plot of Movie Clusters ({cluster_titles[method]})',
        size='popularity',
        template='plotly_dark'
    )
    fig_3d.write_html(f"{plots_dir}/3d_scatter_plot_{method}.html")
    fig_3d.show()

    # Parallel Coordinates Plot
    print(f"Generating Parallel Coordinates Plot for {cluster_titles[method]}...")
    fig_parallel = px.parallel_coordinates(
        df, 
        dimensions=['popularity', 'vote_average', 'vote_count'],
        color=method,
        title=f'Parallel Coordinates Plot of Movie Features by Clusters ({cluster_titles[method]})'
    )
    fig_parallel.write_html(f"{plots_dir}/parallel_coordinates_plot_{method}.html")
    fig_parallel.show()

    # Violin Plot
    print(f"Generating Violin Plot for {cluster_titles[method]}...")
    fig_violin = px.violin(
        df, 
        x=method, 
        y='vote_average', 
        box=True,
        points="all",
        hover_data=['title', 'genre_names', 'release_date'],
        title=f'Distribution of Vote Averages by {cluster_titles[method]}'
    )
    fig_violin.write_html(f"{plots_dir}/violin_plot_{method}.html")
    fig_violin.show()

    # Heatmap of Feature Correlations
    print(f"Generating Heatmap of Feature Correlations for {cluster_titles[method]}...")
    corr_matrix = df[['popularity', 'vote_average', 'vote_count']].corr()
    fig_heatmap = ff.create_annotated_heatmap(
        z=corr_matrix.values, 
        x=list(corr_matrix.columns), 
        y=list(corr_matrix.columns),
        colorscale='Viridis',
        showscale=True
    )
    fig_heatmap.write_html(f"{plots_dir}/heatmap_{method}.html")
    fig_heatmap.show()

print("All plots for both clustering methods have been successfully generated.")