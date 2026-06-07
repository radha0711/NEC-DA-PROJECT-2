"""
PCA (Principal Component Analysis) Module
Performs dimensionality reduction on customer features
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class PCAAnalysis:
    """Performs PCA for dimensionality reduction"""
    
    def __init__(self, df, n_components=2):
        """
        Initialize PCA Analysis
        
        Args:
            df (DataFrame): Feature data (numeric columns only)
            n_components (int): Number of principal components to retain
        """
        self.df = df.copy()
        self.n_components = n_components
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=n_components)
        self.scaled_data = None
        self.pca_data = None
        self.feature_importance = None
        
    def prepare_data(self, columns_to_exclude=None):
        """
        Prepare data for PCA by selecting numeric features
        
        Args:
            columns_to_exclude (list): Columns to exclude from analysis
        """
        if columns_to_exclude is None:
            columns_to_exclude = []
        
        # Select numeric columns excluding specified ones
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in columns_to_exclude]
        
        self.features = numeric_cols
        self.X = self.df[numeric_cols]
        
        print(f"✓ Selected {len(self.features)} features for PCA")
        print(f"  Features: {', '.join(self.features)}")
        
        return self.X
    
    def standardize_features(self):
        """Standardize features to zero mean and unit variance"""
        if not hasattr(self, 'X'):
            print("Prepare data first using prepare_data()")
            return
        
        self.scaled_data = self.scaler.fit_transform(self.X)
        print("✓ Features standardized (zero mean, unit variance)")
        
        return self.scaled_data
    
    def fit_pca(self):
        """Fit PCA model"""
        if self.scaled_data is None:
            print("Standardize features first using standardize_features()")
            return
        
        self.pca.fit(self.scaled_data)
        
        print(f"✓ PCA fitted with {self.n_components} components")
        print(f"\nExplained Variance Ratio:\n{self.pca.explained_variance_ratio_}")
        print(f"Cumulative Variance Explained: {self.pca.explained_variance_ratio_.sum():.4f}")
        
        return self.pca
    
    def transform_data(self):
        """Transform data using fitted PCA"""
        if self.pca.components_ is None or self.scaled_data is None:
            print("Fit PCA first using fit_pca()")
            return
        
        self.pca_data = self.pca.transform(self.scaled_data)
        
        # Create dataframe with PCA components
        pca_columns = [f'PC{i+1}' for i in range(self.n_components)]
        self.pca_df = pd.DataFrame(data=self.pca_data, columns=pca_columns)
        
        print(f"✓ Data transformed to {self.n_components} principal components")
        print(f"\nPCA Data Shape: {self.pca_df.shape}")
        print(f"\nFirst few rows:\n{self.pca_df.head()}")
        
        return self.pca_df
    
    def get_feature_importance(self):
        """
        Get feature importance (loadings) for each principal component
        
        Returns:
            DataFrame: Feature contributions to each principal component
        """
        if self.pca.components_ is None:
            print("Fit PCA first using fit_pca()")
            return
        
        loadings = pd.DataFrame(
            self.pca.components_.T,
            columns=[f'PC{i+1}' for i in range(self.n_components)],
            index=self.features
        )
        
        self.feature_importance = loadings
        
        print("✓ Feature importance calculated")
        print(f"\nFeature Loadings (contributions to PCs):\n{loadings}")
        
        return loadings
    
    def get_variance_explained(self):
        """Get variance explained by each component"""
        if self.pca is None:
            print("Fit PCA first using fit_pca()")
            return
        
        variance_df = pd.DataFrame({
            'Component': [f'PC{i+1}' for i in range(self.n_components)],
            'Explained_Variance': self.pca.explained_variance_ratio_,
            'Cumulative_Variance': np.cumsum(self.pca.explained_variance_ratio_)
        })
        
        return variance_df
    
    def get_pca_data(self):
        """Return transformed PCA data"""
        return self.pca_df
    
    def get_original_features_stats(self):
        """Get statistics of original features"""
        return self.X.describe()
