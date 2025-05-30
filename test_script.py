# K means clustering example
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/result.csv')
df_filtered = df.drop(['Sl. No', 'StudentID', 'Student Name', 'CT3', 'CT4', 'Mid-Term', 'Presentation'], axis=1)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df_filtered)
k=3
kmeans = KMeans(n_clusters=k, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_features)

plt.scatter(df['CT1'], df['CT2'], c=df['Cluster'], cmap='viridis')
plt.title('K-Means Clustering')
plt.xlabel('CT1')
plt.ylabel('CT2')
plt.show()
