# Market & Customer Segmentation Analysis

## 📋 Project Overview

This is a comprehensive **Market & Customer Segmentation Analysis** project designed to help businesses identify and understand customer groups based on purchasing habits. Using advanced data science techniques, this project enables companies to build **targeted marketing campaigns** and improve customer relationship management.

## 🎯 Learning Objectives

By working through this project, you'll master:

1. **RFM Analysis** - Segmenting customers by Recency, Frequency, and Monetary value
2. **Dimensionality Reduction (PCA)** - Reducing feature complexity while retaining variance
3. **K-Means Clustering** - Identifying natural customer groupings
4. **Data Preprocessing** - Cleaning and preparing data for analysis
5. **Data Visualization** - Creating compelling insights through visualizations

## 📁 Project Structure

```
DA-Project-1/
│
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── src/                            # Source code modules
│   ├── data_preprocessing.py        # Data loading and cleaning
│   ├── rfm_analysis.py             # RFM (Recency, Frequency, Monetary)
│   ├── pca_analysis.py             # Principal Component Analysis
│   ├── cluster_profiling.py        # K-Means clustering
│   └── visualization.py            # Creating plots and reports
│
├── data/                           # Input data
│   └── customers.csv               # Mall Customers Dataset
│
└── output/                         # Generated outputs
    ├── processed_customers.csv     # Cleaned data
    ├── rfm_scores.csv              # RFM analysis results
    ├── pca_components.csv          # PCA transformed data
    ├── customer_segmentation.csv   # Final segmentation results
    ├── cluster_metrics.csv         # Clustering metrics
    ├── rfm_distribution.png        # RFM distribution plots
    ├── rfm_relationships.png       # RFM scatter plots
    ├── segment_distribution.png    # Segment distribution
    ├── pca_components.png          # PCA visualization
    ├── cluster_analysis.png        # Cluster analysis
    ├── variance_explained.png      # PCA variance plot
    ├── cluster_sizes.png           # Cluster size distribution
    └── analysis_summary.txt        # Summary report
```

---

## 🚀 Quick Start Guide

### 1. **Installation**

Install all required dependencies:

```bash
pip install -r requirements.txt
```

**Required Libraries:**
- `pandas` - Data manipulation and analysis
- `numpy` - Numerical computing
- `matplotlib` - Visualization
- `seaborn` - Statistical data visualization
- `scikit-learn` - Machine learning algorithms

### 2. **Dataset Preparation**

Place your Mall Customers dataset in the `data/` folder:

```
data/
└── customers.csv
```

**Expected columns in the dataset:**
- `CustomerID` - Unique customer identifier
- `Gender` - Customer gender
- `Age` - Customer age
- `Annual_Income` - Annual income (will be converted to INR)
- `Spending_Score` - Spending behavior score (0-100)

### 3. **Run the Analysis**

Execute the main script to run the complete pipeline:

```bash
python main.py
```

The script will automatically:
- Load and preprocess data
- Perform RFM analysis
- Apply PCA for dimensionality reduction
- Identify optimal clusters
- Generate visualizations
- Create summary reports

---

## 📊 Detailed Methodology

### **STEP 1: Data Preprocessing**
**Module:** `src/data_preprocessing.py`

**What it does:**
- Loads customer data from CSV
- Handles missing values using mean imputation
- Converts annual income to Indian Rupees (INR)
- Detects and removes statistical outliers (IQR method)
- Provides comprehensive data quality reports

**Key Functions:**
```python
preprocessor = DataPreprocessor('data/customers.csv')
df = preprocessor.load_data()
preprocessor.convert_income_to_inr(exchange_rate=83.5)
preprocessor.remove_outliers(['Annual_Income'])
```

---

### **STEP 2: RFM Analysis**
**Module:** `src/rfm_analysis.py`

**What is RFM?**
- **Recency (R):** How recently did the customer make a purchase? (Lower is better)
- **Frequency (F):** How often does the customer purchase? (Higher is better)
- **Monetary (M):** How much does the customer spend? (Higher is better)

**Customer Segments Identified:**
1. **Champions** (R≥3, F≥3, M≥3) - Best customers, buy often, recently, and spend the most
2. **Loyal Customers** (R≥2, F≥3, M≥3) - Good customers with consistent purchase pattern
3. **Potential Loyalists** (R≥3, F≥2, M≥2) - Recent buyers who could become loyal
4. **Big Spenders** (R≥1, F≥1, M≥3) - High-value customers, focus on retention
5. **At Risk** (R≥2, F≤2, M≥2) - Used to be frequent buyers but haven't purchased recently
6. **Cannot Lose Them** (R≤1, F≥2) - Made significant purchases long ago, at risk of leaving
7. **Lost** (R≥2, F≤1) - Almost completely inactive
8. **Needs Activation** - Low engagement across all metrics

**Key Functions:**
```python
rfm = RFMAnalysis(df, 'CustomerID', 'Date', 'Amount')
rfm_data = rfm.calculate_rfm()
rfm_scores = rfm.assign_rfm_scores()
segments = rfm.segment_customers()
summary = rfm.get_segment_summary()
```

---

### **STEP 3: PCA (Principal Component Analysis)**
**Module:** `src/pca_analysis.py`

**Purpose:** Reduce data dimensionality while preserving maximum variance

**How it works:**
1. Standardizes all features to zero mean and unit variance
2. Identifies principal components (new uncorrelated features)
3. Each component captures maximum remaining variance
4. Typically reduces 10+ features to 2-3 components without losing much information

**Benefits:**
- Eliminates multicollinearity
- Improves clustering performance
- Reduces computational complexity
- Enables 2D/3D visualization

**Key Functions:**
```python
pca = PCAAnalysis(df, n_components=2)
pca.prepare_data()
pca.standardize_features()
pca.fit_pca()
pca_data = pca.transform_data()
variance_df = pca.get_variance_explained()
```

---

### **STEP 4: Cluster Profiling**
**Module:** `src/cluster_profiling.py`

**Purpose:** Group customers into homogeneous clusters

**Algorithm:** K-Means Clustering
- Partitions customers into k clusters
- Minimizes within-cluster variance
- Identifies optimal k using Silhouette Score

**Evaluation Metrics:**
- **Silhouette Score:** Measures how similar points are to their own cluster (-1 to 1, higher is better)
- **Davies-Bouldin Index:** Measures cluster separation (lower is better)
- **Inertia:** Sum of squared distances within clusters

**Key Functions:**
```python
profiler = ClusterProfiler(df, features_list, n_clusters_range=(2, 10))
metrics = profiler.find_optimal_clusters()
clustered = profiler.fit_kmeans(n_clusters=4)
profiles = profiler.get_cluster_profiles()
sizes = profiler.get_cluster_sizes()
```

---

### **STEP 5: Visualization**
**Module:** `src/visualization.py`

**Generated Visualizations:**

1. **RFM Distribution** - Histograms showing distribution of Recency, Frequency, Monetary
2. **RFM Relationships** - Scatter plots showing correlations between RFM metrics
3. **Segment Distribution** - Bar and pie charts of customer segments
4. **PCA Components** - 2D scatter plot of first two principal components
5. **Variance Explained** - Cumulative variance captured by each PC
6. **Cluster Analysis** - Box plots of features by cluster
7. **Cluster Sizes** - Bar chart of customers per cluster

All visualizations are saved as high-resolution PNG files (300 DPI).

---

## 📈 Usage Examples

### Example 1: Load and Preprocess Data

```python
from src.data_preprocessing import DataPreprocessor

# Initialize preprocessor
preprocessor = DataPreprocessor('data/customers.csv')

# Load data
df = preprocessor.load_data()

# Handle missing values
preprocessor.handle_missing_values(strategy='mean')

# Convert income to INR (from USD)
preprocessor.convert_income_to_inr(income_column='Annual_Income', exchange_rate=83.5)

# Get processed data
processed_df = preprocessor.get_processed_data()
```

### Example 2: Perform RFM Analysis

```python
from src.rfm_analysis import RFMAnalysis

# Create RFM analysis
rfm = RFMAnalysis(df, 'CustomerID', 'Date', 'Amount')

# Calculate RFM metrics
rfm_data = rfm.calculate_rfm()

# Assign scores (1-4 scale)
rfm_scores = rfm.assign_rfm_scores(r_quartiles=4, f_quartiles=4, m_quartiles=4)

# Segment customers
segmented = rfm.segment_customers()

# Get segment summary
summary = rfm.get_segment_summary()
print(summary)
```

### Example 3: Apply PCA

```python
from src.pca_analysis import PCAAnalysis

# Create PCA analysis
pca = PCAAnalysis(df, n_components=2)

# Prepare data
pca.prepare_data()

# Standardize features
pca.standardize_features()

# Fit PCA
pca.fit_pca()

# Transform data
pca_data = pca.transform_data()

# Get variance explained
variance = pca.get_variance_explained()
print(variance)
```

### Example 4: Perform Clustering

```python
from src.cluster_profiling import ClusterProfiler

# Create profiler
profiler = ClusterProfiler(df, features_list, n_clusters_range=(2, 8))

# Find optimal clusters
metrics = profiler.find_optimal_clusters()

# Fit K-Means
clustered_data = profiler.fit_kmeans(n_clusters=4)

# Get profiles
profiles = profiler.get_cluster_profiles()
print(profiles)
```

### Example 5: Create Visualizations

```python
from src.visualization import Visualizer

# Create visualizer
viz = Visualizer(output_dir='output')

# Plot RFM distributions
viz.plot_rfm_distribution(rfm_data)
viz.plot_rfm_scatter(rfm_data)

# Plot segments
viz.plot_segment_distribution(segmented)

# Plot PCA
viz.plot_pca_components(pca_data, clusters=cluster_labels)
viz.plot_variance_explained(variance_df)

# Plot clusters
viz.plot_cluster_analysis(clustered_data, features)
viz.plot_cluster_sizes(cluster_sizes)

# Generate report
viz.create_summary_report(report_data)
```

---

## 🔍 Understanding the Output Files

### CSV Files (Data)
- **processed_customers.csv** - Cleaned customer data ready for analysis
- **rfm_scores.csv** - RFM values and scores for each customer
- **pca_components.csv** - Principal component scores
- **customer_segmentation.csv** - Final customer segments and clusters
- **cluster_metrics.csv** - Metrics for different cluster counts
- **cluster_sizes.csv** - Number and percentage of customers per cluster

### PNG Files (Visualizations)
- **rfm_distribution.png** - RFM histogram distributions
- **rfm_relationships.png** - RFM correlation scatter plots
- **segment_distribution.png** - Customer segment breakdown
- **variance_explained.png** - PCA variance contribution
- **pca_components.png** - 2D PCA visualization with clusters
- **cluster_analysis.png** - Feature distributions by cluster
- **cluster_sizes.png** - Cluster population sizes

### Text Files (Reports)
- **analysis_summary.txt** - Executive summary of analysis results

---

## 💡 Key Insights from Analysis

### 1. Customer Segmentation Value
Different customer segments need different marketing strategies:
- **Champions:** VIP treatment, personalized offers
- **Loyal:** Reward programs, exclusive benefits
- **At Risk:** Win-back campaigns, special discounts
- **Lost:** Re-engagement campaigns, survey for feedback

### 2. Income Distribution (INR Format)
- Conversion ensures meaningful analysis for Indian market
- Helps segment by purchasing power
- Enables localized pricing strategies

### 3. Cluster Characteristics
- Each cluster represents a distinct customer archetype
- Use cluster profiles to guide marketing campaigns
- Tailor product recommendations by cluster

### 4. PCA Insights
- First 2 components usually capture 70-80% of variance
- Reduced dimensionality improves model interpretability
- Easier to visualize high-dimensional customer data

---

## 🛠️ Customization Guide

### Change Analysis Date for Recency
```python
from datetime import datetime
rfm.calculate_rfm(analysis_date=datetime(2024, 6, 3))
```

### Adjust RFM Score Quartiles
```python
rfm.assign_rfm_scores(r_quartiles=5, f_quartiles=5, m_quartiles=5)
```

### Change Number of PCA Components
```python
pca = PCAAnalysis(df, n_components=3)
```

### Adjust Cluster Range
```python
profiler = ClusterProfiler(df, features, n_clusters_range=(3, 12))
```

### Custom Segment Logic
Edit the `get_segment()` function in `src/rfm_analysis.py` to define your own segmentation rules.

---

## 📚 Theoretical Concepts

### RFM Analysis
**Reference:** Developed by direct marketers, RFM is a proven customer segmentation technique that predicts future purchase behavior.

### Principal Component Analysis
**Reference:** Statistical technique for dimensionality reduction developed by Karl Pearson (1901).
- Transforms correlated variables into uncorrelated principal components
- Useful for reducing noise and improving algorithm efficiency

### K-Means Clustering
**Reference:** Unsupervised learning algorithm developed by Stuart Lloyd (1957).
- Iteratively partitions data into k clusters
- Minimizes within-cluster sum of squares
- Simple but powerful for customer segmentation

---

## ⚠️ Important Notes

1. **Data Quality:** Ensure your customer dataset has no duplicate records
2. **Missing Values:** The default strategy is mean imputation; adjust for your data
3. **Feature Scaling:** PCA requires standardized features (handled automatically)
4. **Cluster Interpretation:** Business context is crucial for meaningful segments
5. **Privacy:** Handle customer data responsibly and in compliance with regulations

---

## 🤝 Contributing

To enhance this project:
1. Add more sophisticated outlier detection methods
2. Implement advanced clustering (Hierarchical, DBSCAN)
3. Add predictive models for churn prediction
4. Create interactive dashboards (Plotly, Streamlit)

---

## 📞 Support

For questions or issues:
1. Check the function docstrings in source files
2. Review example usage in `main.py`
3. Examine the generated summary report

---

## 📄 License

This educational project is provided as-is for learning purposes.

---

**Last Updated:** June 2024  
**Version:** 1.0
