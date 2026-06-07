"""
Data Preprocessing Module
Handles data loading, cleaning, and preparation for analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path

class DataPreprocessor:
    """Handles data loading and preprocessing tasks"""
    
    def __init__(self, data_path):
        """
        Initialize the preprocessor with data path
        
        Args:
            data_path (str): Path to the CSV file
        """
        self.data_path = data_path
        self.df = None
        
    def load_data(self):
        """Load the customer dataset"""
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✓ Data loaded successfully: {self.df.shape[0]} customers, {self.df.shape[1]} features")
            return self.df
        except FileNotFoundError:
            print(f"✗ Error: File not found at {self.data_path}")
            return None
    
    def display_basic_info(self):
        """Display basic information about the dataset"""
        if self.df is None:
            print("Load data first using load_data()")
            return
        
        print("\n" + "="*60)
        print("DATASET OVERVIEW")
        print("="*60)
        print(f"\nDataset Shape: {self.df.shape}")
        print(f"\nFirst few rows:\n{self.df.head()}")
        print(f"\nData Types:\n{self.df.dtypes}")
        print(f"\nMissing Values:\n{self.df.isnull().sum()}")
        print(f"\nBasic Statistics:\n{self.df.describe()}")
    
    def handle_missing_values(self, strategy='mean'):
        """
        Handle missing values in the dataset
        
        Args:
            strategy (str): 'mean', 'median', or 'drop'
        """
        if self.df is None:
            print("Load data first using load_data()")
            return
        
        if self.df.isnull().sum().sum() == 0:
            print("✓ No missing values found")
            return self.df
        
        if strategy == 'mean':
            self.df = self.df.fillna(self.df.mean(numeric_only=True))
        elif strategy == 'median':
            self.df = self.df.fillna(self.df.median(numeric_only=True))
        elif strategy == 'drop':
            self.df = self.df.dropna()
        
        print(f"✓ Missing values handled using {strategy} strategy")
        return self.df
    
    def convert_income_to_inr(self, income_column='Annual_Income', exchange_rate=83.5):
        """
        Convert annual income to Indian Rupees (INR)
        
        Args:
            income_column (str): Name of the income column
            exchange_rate (float): Exchange rate to INR (default USD to INR)
        """
        if self.df is None:
            print("Load data first using load_data()")
            return
        
        if income_column in self.df.columns:
            self.df[f'{income_column}_INR'] = (self.df[income_column] * exchange_rate).round(2)
            print(f"✓ Converted {income_column} to INR")
            print(f"  Sample conversions:\n{self.df[[income_column, f'{income_column}_INR']].head()}")
        else:
            print(f"✗ Column '{income_column}' not found in dataset")
        
        return self.df
    
    def remove_outliers(self, columns, method='iqr', threshold=1.5):
        """
        Remove outliers from specified columns
        
        Args:
            columns (list): Columns to check for outliers
            method (str): 'iqr' for Interquartile Range
            threshold (float): IQR multiplier for outlier detection
        """
        if self.df is None:
            print("Load data first using load_data()")
            return
        
        initial_rows = len(self.df)
        
        if method == 'iqr':
            Q1 = self.df[columns].quantile(0.25)
            Q3 = self.df[columns].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            mask = ~((self.df[columns] < lower_bound) | (self.df[columns] > upper_bound)).any(axis=1)
            self.df = self.df[mask]
        
        removed_rows = initial_rows - len(self.df)
        print(f"✓ Removed {removed_rows} outliers (IQR method)")
        return self.df
    
    def get_processed_data(self):
        """Return the processed dataframe"""
        return self.df
    
    def save_processed_data(self, output_path):
        """Save processed data to CSV"""
        if self.df is None:
            print("No data to save")
            return
        
        self.df.to_csv(output_path, index=False)
        print(f"✓ Processed data saved to {output_path}")