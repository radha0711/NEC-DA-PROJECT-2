"""
Visualization Module
Creates comprehensive visualizations for customer segmentation analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

class Visualizer:
    """Creates visualizations for analysis results"""
    
    def __init__(self, output_dir='output'):
        """
        Initialize Visualizer
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
    
    def plot_rfm_distribution(self, rfm_data):
        """Plot RFM distribution"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        
        axes[0].hist(rfm_data['Recency'], bins=30, color='skyblue', edgecolor='black')
        axes[0].set_title('Recency Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Days Since Last Purchase')
        axes[0].set_ylabel('Number of Customers')
        
        axes[1].hist(rfm_data['Frequency'], bins=30, color='lightgreen', edgecolor='black')
        axes[1].set_title('Frequency Distribution', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Number of Purchases')
        axes[1].set_ylabel('Number of Customers')
        
        axes[2].hist(rfm_data['Monetary'], bins=30, color='salmon', edgecolor='black')
        axes[2].set_title('Monetary Distribution', fontsize=12, fontweight='bold')
        axes[2].set_xlabel('Total Amount Spent (INR)')
        axes[2].set_ylabel('Number of Customers')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'rfm_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ RFM distribution plot saved")
        plt.close()
    
    def plot_rfm_scatter(self, rfm_data):
        """Plot RFM relationship scatter plots"""
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # Recency vs Frequency
        scatter1 = axes[0].scatter(rfm_data['Recency'], rfm_data['Frequency'], 
                                   c=rfm_data['Monetary'], cmap='viridis', s=100, alpha=0.6)
        axes[0].set_xlabel('Recency (Days)', fontsize=11)
        axes[0].set_ylabel('Frequency (Purchases)', fontsize=11)
        axes[0].set_title('Recency vs Frequency', fontsize=12, fontweight='bold')
        plt.colorbar(scatter1, ax=axes[0], label='Monetary (INR)')
        
        # Frequency vs Monetary
        scatter2 = axes[1].scatter(rfm_data['Frequency'], rfm_data['Monetary'],
                                   c=rfm_data['Recency'], cmap='plasma', s=100, alpha=0.6)
        axes[1].set_xlabel('Frequency (Purchases)', fontsize=11)
        axes[1].set_ylabel('Monetary (INR)', fontsize=11)
        axes[1].set_title('Frequency vs Monetary', fontsize=12, fontweight='bold')
        plt.colorbar(scatter2, ax=axes[1], label='Recency (Days)')
        
        # Recency vs Monetary
        scatter3 = axes[2].scatter(rfm_data['Recency'], rfm_data['Monetary'],
                                   c=rfm_data['Frequency'], cmap='coolwarm', s=100, alpha=0.6)
        axes[2].set_xlabel('Recency (Days)', fontsize=11)
        axes[2].set_ylabel('Monetary (INR)', fontsize=11)
        axes[2].set_title('Recency vs Monetary', fontsize=12, fontweight='bold')
        plt.colorbar(scatter3, ax=axes[2], label='Frequency')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'rfm_relationships.png', dpi=300, bbox_inches='tight')
        print("✓ RFM relationships plot saved")
        plt.close()
    
    def plot_segment_distribution(self, rfm_scores):
        """Plot customer segment distribution"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        segment_counts = rfm_scores['Segment'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(segment_counts)))
        
        # Bar plot
        axes[0].bar(segment_counts.index, segment_counts.values, color=colors, edgecolor='black')
        axes[0].set_title('Customer Segment Distribution', fontsize=12, fontweight='bold')
        axes[0].set_xlabel('Segment', fontsize=11)
        axes[0].set_ylabel('Number of Customers', fontsize=11)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Pie chart
        axes[1].pie(segment_counts.values, labels=segment_counts.index, autopct='%1.1f%%',
                   colors=colors, startangle=90)
        axes[1].set_title('Customer Segment Percentage', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'segment_distribution.png', dpi=300, bbox_inches='tight')
        print("✓ Segment distribution plot saved")
        plt.close()
    
    def plot_pca_components(self, pca_data, clusters=None):
        """Plot PCA components"""
        if pca_data.shape[1] < 2:
            print("Need at least 2 principal components for visualization")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        if clusters is not None:
            scatter = ax.scatter(pca_data.iloc[:, 0], pca_data.iloc[:, 1],
                               c=clusters, cmap='viridis', s=100, alpha=0.6, edgecolors='black')
            plt.colorbar(scatter, ax=ax, label='Cluster')
            title = 'PCA: First Two Components (with Clusters)'
        else:
            ax.scatter(pca_data.iloc[:, 0], pca_data.iloc[:, 1],
                      s=100, alpha=0.6, edgecolors='black')
            title = 'PCA: First Two Components'
        
        ax.set_xlabel(f'{pca_data.columns[0]}', fontsize=11)
        ax.set_ylabel(f'{pca_data.columns[1]}', fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'pca_components.png', dpi=300, bbox_inches='tight')
        print("✓ PCA components plot saved")
        plt.close()
    
    def plot_cluster_analysis(self, clustered_data, features):
        """Plot cluster analysis with feature distributions"""
        n_features = len(features)
        fig, axes = plt.subplots((n_features + 1) // 2, 2, figsize=(15, 3 * ((n_features + 1) // 2)))
        axes = axes.flatten() if n_features > 1 else [axes]
        
        for idx, feature in enumerate(features):
            clustered_data.boxplot(column=feature, by='Cluster', ax=axes[idx])
            axes[idx].set_title(f'{feature} by Cluster', fontsize=11, fontweight='bold')
            axes[idx].set_xlabel('Cluster')
            axes[idx].set_ylabel(feature)
        
        # Remove empty subplots
        for idx in range(len(features), len(axes)):
            fig.delaxes(axes[idx])
        
        plt.suptitle('Feature Distribution by Cluster', fontsize=13, fontweight='bold', y=1.00)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'cluster_analysis.png', dpi=300, bbox_inches='tight')
        print("✓ Cluster analysis plot saved")
        plt.close()
    
    def plot_variance_explained(self, variance_df):
        """Plot cumulative variance explained by PCA"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.plot(variance_df['Component'], variance_df['Cumulative_Variance'], 
               marker='o', linewidth=2, markersize=8, color='darkblue', label='Cumulative')
        ax.bar(variance_df['Component'], variance_df['Explained_Variance'], 
              alpha=0.3, color='skyblue', label='Individual')
        
        ax.set_xlabel('Principal Component', fontsize=11)
        ax.set_ylabel('Variance Explained', fontsize=11)
        ax.set_title('Variance Explained by Principal Components', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 1])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'variance_explained.png', dpi=300, bbox_inches='tight')
        print("✓ Variance explained plot saved")
        plt.close()
    
    def plot_cluster_sizes(self, cluster_sizes):
        """Plot cluster size distribution"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        colors = plt.cm.Set2(np.linspace(0, 1, len(cluster_sizes)))
        bars = ax.bar(cluster_sizes['Cluster'].astype(str), cluster_sizes['Count'], 
                     color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Cluster', fontsize=11)
        ax.set_ylabel('Number of Customers', fontsize=11)
        ax.set_title('Cluster Size Distribution', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'cluster_sizes.png', dpi=300, bbox_inches='tight')
        print("✓ Cluster sizes plot saved")
        plt.close()
    
    def create_summary_report(self, metrics_dict):
        """Create a text summary report"""
        report_path = self.output_dir / 'analysis_summary.txt'
        
        with open(report_path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("MARKET & CUSTOMER SEGMENTATION ANALYSIS REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            for section, content in metrics_dict.items():
                f.write(f"\n{section}\n")
                f.write("-" * 70 + "\n")
                f.write(str(content) + "\n")
        
        print(f"✓ Summary report saved to {report_path}")