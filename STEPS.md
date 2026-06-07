# Market & Customer Segmentation Analysis - Execution Guide

## 🎯 Project Overview

**Objective:** Group customers by purchasing habits using RFM analysis, PCA dimensionality reduction, and K-Means clustering to enable targeted marketing campaigns.

**Dataset:** Mall Customers Dataset  
**Tech Stack:** Python, Pandas, Scikit-Learn, Matplotlib, Seaborn

---

## 📋 Step-by-Step Execution

### **STEP 1: Environment Setup**

#### 1.1 Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What Gets Installed:**
- **pandas** (2.0.3) - Data manipulation and analysis
- **numpy** (1.24.3) - Numerical computing
- **matplotlib** (3.7.2) - Plotting and visualization
- **seaborn** (0.12.2) - Statistical visualization
- **scikit-learn** (1.3.0) - Machine learning algorithms
- **plotly** (5.16.1) - Interactive visualizations (optional)

#### 1.2 Verify Installation

```bash
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('✓ All packages installed successfully')"
```

---

### **STEP 2: Prepare Your Dataset**

#### 2.1 Dataset Location

Place your Mall Customers CSV file in the `data/` folder:

```
DA-Project-1/
└── data/
    └── customers.csv
```

#### 2.2 Expected Data Format

Your CSV should have columns like:

```
CustomerID | Gender | Age | Annual_Income | Spending_Score
1001       | Male   | 25  | 50000        | 45
1002       | Female | 35  | 75000        | 65
1003       | Male   | 28  | 60000        | 55
...
```

#### 2.3 Column Mapping (Customize as Needed)

The code expects:
- `CustomerID` - Unique customer identifier
- `Annual_Income` - Annual income (will be converted to INR)
- `Spending_Score` - Customer spending pattern score
- `Age`, `Gender` - Additional customer attributes

**If your column names are different, edit `main.py` lines 45-47:**

```python
# Change these to match your CSV columns
customer_id='CustomerID'          # Your customer ID column
transaction_date='Date'           # Your date column
amount='Amount'                   # Your transaction amount column
```

---

### **STEP 3: Execute the Main Analysis Pipeline**

#### 3.1 Run the Complete Analysis

```bash
python main.py
```

This will automatically execute 6 major steps:

1. **Data Loading & Preprocessing** - Clean and prepare data
2. **RFM Analysis** - Calculate Recency, Frequency, Monetary metrics
3. **Dimensionality Reduction (PCA)** - Reduce features to 2 components
4. **Cluster Profiling** - Apply K-Means clustering
5. **Visualization** - Generate 7 detailed plots
6. **Summary Report** - Create analysis summary

#### 3.2 Expected Output

```
======================================================================
MARKET & CUSTOMER SEGMENTATION ANALYSIS
======================================================================

[STEP 1] DATA LOADING & PREPROCESSING
----------------------------------------------------------------------
✓ Data loaded successfully: 200 customers, 5 features

DATASET OVERVIEW
============================================================
Dataset Shape: (200, 5)
...

[STEP 2] RFM ANALYSIS (Recency, Frequency, Monetary)
----------------------------------------------------------------------
✓ RFM metrics calculated successfully

RFM Summary:
       Recency  Frequency  Monetary
count     200      200        200
mean    50.5       10.2    60000.5
...

✓ RFM Scores assigned successfully
...

[STEP 3] DIMENSIONALITY REDUCTION (PCA)
----------------------------------------------------------------------
✓ Features standardized (zero mean, unit variance)
✓ PCA fitted with 2 components

Explained Variance Ratio:
[0.45 0.30]
Cumulative Variance Explained: 0.7500

[STEP 4] CLUSTER PROFILING (K-Means)
----------------------------------------------------------------------
✓ Optimal number of clusters: 4

[STEP 5] VISUALIZATION
----------------------------------------------------------------------
✓ RFM distribution plot saved
✓ RFM relationships plot saved
✓ Segment distribution plot saved
✓ PCA components plot saved
✓ Variance explained plot saved
✓ Cluster analysis plot saved
✓ Cluster sizes plot saved

[STEP 6] SUMMARY REPORT
----------------------------------------------------------------------
✓ Summary report saved to output/analysis_summary.txt

======================================================================
ANALYSIS COMPLETE!
======================================================================
```

---

### **STEP 4: Review Generated Outputs**

After execution, the `output/` folder contains:

#### 4.1 CSV Data Files

| File | Purpose |
|------|---------|
| `processed_customers.csv` | Cleaned data without outliers |
| `rfm_scores.csv` | RFM metrics and customer segments |
| `pca_components.csv` | 2D PCA transformed data |
| `customer_segmentation.csv` | Final clusters + RFM segments |
| `cluster_metrics.csv` | K-Means evaluation metrics |
| `cluster_sizes.csv` | Cluster distribution |

#### 4.2 Visualization Files (PNG)

| File | Shows |
|------|-------|
| `rfm_distribution.png` | Histograms of R, F, M values |
| `rfm_relationships.png` | Scatter plots of RFM correlations |
| `segment_distribution.png` | Bar and pie charts of segments |
| `pca_components.png` | 2D scatter of PC1 vs PC2 |
| `variance_explained.png` | PCA variance contribution |
| `cluster_analysis.png` | Feature distributions by cluster |
| `cluster_sizes.png` | Customers per cluster |

#### 4.3 Report File

- `analysis_summary.txt` - Executive summary of findings

---

## 🔍 Understanding Each Module

### **Module 1: Data Preprocessing** (`src/data_preprocessing.py`)

**Functions:**

```python
# Initialize
preprocessor = DataPreprocessor('data/customers.csv')

# Load data
df = preprocessor.load_data()

# Display info
preprocessor.display_basic_info()

# Handle missing values
preprocessor.handle_missing_values(strategy='mean')

# Convert income to INR (USD → INR, default rate: 83.5)
preprocessor.convert_income_to_inr(
    income_column='Annual_Income',
    exchange_rate=83.5
)

# Remove outliers using IQR method
preprocessor.remove_outliers(
    columns=['Annual_Income', 'Age'],
    method='iqr',
    threshold=1.5  # 1.5x IQR = outlier
)

# Get processed data
processed_df = preprocessor.get_processed_data()

# Save to CSV
preprocessor.save_processed_data('output/processed_data.csv')
```

---

### **Module 2: RFM Analysis** (`src/rfm_analysis.py`)

**What is RFM?**

- **Recency (R):** Days since last purchase (Lower = Better)
- **Frequency (F):** Number of purchases (Higher = Better)
- **Monetary (M):** Total amount spent (Higher = Better)

**Functions:**

```python
# Initialize
rfm = RFMAnalysis(
    df,
    customer_id='CustomerID',
    transaction_date='Date',
    amount='Amount'
)

# Calculate RFM metrics
rfm_data = rfm.calculate_rfm(
    analysis_date=datetime.now()  # Reference date for recency
)

# Assign RFM scores (1-4 scale)
rfm_scores = rfm.assign_rfm_scores(
    r_quartiles=4,  # 1 = lowest recency, 4 = highest
    f_quartiles=4,  # 1 = lowest frequency, 4 = highest
    m_quartiles=4   # 1 = lowest monetary, 4 = highest
)

# Segment customers based on scores
segmented = rfm.segment_customers()

# Get summary by segment
summary = rfm.get_segment_summary()
```

**Customer Segments:**

| Segment | Characteristics | RFM Pattern | Action |
|---------|-----------------|-------------|--------|
| Champions | Best customers | R≥3, F≥3, M≥3 | VIP program |
| Loyal | Consistent buyers | R≥2, F≥3, M≥3 | Loyalty rewards |
| Potential | Recent buyers | R≥3, F≥2, M≥2 | Upsell offers |
| Big Spenders | High value | R≥1, F≥1, M≥3 | Premium service |
| At Risk | Were frequent | R≥2, F≤2, M≥2 | Re-engagement |
| Cannot Lose | Important past | R≤1, F≥2 | Win-back campaign |
| Lost | Inactive | R≥2, F≤1 | Survey/feedback |

---

### **Module 3: PCA Analysis** (`src/pca_analysis.py`)

**Why PCA?**

Reduces high-dimensional data to 2-3 components while preserving 70-80% of variance, making clustering more effective and interpretable.

**Functions:**

```python
# Initialize with 2 components
pca = PCAAnalysis(df, n_components=2)

# Select features to analyze
pca.prepare_data(columns_to_exclude=['CustomerID', 'Gender'])

# Standardize features (mean=0, std=1)
pca.standardize_features()

# Fit PCA model
pca.fit_pca()

# Transform data to PC space
pca_data = pca.transform_data()

# Get variance explained
variance_df = pca.get_variance_explained()
# Output:
#   Component  Explained_Variance  Cumulative_Variance
#   PC1        0.45               0.45
#   PC2        0.30               0.75

# Get feature loadings
loadings = pca.get_feature_importance()
```

**Interpretation:**
- If PC1 explains 45% and PC2 explains 30%, together they capture 75% of variance
- First 2 components usually sufficient for visualization
- Loadings show which original features contribute to each PC

---

### **Module 4: Cluster Profiling** (`src/cluster_profiling.py`)

**What is K-Means?**

Partitions customers into k groups that minimize within-cluster variance.

**Functions:**

```python
# Initialize
profiler = ClusterProfiler(
    df,
    features_for_clustering=['PC1', 'PC2'],
    n_clusters_range=(2, 8)
)

# Find optimal clusters (using Silhouette Score)
metrics = profiler.find_optimal_clusters()
# Evaluates k=2 to k=8, returns metrics for each

# Fit K-Means with optimal k
clustered = profiler.fit_kmeans(n_clusters=4)

# Get cluster profiles (mean feature values per cluster)
profiles = profiler.get_cluster_profiles()

# Get cluster sizes
sizes = profiler.get_cluster_sizes()

# Get cluster centers
centers = profiler.get_cluster_centers()
```

**Evaluation Metrics:**

| Metric | Range | Interpretation |
|--------|-------|-----------------|
| Silhouette Score | -1 to 1 | >0.5 = good separation |
| Davies-Bouldin Index | 0 to ∞ | Lower is better |
| Inertia | 0 to ∞ | Lower = tighter clusters |

---

### **Module 5: Visualization** (`src/visualization.py`)

**Functions:**

```python
# Initialize
viz = Visualizer(output_dir='output')

# RFM visualizations
viz.plot_rfm_distribution(rfm_data)
viz.plot_rfm_scatter(rfm_data)
viz.plot_segment_distribution(segmented)

# PCA visualizations
viz.plot_variance_explained(variance_df)
viz.plot_pca_components(pca_data, clusters=cluster_labels)

# Cluster visualizations
viz.plot_cluster_analysis(clustered_data, features_list)
viz.plot_cluster_sizes(cluster_sizes)

# Generate report
viz.create_summary_report({
    'Key Finding 1': 'Value 1',
    'Key Finding 2': 'Value 2'
})
```

---

## 💡 Practical Examples

### Example 1: Analyzing a Specific Segment

```python
# Get Champions customers
champions = segmented[segmented['Segment'] == 'Champions']
print(f"Champions: {len(champions)} customers")
print(f"Average Monetary: ₹{champions['Monetary'].mean():,.2f}")

# Export to CSV
champions.to_csv('output/champions_list.csv', index=False)
```

### Example 2: Analyzing a Specific Cluster

```python
# Get Cluster 2
cluster_2 = clustered[clustered['Cluster'] == 2]
print(f"Cluster 2: {len(cluster_2)} customers")

# Segment distribution within cluster
print(cluster_2['Segment'].value_counts())

# Average features
print(cluster_2[['PC1', 'PC2']].describe())
```

### Example 3: Marketing Strategy by Segment

```python
segment_strategies = {
    'Champions': {
        'campaign': 'VIP loyalty program',
        'discount': '10-15%',
        'frequency': 'monthly'
    },
    'At Risk': {
        'campaign': 'Win-back offer',
        'discount': '20-25%',
        'frequency': 'weekly'
    },
    'Lost': {
        'campaign': 'Survey & feedback',
        'discount': '30%',
        'frequency': 'one-time'
    }
}

for segment, strategy in segment_strategies.items():
    customers = segmented[segmented['Segment'] == segment]
    print(f"\n{segment} ({len(customers)} customers):")
    print(f"  Campaign: {strategy['campaign']}")
    print(f"  Offer: {strategy['discount']} discount")
```

---

## 🎨 Interpreting the Visualizations

### 1. RFM Distribution
- **Left skew:** Most customers have recent activity (good)
- **Right skew:** Many inactive customers (needs attention)
- **Multi-modal:** Multiple customer types present

### 2. PCA Components Plot
- **Tight clusters:** Well-defined customer groups
- **Overlapping clouds:** Similar customer behaviors
- **Outliers:** Unique customer patterns

### 3. Segment Distribution
- **Unbalanced:** Some segments very small (risky)
- **Balanced:** Good diversity in customer base

### 4. Variance Explained
- **>80% with 2 components:** High reduction success
- **<60% with 2 components:** May need more components

---

## 🚀 Advanced Customizations

### Change Currency Exchange Rate

```python
# For INR conversion from different currencies
preprocessor.convert_income_to_inr(
    income_column='Annual_Income',
    exchange_rate=100  # EUR to INR
)
```

### Adjust RFM Scoring

```python
# Use 5-level scoring instead of 4
rfm_scores = rfm.assign_rfm_scores(
    r_quartiles=5,
    f_quartiles=5,
    m_quartiles=5
)
```

### Change PCA Components

```python
# Use 3 components for more variance
pca = PCAAnalysis(df, n_components=3)
```

### Custom Cluster Range

```python
# Evaluate k=3 to k=15
profiler = ClusterProfiler(df, features, n_clusters_range=(3, 15))
```

### Define Custom Segments

Edit `src/rfm_analysis.py` `get_segment()` function:

```python
def get_segment(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    
    if r >= 4 and f >= 4:
        return 'VIP'  # Custom definition
    elif r >= 3 and m >= 4:
        return 'Premium'
    else:
        return 'Standard'
```

---

## ⚠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:** Ensure you run `main.py` from the project root directory:

```bash
cd DA-Project-1/
python main.py
```

### Issue: "FileNotFoundError: data/customers.csv"

**Solution:** Ensure CSV file exists in the `data/` folder:

```bash
ls data/customers.csv  # Linux/Mac
dir data\customers.csv  # Windows
```

### Issue: "ValueError: could not convert string to float"

**Solution:** Check CSV for non-numeric values in numeric columns. Clean data first.

### Issue: "Empty DataFrame" warning

**Solution:** Outlier removal threshold too strict. Adjust in main.py:

```python
preprocessor.remove_outliers(columns=numeric_cols, threshold=2.0)  # More lenient
```

---

## 📊 Output Format Specifications

### CSV Files
- UTF-8 encoding
- Comma-separated values
- Headers included
- Numeric values with 2 decimal places

### PNG Visualizations
- 300 DPI resolution
- High-quality suitable for reports
- All axes labeled with units

### TXT Report
- Plain ASCII text
- Section headers with dashes
- Easy copy-paste to documents

---

## ✅ Validation Checklist

After execution, verify:

- [ ] All 6 analysis steps completed
- [ ] No errors in console output
- [ ] `output/` folder contains 13+ files
- [ ] CSV files have correct row counts
- [ ] PNG files open and display correctly
- [ ] Summary report is readable

---

## 📈 Next Steps

### 1. Business Implementation
- Export segments to CRM system
- Create targeted email campaigns
- Develop personalized product recommendations

### 2. Advanced Analysis
- Add predictive churn modeling
- Implement cohort analysis
- Create customer lifetime value (CLV) calculations

### 3. Automation
- Schedule weekly/monthly re-runs
- Set up automated alerts for segment changes
- Create dashboard for real-time monitoring

---

## 📚 References

**RFM Analysis:**
- Developed by direct marketing professionals
- Predicts customer lifetime value
- Widely used in retail and e-commerce

**Principal Component Analysis:**
- Dimensionality reduction technique
- Preserves maximum variance
- Enables visualization of high-dimensional data

**K-Means Clustering:**
- Unsupervised learning algorithm
- Partitions into k clusters
- Widely used for market segmentation

---

**Version:** 1.0  
**Last Updated:** June 2024  
**Status:** Ready for Production Use

---
