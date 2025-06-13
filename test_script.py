#!/usr/bin/env python
"""
Student Performance Analysis Script

This script performs cluster analysis on student exam data to identify performance groups.
It uses Principal Component Analysis (PCA) for dimensionality reduction and visualization,
and K-means clustering to group students by performance.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
from datetime import datetime


def load_data(file_path, index_col=0, fill_na_value=0):
    """
    Load data from CSV file and preprocess it.

    Args:
        file_path (str): Path to the CSV file
        index_col (int): Column to use as index
        fill_na_value: Value to use for filling NA/NaN values

    Returns:
        pd.DataFrame: Preprocessed dataframe
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")

    df = pd.read_csv(file_path, index_col=index_col)
    df.fillna(fill_na_value, inplace=True)

    # Optional preprocessing steps
    if 'Mid-Term' in df.columns:
        df['Midterm_Scaled'] = df['Mid-Term'] / 2

    # Best 3 CT average calculation
    ct_columns = ['CT1', 'CT2', 'CT3', 'CT4']
    valid_ct_cols = [col for col in ct_columns if col in df.columns]

    ct_scores = []
    for index, row in df.iterrows():
        scores = [row[col] for col in valid_ct_cols if pd.notna(row[col])]
        scores.sort(reverse=True)
        best_3_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else (sum(scores) / len(scores) if scores else 0)
        ct_scores.append(best_3_avg)

    df['CT_Avg'] = ct_scores

    # Delete individual CT columns after calculating the average
    for col in valid_ct_cols:
        if col in df.columns:
            df = df.drop(columns=[col])

    return df


def perform_clustering(df, exam_columns, n_clusters=3, random_state=83):
    """
    Perform clustering on student exam data.

    Args:
        df (pd.DataFrame): Dataframe containing student data
        exam_columns (list): List of column names containing exam scores
        n_clusters (int): Number of clusters to create
        random_state (int): Random seed for reproducibility

    Returns:
        tuple: (Updated dataframe with cluster assignments, cluster labels dictionary)
    """
    # Extract exam data
    X = df[exam_columns]

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # Calculate total score and assign group labels
    df['Total'] = df[exam_columns].sum(axis=1)
    cluster_means = df.groupby('Cluster')['Total'].mean().sort_values(ascending=False)

    # Create label mapping based on performance
    if n_clusters == 3:
        labels = {
            cluster_means.index[0]: 'Good',
            cluster_means.index[1]: 'Average',
            cluster_means.index[2]: 'Struggling'
        }
    else:
        # Generate generic labels for any number of clusters
        labels = {
            idx: f"Group {i+1}"
            for i, idx in enumerate(cluster_means.index)
        }

    df['Group'] = df['Cluster'].map(labels)

    return df, labels, X_scaled


def visualize_clusters(df, X_scaled, groups, output_path=None):
    """
    Visualize clusters using PCA for dimensionality reduction.

    Args:
        df (pd.DataFrame): Dataframe with cluster assignments
        X_scaled (np.array): Scaled feature matrix
        groups (list): List of group names
        output_path (str, optional): Path to save the plot image
    """
    # Reduce dimensions with PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(X_scaled)

    # Plot the clusters
    plt.figure(figsize=(10, 8))
    colors = ['g', 'b', 'r', 'c', 'm', 'y', 'k']  # Support for more clusters

    for i, group in enumerate(groups):
        idx = df['Group'] == group
        plt.scatter(
            components[idx, 0],
            components[idx, 1],
            label=group,
            alpha=0.7,
            c=colors[i % len(colors)]
        )

    # Add explained variance information
    explained_variance = pca.explained_variance_ratio_
    plt.xlabel(f'PCA 1 ({explained_variance[0]:.2%} variance)')
    plt.ylabel(f'PCA 2 ({explained_variance[1]:.2%} variance)')
    plt.title('Student Performance Clusters')
    plt.legend()
    plt.grid(alpha=0.3)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        print(f"Plot saved to: {output_path}")

    plt.show()


def print_group_statistics(df, groups, id_column='StudentID', name_column='Student Name'):
    """
    Print statistics for each group.

    Args:
        df (pd.DataFrame): Dataframe with group assignments
        groups (list): List of group names
        id_column (str): Name of the ID column
        name_column (str): Name of the name column
    """
    print("\n==== Student Group Statistics ====")

    for group in groups:
        group_df = df[df['Group'] == group]
        print(f"\n{group} students ({len(group_df)} total):")
        print(f"Average total score: {group_df['Total'].mean():.2f}")
        print(f"Score range: {group_df['Total'].min():.2f} - {group_df['Total'].max():.2f}")

        # Print student details
        print("\nStudent details:")
        columns_to_show = [id_column, name_column, 'Total']
        print(group_df[columns_to_show].sort_values('Total', ascending=False).head(10))
        if len(group_df) > 10:
            print(f"... and {len(group_df) - 10} more students")


# Main execution code
if __name__ == "__main__":
    # Configuration - modify these variables as needed
    DATA_FILE = 'data/result.csv'
    # EXAM_COLUMNS = ['CT1', 'CT2', 'Mid-Term', 'CT3', 'CT4', 'Presentation', 'Attendance']
    N_CLUSTERS = 3
    OUTPUT_DIR = 'output'  # Set to None if you don't want to save outputs

    # Step 1: Load the data
    print(f"Loading data from: {DATA_FILE}")
    df = load_data(DATA_FILE)
    print("Data sample:")
    print(df.head())
    EXAM_COLUMNS = df.columns.drop(['StudentID', 'Student Name'])

    # Step 2: Perform clustering analysis
    print(f"\nAnalyzing the following assessment components: {EXAM_COLUMNS}")
    df, labels, X_scaled = perform_clustering(df, EXAM_COLUMNS, n_clusters=N_CLUSTERS)

    # Step 3: Get the groups in order from highest to lowest performance
    groups = sorted(df['Group'].unique(),
                  key=lambda x: ['Good', 'Average', 'Struggling'].index(x)
                  if x in ['Good', 'Average', 'Struggling'] else 999)

    # Step 4: Print statistics for each group
    print_group_statistics(df, groups)

    # Step 5: Visualize the clusters
    plot_path = None
    if OUTPUT_DIR:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plot_path = os.path.join(OUTPUT_DIR, f"student_clusters_{timestamp}.png")

    visualize_clusters(df, X_scaled, groups, output_path=plot_path)

    # Step 6: Save results if output directory is specified
    if OUTPUT_DIR:
        results_path = os.path.join(OUTPUT_DIR, f"student_analysis_{timestamp}.csv")
        os.makedirs(os.path.dirname(results_path), exist_ok=True)
        df.to_csv(results_path)
        print(f"Results saved to: {results_path}")

    print("\nAnalysis completed successfully!")
