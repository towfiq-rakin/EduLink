import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os
from datetime import datetime

class ClusterAnalyzer:
    def __init__(self, data_file):
        self.data_file = os.path.normpath(data_file)  # Normalize path
        self.data = None
        self.processed_data = None
        self.clusters = None
        self.labels = None
        self.X_scaled = None
        # Use os.path.abspath to get absolute path and normalize it
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.output_dir = os.path.join(root_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def load_data(self, index_col=0, fill_na_value=0):
        """
        Load data from CSV file and preprocess it.

        Args:
            index_col (int): Column to use as index
            fill_na_value: Value to use for filling NA/NaN values

        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            if not os.path.exists(self.data_file):
                raise FileNotFoundError(f"Data file not found: {self.data_file}")

            self.data = pd.read_csv(self.data_file, index_col=index_col)
            self.data.fillna(fill_na_value, inplace=True)

            # Optional preprocessing steps
            if 'Mid-Term' in self.data.columns:
                self.data['Midterm_Scaled'] = self.data['Mid-Term'] / 2

            # Best 3 CT average calculation
            ct_columns = ['CT1', 'CT2', 'CT3', 'CT4']
            valid_ct_cols = [col for col in ct_columns if col in self.data.columns]

            ct_scores = []
            for index, row in self.data.iterrows():
                scores = [row[col] for col in valid_ct_cols if pd.notna(row[col])]
                scores.sort(reverse=True)
                best_3_avg = sum(scores[:3]) / 3 if len(scores) >= 3 else (sum(scores) / len(scores) if scores else 0)
                # Round to 2 decimal places
                best_3_avg = round(best_3_avg, 2)
                ct_scores.append(best_3_avg)

            self.data['CT_Avg'] = ct_scores

            # Delete individual CT columns after calculating the average
            for col in valid_ct_cols:
                if col in self.data.columns:
                    self.data = self.data.drop(columns=[col])

            self.processed_data = self.data.copy()
            print(f"Data loaded successfully from {self.data_file}")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def perform_clustering(self, n_clusters=3, random_state=83):
        """
        Perform clustering on student exam data.

        Args:
            n_clusters (int): Number of clusters to create
            random_state (int): Random seed for reproducibility

        Returns:
            bool: True if clustering was successful, False otherwise
        """
        try:
            if self.processed_data is None:
                raise ValueError("Data not loaded. Please load the data first.")

            # Get assessment columns (excluding student ID and name)
            exam_columns = self.processed_data.columns.drop(['StudentID', 'Student Name'])

            # Extract exam data
            X = self.processed_data[exam_columns]

            # Standardize features
            scaler = StandardScaler()
            self.X_scaled = scaler.fit_transform(X)

            # KMeans clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
            self.processed_data['Cluster'] = kmeans.fit_predict(self.X_scaled)

            # Calculate total score and assign group labels
            self.processed_data['Total'] = self.processed_data[exam_columns].sum(axis=1)
            cluster_means = self.processed_data.groupby('Cluster')['Total'].mean().sort_values(ascending=False)

            # Create label mapping based on performance
            if n_clusters == 3:
                self.labels = {
                    cluster_means.index[0]: 'Good',
                    cluster_means.index[1]: 'Average',
                    cluster_means.index[2]: 'Struggling'
                }
            else:
                # Generate generic labels for any number of clusters
                self.labels = {
                    idx: f"Group {i+1}"
                    for i, idx in enumerate(cluster_means.index)
                }

            self.processed_data['Group'] = self.processed_data['Cluster'].map(self.labels)

            # Get the groups in order from highest to lowest performance
            self.groups = sorted(self.processed_data['Group'].unique(),
                              key=lambda x: ['Good', 'Average', 'Struggling'].index(x)
                              if x in ['Good', 'Average', 'Struggling'] else 999)

            return True
        except Exception as e:
            print(f"Error performing clustering: {e}")
            return False

    def visualize_clusters(self):
        """
        Visualize clusters using PCA for dimensionality reduction.

        Returns:
            str: Path to the saved plot image
        """
        try:
            if self.processed_data is None or self.X_scaled is None:
                raise ValueError("Clustering has not been performed. Please perform clustering first.")

            # Reduce dimensions with PCA
            pca = PCA(n_components=2)
            components = pca.fit_transform(self.X_scaled)

            # Plot the clusters
            plt.figure(figsize=(10, 8))
            colors = ['g', 'b', 'r', 'c', 'm', 'y', 'k']  # Support for more clusters

            for i, group in enumerate(self.groups):
                idx = self.processed_data['Group'] == group
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

            plot_path = os.path.join(self.output_dir, f"student_clusters_{self.timestamp}.png")
            plt.savefig(plot_path, bbox_inches='tight', dpi=300)
            plt.close()

            print(f"Cluster visualization saved to: {plot_path}")
            return plot_path
        except Exception as e:
            print(f"Error visualizing clusters: {e}")
            return None

    def save_results(self):
        """
        Save clustered results to a CSV file.

        Returns:
            str: Path to the saved CSV file
        """
        try:
            if self.processed_data is None:
                raise ValueError("Clustering has not been performed. Please perform clustering first.")

            results_path = os.path.join(self.output_dir, f"student_analysis_{self.timestamp}.csv")
            self.processed_data.to_csv(results_path)
            print(f"Clustering results saved to: {results_path}")
            return results_path
        except Exception as e:
            print(f"Error saving results: {e}")
            return None

    def print_group_statistics(self, id_column='StudentID', name_column='Student Name'):
        """
        Print statistics for each group.

        Args:
            id_column (str): Name of the ID column
            name_column (str): Name of the name column

        Returns:
            dict: Statistics for each group
        """
        if self.processed_data is None:
            raise ValueError("Clustering has not been performed. Please perform clustering first.")

        stats = {}
        print("\n==== Student Group Statistics ====")

        for group in self.groups:
            group_df = self.processed_data[self.processed_data['Group'] == group]
            print(f"\n{group} students ({len(group_df)} total):")
            print(f"Average total score: {group_df['Total'].mean():.2f}")
            print(f"Score range: {group_df['Total'].min():.2f} - {group_df['Total'].max():.2f}")

            # Collect statistics
            stats[group] = {
                'count': len(group_df),
                'avg_score': group_df['Total'].mean(),
                'min_score': group_df['Total'].min(),
                'max_score': group_df['Total'].max(),
                'students': []
            }

            # Print student details
            print("\nStudent details:")
            columns_to_show = [id_column, name_column, 'Total']
            top_students = group_df[columns_to_show].sort_values('Total', ascending=False).head(10)
            print(top_students)

            # Add students to stats
            for _, student in top_students.iterrows():
                stats[group]['students'].append({
                    'id': student[id_column],
                    'name': student[name_column],
                    'total': student['Total']
                })

            if len(group_df) > 10:
                print(f"... and {len(group_df) - 10} more students")

        return stats

    def generate_cluster_report(self):
        """
        Generate a detailed report on the clustering results.

        Returns:
            str: Path to the saved report file
        """
        if self.processed_data is None:
            raise ValueError("Clustering has not been performed. Please perform clustering first.")

        report_path = os.path.join(self.output_dir, f"cluster_analysis_report_{self.timestamp}.txt")

        with open(report_path, 'w') as f:
            f.write("="*80 + "\n")
            f.write("EDULINK - CLUSTER ANALYSIS REPORT\n")
            f.write("="*80 + "\n\n")

            f.write("CLUSTER SUMMARY:\n")
            f.write("-"*40 + "\n")
            f.write(f"Total Students: {len(self.processed_data)}\n")
            f.write(f"Number of Clusters: {len(self.groups)}\n")
            f.write(f"Cluster Labels: {', '.join(self.groups)}\n\n")

            # Group statistics
            for group in self.groups:
                group_df = self.processed_data[self.processed_data['Group'] == group]
                f.write(f"\n{group.upper()} GROUP STATISTICS:\n")
                f.write("-"*40 + "\n")
                f.write(f"Number of Students: {len(group_df)}\n")
                f.write(f"Average Total Score: {group_df['Total'].mean():.2f}\n")
                f.write(f"Score Range: {group_df['Total'].min():.2f} - {group_df['Total'].max():.2f}\n")

                # Top 5 students in the group
                f.write("\nTop 5 Students in this Group:\n")
                top_students = group_df.sort_values('Total', ascending=False).head(5)
                for i, (_, student) in enumerate(top_students.iterrows(), 1):
                    f.write(f"{i}. {student['Student Name']} - Total Score: {student['Total']:.2f}\n")

            f.write("\n" + "="*80 + "\n")
            f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n")

        print(f"Cluster analysis report saved to: {report_path}")
        return report_path

    def run_full_analysis(self, n_clusters=3):
        """
        Run the complete clustering workflow.

        Args:
            n_clusters (int): Number of clusters to create

        Returns:
            dict: Paths to generated files and statistics
        """
        results = {
            'success': False,
            'cluster_plot': None,
            'csv_file': None,
            'report_file': None,
            'statistics': None
        }

        try:
            # Step 1: Load and preprocess data
            if not self.load_data():
                return results

            # Step 2: Perform clustering
            if not self.perform_clustering(n_clusters=n_clusters):
                return results

            # Step 3: Visualize clusters
            results['cluster_plot'] = self.visualize_clusters()

            # Step 4: Save results to CSV
            results['csv_file'] = self.save_results()

            # Step 5: Generate report
            results['report_file'] = self.generate_cluster_report()

            # Step 6: Calculate statistics
            results['statistics'] = self.print_group_statistics()

            results['success'] = True
            return results
        except Exception as e:
            print(f"Error running full analysis: {e}")
            return results
