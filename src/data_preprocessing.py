"""
Module 2: Data Cleaning and Preprocessing
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module handles:
1. Loading the raw dataset
2. Inspection for missing values, duplicates, and anomalous data ranges
3. Missing value imputation (Median for numerical, Mode for categorical)
4. Deduplication
5. Categorical encoding (Binary mapping & One-Hot Encoding)
6. Feature scaling with StandardScaler
7. Train-Test split with stratification
8. Preprocessor artifact serialization (Scaler & Feature columns list)
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(filepath):
    """
    Loads dataset from a CSV file.
    
    Parameters:
    - filepath (str): Absolute or relative path to the CSV file.
    
    Returns:
    - pd.DataFrame: Loaded dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"[Data Loading] Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def inspect_data(df):
    """
    Performs comprehensive data health inspection:
    - Null/missing value counts
    - Duplicate row counts
    - Data types
    
    Returns:
    - dict: Summary statistics of dataset health.
    """
    null_counts = df.isnull().sum().to_dict()
    duplicates = df.duplicated(subset=["EmployeeID"]).sum()
    
    summary = {
        "total_records": len(df),
        "total_features": len(df.columns),
        "duplicate_employees": int(duplicates),
        "null_counts": {k: v for k, v in null_counts.items() if v > 0}
    }
    
    print("\n--- Data Health Inspection ---")
    print(f"Total Records: {summary['total_records']}")
    print(f"Duplicate Employee IDs: {summary['duplicate_employees']}")
    if summary["null_counts"]:
        print(f"Missing Values Found: {summary['null_counts']}")
    else:
        print("Missing Values: Zero missing values detected (Clean dataset).")
        
    return summary

def clean_data(df):
    """
    Cleans the dataset:
    - Drops duplicates if any
    - Imputes missing values if any exist
    - Ensures valid numeric bounds
    
    Returns:
    - pd.DataFrame: Cleaned dataframe.
    """
    cleaned_df = df.copy()
    
    # 1. Deduplication
    initial_len = len(cleaned_df)
    cleaned_df = cleaned_df.drop_duplicates(subset=["EmployeeID"])
    if len(cleaned_df) < initial_len:
        print(f"[Cleaning] Removed {initial_len - len(cleaned_df)} duplicate records.")
        
    # 2. Missing Value Imputation
    num_cols = cleaned_df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        if cleaned_df[col].isnull().sum() > 0:
            median_val = cleaned_df[col].median()
            cleaned_df[col] = cleaned_df[col].fillna(median_val)
            print(f"[Imputation] Filled missing values in numerical column '{col}' with median: {median_val}")
            
    cat_cols = cleaned_df.select_dtypes(include=["object", "string"]).columns
    for col in cat_cols:
        if cleaned_df[col].isnull().sum() > 0:
            mode_val = cleaned_df[col].mode()[0]
            cleaned_df[col] = cleaned_df[col].fillna(mode_val)
            print(f"[Imputation] Filled missing values in categorical column '{col}' with mode: {mode_val}")
            
    # 3. Logical Bounds Validation
    cleaned_df["Age"] = cleaned_df["Age"].clip(lower=18, upper=65)
    cleaned_df["JobSatisfaction"] = cleaned_df["JobSatisfaction"].clip(lower=1, upper=4)
    cleaned_df["WorkLifeBalance"] = cleaned_df["WorkLifeBalance"].clip(lower=1, upper=4)
    cleaned_df["PerformanceRating"] = cleaned_df["PerformanceRating"].clip(lower=1, upper=4)
    
    print("[Cleaning] Data validation and sanity bounds verified.")
    return cleaned_df

def encode_and_prepare_features(df):
    """
    Encodes categorical features into numerical form for machine learning:
    - Target 'Attrition': 'Yes' -> 1, 'No' -> 0
    - Binary feature 'OverTime': 'Yes' -> 1, 'No' -> 0
    - Multi-class features ('Department', 'JobRole', 'Education', 'Gender') -> One-Hot Encoding
    
    Returns:
    - X (pd.DataFrame): Encoded feature matrix (without EmployeeID and Attrition)
    - y (pd.Series): Target binary vector
    - feature_columns (list): List of all encoded column names
    """
    processed_df = df.copy()
    
    # 1. Target column encoding
    y = processed_df["Attrition"].map({"Yes": 1, "No": 0})
    
    # 2. Binary column encoding
    processed_df["OverTime"] = processed_df["OverTime"].map({"Yes": 1, "No": 0})
    
    # 3. Drop identifier and target column
    drop_cols = ["EmployeeID", "Attrition"]
    feature_df = processed_df.drop(columns=[c for c in drop_cols if c in processed_df.columns])
    
    # 4. Multi-class categorical columns for One-Hot Encoding
    cat_cols_to_encode = ["Department", "JobRole", "Education", "Gender"]
    X_encoded = pd.get_dummies(feature_df, columns=cat_cols_to_encode, drop_first=True, dtype=int)
    
    feature_columns = list(X_encoded.columns)
    print(f"[Encoding] Converted categorical features. Total encoded ML features: {len(feature_columns)}")
    
    return X_encoded, y, feature_columns

def prepare_train_test_data(filepath, models_dir=None, test_size=0.2, random_state=42):
    """
    Executes the full preprocessing pipeline:
    Load -> Inspect -> Clean -> Encode -> Split -> Scale -> Save Scaler.
    
    Returns:
    - X_train_scaled, X_test_scaled, y_train, y_test, feature_columns, scaler
    """
    raw_df = load_data(filepath)
    inspect_data(raw_df)
    clean_df = clean_data(raw_df)
    
    X, y, feature_columns = encode_and_prepare_features(clean_df)
    
    # Stratified Train-Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print(f"[Splitting] Train set: {len(X_train)} samples, Test set: {len(X_test)} samples")
    print(f"[Splitting] Attrition rate in Train: {y_train.mean()*100:.2f}%, Test: {y_test.mean()*100:.2f}%")
    
    # Feature Scaling using StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save artifacts if models_dir is provided
    if models_dir:
        os.makedirs(models_dir, exist_ok=True)
        scaler_path = os.path.join(models_dir, "scaler.pkl")
        features_path = os.path.join(models_dir, "feature_names.json")
        
        joblib.dump(scaler, scaler_path)
        with open(features_path, "w") as f:
            json.dump(feature_columns, f, indent=4)
            
        print(f"[Artifacts] Saved Scaler to: {scaler_path}")
        print(f"[Artifacts] Saved Feature Names list to: {features_path}")
        
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_columns, scaler, clean_df

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    models_dir = os.path.join(base_dir, "models")
    
    print("=" * 60)
    print("Executing Module 2: Data Preprocessing Pipeline")
    print("=" * 60)
    
    X_train_sc, X_test_sc, y_train, y_test, features, scaler, clean_df = prepare_train_test_data(
        dataset_path, models_dir=models_dir
    )
    
    print("\n[Status] Data preprocessing completed successfully.")
    print(f"Features ready for model training: {len(features)}")

if __name__ == "__main__":
    main()
