"""
Module 4: Employee Performance Analytics
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module analyzes employee performance:
1. Performance Categorization (Low, Average, High, Outstanding)
2. Normalized 0-100 Composite Performance Index
3. Performance breakdown by Department and Job Role
4. Correlation between Performance, Salary, Experience, and Satisfaction
5. Identifies top performers vs individuals requiring performance improvement
"""

import os
import pandas as pd
import numpy as np

def calculate_composite_performance_score(df):
    """
    Computes a realistic 0-100 Composite Performance Score combining:
    - Base Performance Rating (50% weight)
    - Training Participation (20% weight)
    - Attendance Reliability (15% weight, inversely proportional to absenteeism)
    - Job Satisfaction & Engagement (15% weight)
    
    Formula:
    Score = (Rating/4 * 50) + (Training/6 * 20) + ((1 - Absenteeism/25) * 15) + (Satisfaction/4 * 15)
    """
    df = df.copy()
    
    # Categorical labeling
    category_map = {
        1: "Low (Needs Improvement)",
        2: "Average Performer",
        3: "High Performer",
        4: "Outstanding Performer"
    }
    df["PerformanceCategory"] = df["PerformanceRating"].map(category_map)
    
    # Normalized score calculation
    rating_comp = (df["PerformanceRating"] / 4.0) * 50.0
    training_comp = (df["TrainingTimesLastYear"].clip(upper=6) / 6.0) * 20.0
    attendance_comp = (1.0 - (df["Absenteeism"].clip(upper=25) / 25.0)) * 15.0
    satisfaction_comp = (df["JobSatisfaction"] / 4.0) * 15.0
    
    df["CompositePerformanceScore"] = (rating_comp + training_comp + attendance_comp + satisfaction_comp).round(2)
    return df

def analyze_performance(df):
    """
    Executes deep analytical breakdown of workforce performance metrics.
    
    Returns:
    - dict: Dictionary of summary tables and key insights.
    """
    df_scored = calculate_composite_performance_score(df)
    
    # 1. Performance Tier Breakdown
    tier_counts = df_scored["PerformanceCategory"].value_counts()
    tier_percent = (df_scored["PerformanceCategory"].value_counts(normalize=True) * 100).round(1)
    tier_df = pd.DataFrame({"Count": tier_counts, "Percentage": tier_percent})
    
    # 2. Performance by Department
    dept_perf = df_scored.groupby("Department").agg(
        TotalEmployees=("EmployeeID", "count"),
        AvgRating=("PerformanceRating", "mean"),
        AvgCompositeScore=("CompositePerformanceScore", "mean"),
        AvgSalary=("MonthlyIncome", "mean")
    ).round(2).reset_index()
    
    # 3. Performance by Job Role
    role_perf = df_scored.groupby("JobRole").agg(
        TotalEmployees=("EmployeeID", "count"),
        AvgRating=("PerformanceRating", "mean"),
        AvgCompositeScore=("CompositePerformanceScore", "mean"),
        AvgSalary=("MonthlyIncome", "mean")
    ).round(2).sort_values(by="AvgCompositeScore", ascending=False).reset_index()
    
    # 4. Performance vs Salary Correlation
    corr_salary = df_scored["PerformanceRating"].corr(df_scored["MonthlyIncome"])
    corr_exp = df_scored["PerformanceRating"].corr(df_scored["YearsAtCompany"])
    corr_sat = df_scored["PerformanceRating"].corr(df_scored["JobSatisfaction"])
    
    # 5. Top 5 High Performers & Low Performers
    top_performers = df_scored.sort_values(by="CompositePerformanceScore", ascending=False)[
        ["EmployeeID", "JobRole", "Department", "PerformanceRating", "CompositePerformanceScore", "MonthlyIncome"]
    ].head(5)
    
    low_performers = df_scored.sort_values(by="CompositePerformanceScore", ascending=True)[
        ["EmployeeID", "JobRole", "Department", "PerformanceRating", "CompositePerformanceScore", "MonthlyIncome"]
    ].head(5)
    
    results = {
        "tier_distribution": tier_df,
        "department_performance": dept_perf,
        "role_performance": role_perf,
        "correlations": {
            "Performance_vs_Salary": round(corr_salary, 3),
            "Performance_vs_Experience": round(corr_exp, 3),
            "Performance_vs_Satisfaction": round(corr_sat, 3)
        },
        "top_performers": top_performers,
        "low_performers": low_performers,
        "scored_df": df_scored
    }
    
    return results

def print_performance_summary(results):
    """Prints a structured academic summary report to console."""
    print("=" * 65)
    print("       MODULE 4: EMPLOYEE PERFORMANCE ANALYTICS REPORT       ")
    print("=" * 65)
    
    print("\n1. PERFORMANCE TIER DISTRIBUTION:")
    print(results["tier_distribution"].to_string())
    
    print("\n2. DEPARTMENT-WISE PERFORMANCE & COMPENSATION:")
    print(results["department_performance"].to_string(index=False))
    
    print("\n3. CORRELATION ANALYSIS WITH PERFORMANCE:")
    for k, v in results["correlations"].items():
        print(f" - {k.replace('_', ' ')}: {v}")
        
    print("\n4. TOP 5 BENCHMARK PERFORMERS:")
    print(results["top_performers"].to_string(index=False))
    
    print("\n5. TOP 5 EMPLOYEES REQUIRING PERFORMANCE INTERVENTION:")
    print(results["low_performers"].to_string(index=False))
    print("=" * 65)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")
        return
        
    df = pd.read_csv(dataset_path)
    results = analyze_performance(df)
    print_performance_summary(results)

if __name__ == "__main__":
    main()
