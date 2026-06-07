# 🚀 Quick Reference Guide

## One-Command Start

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run complete analysis
python main.py
```

---

## 5-Minute Overview

| Step | What | Input | Output | Time |
|------|------|-------|--------|------|
| 1 | **Data Prep** | customers.csv | processed_customers.csv | 30s |
| 2 | **RFM Analysis** | Processed data | rfm_scores.csv | 20s |
| 3 | **PCA** | Numeric features | pca_components.csv | 15s |
| 4 | **Clustering** | PCA data | customer_segmentation.csv | 30s |
| 5 | **Visualization** | All results | 7 PNG files | 45s |
| 6 | **Summary** | All metrics | analysis_summary.txt | 10s |

**Total Runtime:** ~2-3 minutes

---

## Key Metrics Explained

### RFM Scores (1-4 scale)

```
R_Score = 4 → Most recent purchase (0-30 days ago) ✓
R_Score = 1 → Least recent purchase (300+ days ago) ✗

F_Score = 4 → Most frequent buyer (20+ purchases) ✓
F_Score = 1 → Least frequent (1-5 purchases) ✗

M_Score = 4 → Highest spender (₹90,000+) ✓
M_Score = 1 → Lowest spender (₹10,000-30,000) ✗
```

### Customer Segments

```
Champions (R≥3, F≥3, M≥3)           → VIP: Give best deals & service
Loyal (R≥2, F≥3, M≥3)              → Reward: Keep engaged
Potential (R≥3, F≥2, M≥2)          → Nurture: Grow relationship
Big Spenders (R≥1, F≥1, M≥3)       → Protect: Retain high value
At Risk (R≥2, F≤2, M≥2)            → Re-engage: Win back
Cannot Lose (R≤1, F≥2)             → Alert: Critical
Lost (R≥2, F≤1)                    → Campaign: Try to recover
Needs Activation (others)           → Target: Low engagement
```

### Clustering Quality

```
Silhouette Score > 0.5  → Good cluster separation ✓
Silhouette Score 0.3-0.5 → Fair separation
Silhouette Score < 0.3  → Weak separation ✗

Davies-Bouldin Index < 1.0 → Good separation ✓
Davies-Bouldin Index > 1.5 → Poor separation ✗
```

---

## Code Snippets for Common Tasks

### Load Preprocessed Data
```python
import pandas as pd
df = pd.read_csv('output/processed_customers.csv')
```

### Get Specific Segment
```python
rfm = pd.read_csv('output/rfm_scores.csv')
champions = rfm[rfm['Segment'] == 'Champions']
print(f"Champions: {len(champions)} customers")
```

### Get Specific Cluster
```python
segmented = pd.read_csv('output/customer_segmentation.csv')
cluster_2 = segmented[segmented['Cluster'] == 2]
print(f"Cluster 2: {len(cluster_2)} customers")
```

### Export Email List by Segment
```python
at_risk = rfm[rfm['Segment'] == 'At Risk']
at_risk[['CustomerID']].to_csv('at_risk_emails.csv', index=False)
```

### Calculate Average Monetary by Segment
```python
rfm.groupby('Segment')['Monetary'].agg(['mean', 'count']).round(2)
```

---

## Customization Guide

### Change INR Exchange Rate
**File:** main.py, line 56

```python
preprocessor.convert_income_to_inr(income_column='Annual_Income', exchange_rate=83.5)
# Change 83.5 to your desired rate
```

### Change CSV Column Names
**File:** main.py, lines 45-47

```python
rfm = RFMAnalysis(
    processed_df,
    customer_id='Your_ID_Column',      # Change this
    transaction_date='Your_Date_Column',  # Change this
    amount='Your_Amount_Column'        # Change this
)
```

### Change Number of Clusters to Evaluate
**File:** main.py, line 121

```python
profiler = ClusterProfiler(pca_transformed, clustering_features, n_clusters_range=(2, 12))
# Change (2, 12) to (2, 15) for more evaluation
```

### Change PCA Components
**File:** main.py, line 108

```python
pca = PCAAnalysis(processed_df, n_components=3)  # Change 2 to 3
```

---

## File Locations Quick Map

```
📁 Input Data:
   └─ data/customers.csv

📁 Source Code:
   └─ src/
      ├─ data_preprocessing.py
      ├─ rfm_analysis.py
      ├─ pca_analysis.py
      ├─ cluster_profiling.py
      └─ visualization.py

📁 Main Script:
   └─ main.py

📁 Output Results:
   └─ output/
      ├─ processed_customers.csv
      ├─ rfm_scores.csv
      ├─ pca_components.csv
      ├─ customer_segmentation.csv
      ├─ *.png (7 plots)
      └─ analysis_summary.txt
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution:** Run from project root:
```bash
cd DA-Project-1/
python main.py
```

### Problem: "FileNotFoundError: customers.csv"
**Solution:** Ensure CSV exists:
```bash
ls data/customers.csv      # Linux/Mac
dir data\customers.csv     # Windows
```

### Problem: "ValueError: could not convert"
**Solution:** Check CSV for non-numeric values in numeric columns

### Problem: "Empty Cluster"
**Solution:** Increase outlier threshold in main.py line 63:
```python
preprocessor.remove_outliers(columns=numeric_cols, threshold=2.0)  # More lenient
```

---

## Python Version Check

```bash
python --version
# Should be 3.10 or higher
```

---

## Import Verification

```bash
python -c "import pandas, numpy, sklearn, matplotlib, seaborn; print('✓ All OK')"
```

---

## Performance Tips

1. **Large Datasets:** Reduce `n_clusters_range` to speed up evaluation
2. **Memory:** Use only essential columns in analysis
3. **Time:** Pre-process data separately if running multiple times

---

## Output File Sizes (Typical)

```
processed_customers.csv    ~15 KB
rfm_scores.csv            ~12 KB
pca_components.csv        ~8 KB
customer_segmentation.csv ~20 KB
cluster_metrics.csv       ~2 KB
cluster_sizes.csv         ~1 KB
rfm_distribution.png      ~25 KB
rfm_relationships.png     ~30 KB
segment_distribution.png  ~20 KB
pca_components.png        ~25 KB
variance_explained.png    ~18 KB
cluster_analysis.png      ~35 KB
cluster_sizes.png         ~15 KB
analysis_summary.txt      ~5 KB
─────────────────────────────────
Total: ~250 KB
```

---

## Documentation Map

```
Want to...                           → See...
───────────────────────────────────────────────────
Run the analysis                    → This file (Quick Start)
Understand methodology              → README.md
Step-by-step execution              → STEPS.md
Full project overview               → PROJECT_SUMMARY.md
Module details                      → Docstrings in src/*.py
```

---

## Key Formulas

### RFM Calculation
```
Recency = Days since last purchase
Frequency = Count of purchases
Monetary = Sum of all purchases

RFM_Score = R_digit + F_digit + M_digit
            (e.g., "343" = R=3, F=4, M=3)
```

### PCA
```
PC1 = Linear combination of features capturing max variance
PC2 = Orthogonal to PC1, captures next max variance
...

Cumulative Variance = PC1 + PC2 + ... 
```

### K-Means
```
minimize: Σ ||x_i - c_j||² for each point x_i to nearest center c_j
```

---

## Contact & Support

**File Issues:**
1. Check STEPS.md for detailed troubleshooting
2. Review function docstrings in source files
3. Check console output for specific error messages

**Customization Help:**
- See Customization Guide (above)
- Edit relevant source files as needed
- Test with sample data first

---

## Quick Checklists

### Before Running:
- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`python -m pip install -r requirements.txt`)
- [ ] CSV file in `data/` folder
- [ ] Output folder doesn't have conflicting files

### After Running:
- [ ] All 6 steps completed without errors
- [ ] `output/` folder has 15+ files
- [ ] PNG files display correctly
- [ ] CSV files have content

### For Production:
- [ ] Test with sample data first
- [ ] Validate output formats
- [ ] Set up automated runs
- [ ] Monitor error logs

---

## One-Pager Summary

**What:** Customer segmentation using RFM + PCA + K-Means  
**Why:** Identify high-value customers, at-risk customers, targeting  
**How:** 6-step pipeline from data prep to visualization  
**Output:** 8 segments, 4 clusters, 7 visualizations, actionable insights  
**Time:** ~3 minutes runtime  
**Data:** CSV file with customer purchases  
**Tech:** Python, pandas, scikit-learn, matplotlib  

**Start:** `python -m pip install -r requirements.txt` then `python main.py`  
**Docs:** README.md → STEPS.md → PROJECT_SUMMARY.md

---

**Version:** 1.0 | **Status:** Ready | **Date:** June 2024
