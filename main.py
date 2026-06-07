import pandas as pd
import os

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt


def main():

    print("=" * 60)
    print("MARKET & CUSTOMER SEGMENTATION ANALYSIS")
    print("=" * 60)

    # Create output folder
    os.makedirs("output", exist_ok=True)

    # Load dataset
    df = pd.read_csv("data/customers.csv")

    print("\nDataset Loaded Successfully!")
    print(df.head())

    # Select features
    features = df[["Age", "Annual_Income", "Spending_Score"]]

    # Standardize data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)

    print("\nData Standardized")

    # PCA
    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)

    pca_df = pd.DataFrame(
        pca_data,
        columns=["PC1", "PC2"]
    )

    print("\nPCA Completed")

    # KMeans Clustering
    kmeans = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    clusters = kmeans.fit_predict(pca_data)

    df["Cluster"] = clusters

    print("\nClustering Completed")

    # Save results
    df.to_csv(
        "output/customer_segmentation.csv",
        index=False
    )

    print("✓ Segmentation file saved")

    # ==========================
    # Visualization 1
    # PCA Cluster Plot
    # ==========================

    plt.figure(figsize=(10, 6))

    plt.scatter(
        pca_df["PC1"],
        pca_df["PC2"],
        c=clusters,
        cmap="viridis",
        s=100
    )

    plt.title("Customer Segmentation using PCA")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")

    plt.savefig(
        "output/cluster_plot.png"
    )

    plt.close()

    # ==========================
    # Visualization 2
    # Income vs Spending
    # ==========================

    plt.figure(figsize=(10, 6))

    plt.scatter(
        df["Annual_Income"],
        df["Spending_Score"],
        c=df["Cluster"],
        cmap="viridis",
        s=100
    )

    plt.xlabel("Annual Income")
    plt.ylabel("Spending Score")
    plt.title("Income vs Spending Score")

    plt.savefig(
        "output/income_spending_plot.png"
    )

    plt.close()

    print("✓ Visualizations saved")

    print("\nFiles Generated:")
    print("output/customer_segmentation.csv")
    print("output/cluster_plot.png")
    print("output/income_spending_plot.png")

    print("\nAnalysis Completed Successfully!")


if __name__ == "__main__":
    main()