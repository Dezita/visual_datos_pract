# data_exploration.py

import pandas as pd

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df

def basic_exploration(df):
    print("=== Basic DataFrame Info ===")
    print(df.info())  # Column types and non-null counts
    
    print("\n=== Descriptive Statistics (numeric columns) ===")
    print(df.describe())
    
    print("\n=== First 10 Rows ===")
    print(df.head(10))
    
    print("\n=== Null Values Count by Column ===")
    print(df.isnull().sum())
    
    print("\n=== Number of Rows and Columns ===")
    print(df.shape)

if __name__ == "__main__":
    csv_path = "data/Mental_Health_Lifestyle_Dataset.csv"
    
    df = load_data(csv_path)
    basic_exploration(df)
