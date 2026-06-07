"""
Cluster Profiling Module
Profiles and analyzes customer clusters
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score

class ClusterProfiler:
    """Profiles and analyzes customer clusters"""
    
    def __init__(self, df, features_for_clustering, n_clusters_range=(2, 10)):
        """
        Initialize Cluster Profiler
        
        Args:
            df (DataFrame): Feature data for clustering
            features_for_clustering (list): Column names to use for clustering
            n_clusters_range (tuple): Range of clusters to evaluate
        """
        self.df = df.copy()
        self.features = features_for_clustering
        self.X = df[features_for_clustering]
        self.n_clusters_range = n_clusters_range
        self.kmeans = None
        self.clusters = None
        self.optimal_k = None
        
    def find_optimal_clusters(self):
        """
        Find optimal number of clusters using Elbow method and Silhouette score
        
        Returns:
            DataFrame: Metrics for different cluster counts
        """
        inertias = []
        silhouette_scores = []
        davies_bouldin_scores = []
        K_range = range(self.n_clusters_range[0], self.n_clusters_range[1] + 1)
        
        print("Evaluating different cluster numbers...")
        
        for k in K_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.X)
            
            inertias.append(kmeans.inertia_)
            sil_score = silhouette_score(self.X, kmeans.labels_)
            silhouette_scores.append(sil_score)
            db_score = davies_bouldin_score(self.X, kmeans.labels_)
            davies_bouldin_scores.append(db_score)
            
            print(f"  k={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.4f}, DB={db_score:.4f}")
        
        # Find optimal k (highest silhouette score)
        self.optimal_k = K_range[np.argmax(silhouette_scores)]
        
        metrics_df = pd.DataFrame({
            'N_Clusters': list(K_range),
            'Inertia': inertias,
            'Silhouette_Score': silhouette_scores,
            'Davies_Bouldin_Index': davies_bouldin_scores
        })
        
        print(f"\n✓ Optimal number of clusters: {self.optimal_k}")
        print(f"  (Based on highest Silhouette Score)")
        
        return metrics_df
    
    def fit_kmeans(self, n_clusters=None):
        """
        Fit K-Means clustering
        
        Args:
            n_clusters (int): Number of clusters (uses optimal if not specified)
        """
        if n_clusters is None:
            if self.optimal_k is None:
                self.find_optimal_clusters()
            n_clusters = self.optimal_k
        
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.df['Cluster'] = self.kmeans.fit_predict(self.X)
        self.clusters = self.df['Cluster']
        
        print(f"✓ K-Means clustering fitted with {n_clusters} clusters")
        print(f"  Inertia: {self.kmeans.inertia_:.2f}")
        print(f"  Silhouette Score: {silhouette_score(self.X, self.clusters):.4f}")
        
        return self.df
    
    def get_cluster_profiles(self):
        """
        Get detailed profiles of each cluster
        
        Returns:
            DataFrame: Summary statistics for each cluster
        """
        if self.clusters is None:
            print("Fit K-Means first using fit_kmeans()")
            return
        
        profiles = self.df.groupby('Cluster')[self.features].agg(['mean', 'std', 'min', 'max']).round(2)
        
        print("✓ Cluster profiles generated")
        print(f"\nCluster Profiles:\n{profiles}")
        
        return profiles
    
    def get_cluster_sizes(self):
        """Get size distribution of clusters"""
        if self.clusters is None:
            print("Fit K-Means first using fit_kmeans()")
            return
        
        sizes = self.df['Cluster'].value_counts().sort_index()
        pct = (sizes / len(self.df) * 100).round(2)
        
        size_df = pd.DataFrame({
            'Cluster': sizes.index,
            'Count': sizes.values,
            'Percentage': pct.values
        })
        
        print("✓ Cluster size distribution:")
        print(f"\n{size_df.to_string(index=False)}")
        
        return size_df
    
    def get_cluster_centers(self):
        """Get cluster centers"""
        if self.kmeans is None:
            print("Fit K-Means first using fit_kmeans()")
            return
        
        centers_df = pd.DataFrame(
            self.kmeans.cluster_centers_,
            columns=self.features
        )
        
        return centers_df
    
    def get_clustered_data(self):
        """Return data with cluster assignments"""
        return self.df
    
    def profile_by_segment(self, segment_column):
        """
        Profile clusters by another segment column
        
        Args:
            segment_column (str): Column name to cross-tabulate with clusters
        """
        if self.clusters is None:
            print("Fit K-Means first using fit_kmeans()")
            return
        
        cross_tab = pd.crosstab(self.df['Cluster'], self.df[segment_column], margins=True)
        
        return cross_tab
