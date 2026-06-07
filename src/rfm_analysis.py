"""
RFM Analysis Module
Implements Recency, Frequency, Monetary analysis for customer segmentation
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class RFMAnalysis:
    """Performs RFM analysis on customer purchase data"""
    
    def __init__(self, df, customer_id='CustomerID', transaction_date='TransactionDate', 
                 amount='Amount'):
        """
        Initialize RFM Analysis
        
        Args:
            df (DataFrame): Customer transaction data
            customer_id (str): Column name for customer ID
            transaction_date (str): Column name for transaction date
            amount (str): Column name for transaction amount
        """
        self.df = df.copy()
        self.customer_id = customer_id
        self.transaction_date = transaction_date
        self.amount = amount
        self.rfm_data = None
        self.rfm_scores = None
        
    def calculate_rfm(self, analysis_date=None):
        """
        Calculate RFM values
        
        Args:
            analysis_date (datetime): Date for calculating recency (default: today)
        """
        if analysis_date is None:
            analysis_date = datetime.now()
        
        # Ensure transaction_date is datetime
        self.df[self.transaction_date] = pd.to_datetime(self.df[self.transaction_date])
        
        # Group by customer
        rfm_data = self.df.groupby(self.customer_id).agg({
            self.transaction_date: lambda x: (analysis_date - x.max()).days,  # Recency
            self.customer_id: 'count',  # Frequency
            self.amount: 'sum'  # Monetary
        })
        
        rfm_data.columns = ['Recency', 'Frequency', 'Monetary']
        rfm_data = rfm_data.reset_index()
        
        self.rfm_data = rfm_data
        print("✓ RFM metrics calculated successfully")
        print(f"\nRFM Summary:\n{rfm_data.describe()}")
        
        return rfm_data
    
    def assign_rfm_scores(self, r_quartiles=4, f_quartiles=4, m_quartiles=4):
        """
        Assign RFM scores using quantile-based ranking
        
        Args:
            r_quartiles (int): Number of recency segments (lower is better)
            f_quartiles (int): Number of frequency segments (higher is better)
            m_quartiles (int): Number of monetary segments (higher is better)
        """
        if self.rfm_data is None:
            print("Calculate RFM metrics first using calculate_rfm()")
            return
        
        # Recency: Lower values are better (recently purchased) = higher score
        self.rfm_data['R_Score'] = pd.qcut(
            self.rfm_data['Recency'], 
            q=r_quartiles, 
            labels=range(r_quartiles, 0, -1),
            duplicates='drop'
        ).astype(int)
        
        # Frequency: Higher values are better = higher score
        self.rfm_data['F_Score'] = pd.qcut(
            self.rfm_data['Frequency'], 
            q=f_quartiles, 
            labels=range(1, f_quartiles + 1),
            duplicates='drop'
        ).astype(int)
        
        # Monetary: Higher values are better = higher score
        self.rfm_data['M_Score'] = pd.qcut(
            self.rfm_data['Monetary'], 
            q=m_quartiles, 
            labels=range(1, m_quartiles + 1),
            duplicates='drop'
        ).astype(int)
        
        # Combined RFM Score
        self.rfm_data['RFM_Score'] = (
            self.rfm_data['R_Score'].astype(str) +
            self.rfm_data['F_Score'].astype(str) +
            self.rfm_data['M_Score'].astype(str)
        )
        
        print("✓ RFM Scores assigned successfully")
        print(f"\nScored data sample:\n{self.rfm_data.head(10)}")
        
        self.rfm_scores = self.rfm_data
        return self.rfm_data
    
    def segment_customers(self):
        """
        Segment customers based on RFM scores
        
        Returns:
            DataFrame: Customer data with segment labels
        """
        if self.rfm_scores is None:
            print("Assign RFM scores first using assign_rfm_scores()")
            return
        
        def get_segment(row):
            """Classify customer segment based on RFM scores"""
            r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
            
            if r >= 3 and f >= 3 and m >= 3:
                return 'Champions'
            elif r >= 2 and f >= 3 and m >= 3:
                return 'Loyal Customers'
            elif r >= 3 and f >= 2 and m >= 2:
                return 'Potential Loyalists'
            elif r >= 1 and f >= 1 and m >= 3:
                return 'Big Spenders'
            elif r >= 2 and f <= 2 and m >= 2:
                return 'At Risk'
            elif r <= 1 and f >= 2:
                return 'Cannot Lose Them'
            elif r >= 2 and f <= 1:
                return 'Lost'
            else:
                return 'Needs Activation'
        
        self.rfm_scores['Segment'] = self.rfm_scores.apply(get_segment, axis=1)
        
        print("✓ Customer segments assigned")
        print(f"\nSegment Distribution:\n{self.rfm_scores['Segment'].value_counts()}")
        
        return self.rfm_scores
    
    def get_segment_summary(self):
        """Get summary statistics by segment"""
        if self.rfm_scores is None:
            print("Create segments first using segment_customers()")
            return
        
        summary = self.rfm_scores.groupby('Segment').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean',
            self.customer_id: 'count'
        }).round(2)
        
        summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']
        summary['Pct_Customers'] = (summary['Customer_Count'] / summary['Customer_Count'].sum() * 100).round(2)
        
        return summary
    
    def get_rfm_data(self):
        """Return processed RFM data"""
        return self.rfm_scores if self.rfm_scores is not None else self.rfm_data