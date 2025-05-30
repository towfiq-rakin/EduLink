# PCA (Principal Component Analysis) is a technique for reducing the dimensionality of data.
# It transforms the original features into a new set of features (principal components) that capture the most variance in the data.
# In this script, PCA is used to reduce the student exam data to two dimensions for visualization,
# making it easier to see the separation between clusters of students.

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data/result.csv')

# Select exam columns
exam_cols = ['CT1', 'CT2', 'Mid-Term', 'CT3', 'CT4', 'Presentation']
X = df[exam_cols]

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=83)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Assign labels based on mean total score per cluster
df['Total'] = df[exam_cols].sum(axis=1)
cluster_means = df.groupby('Cluster')['Total'].mean().sort_values(ascending=False)
labels = {cluster_means.index[0]: 'Good', cluster_means.index[1]: 'Average', cluster_means.index[2]: 'Struggling'}
df['Group'] = df['Cluster'].map(labels)

# Print students in each group
for group in ['Good', 'Average', 'Struggling']:
    print(f"\n{group} students:")
    print(df[df['Group'] == group][['StudentID', 'Student Name', 'Total']])

# Plot clusters (using first two principal components for visualization)
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
components = pca.fit_transform(X_scaled)
plt.figure(figsize=(8,6))
for group, color in zip(['Good', 'Average', 'Struggling'], ['g', 'b', 'r']):
    idx = df['Group'] == group
    plt.scatter(components[idx, 0], components[idx, 1], label=group, alpha=0.7, c=color)
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.title('Student Clusters')
plt.legend()
plt.show()
