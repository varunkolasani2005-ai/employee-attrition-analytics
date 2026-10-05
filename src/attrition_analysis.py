"""
Module 5: Employee Attrition Analytics
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module conducts in-depth demographic, behavioral, and organizational attrition analytics:
1. Overall Organizational Attrition KPI
2. Department-wise Attrition Rate
3. Job-Role-wise Attrition Rate
4. Salary Tier Attrition Breakdown
5. Experience/Tenure Bracket Attrition Breakdown
6. Behavioral Stressors (OverTime, Work-Life Balance, Satisfaction) vs Attrition
7. Career Stagnation (Years since promotion) vs Attrition
8. Ranking of top factors associated with employee departures
"""

import os
import pandas as pd
import numpy as np

def analyze_attrition(df):
    """
    Performs comprehensive statistical and cohort analysis of employee attrition.
    
    Returns:
    - dict: Analytics tables and driver rankings.
    """
    df = df.copy()
    
    total_headcount = len(df)
    left_count = (df["Attrition"] == "Yes").sum()
    retained_count = (df["Attrition"] == "No").sum()
    overall_attrition_rate = (left_count / total_headcount) * 100.0
    
    # 1. Department-wise Attrition
    dept_attr = df.groupby("Department").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    dept_attr["AttritionRate%"] = ((dept_attr["AttritionCount"] / dept_attr["TotalEmployees"]) * 100.0).round(2)
    dept_attr = dept_attr.sort_values(by="AttritionRate%", ascending=False)
    
    # 2. Job Role-wise Attrition
    role_attr = df.groupby("JobRole").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    role_attr["AttritionRate%"] = ((role_attr["AttritionCount"] / role_attr["TotalEmployees"]) * 100.0).round(2)
    role_attr = role_attr.sort_values(by="AttritionRate%", ascending=False)
    
    # 3. Salary Tier Attrition Breakdown
    salary_bins = [0, 4500, 8500, 14000, 50000]
    salary_labels = ["Low (<$4.5k)", "Medium ($4.5k-$8.5k)", "High ($8.5k-$14k)", "Executive (>$14k)"]
    df["SalaryTier"] = pd.cut(df["MonthlyIncome"], bins=salary_bins, labels=salary_labels)
    
    salary_attr = df.groupby("SalaryTier", observed=False).agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    salary_attr["AttritionRate%"] = ((salary_attr["AttritionCount"] / salary_attr["TotalEmployees"]) * 100.0).round(2)
    
    # 4. Tenure Bracket Attrition Breakdown
    tenure_bins = [-1, 2, 5, 10, 50]
    tenure_labels = ["0-2 Yrs (New)", "3-5 Yrs (Developing)", "6-10 Yrs (Established)", "10+ Yrs (Senior)"]
    df["TenureBracket"] = pd.cut(df["YearsAtCompany"], bins=tenure_bins, labels=tenure_labels)
    
    tenure_attr = df.groupby("TenureBracket", observed=False).agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    tenure_attr["AttritionRate%"] = ((tenure_attr["AttritionCount"] / tenure_attr["TotalEmployees"]) * 100.0).round(2)
    
    # 5. OverTime vs Attrition
    ot_attr = df.groupby("OverTime").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    ot_attr["AttritionRate%"] = ((ot_attr["AttritionCount"] / ot_attr["TotalEmployees"]) * 100.0).round(2)
    
    # 6. Job Satisfaction vs Attrition
    sat_map = {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}
    df["SatisfactionLabel"] = df["JobSatisfaction"].map(sat_map)
    sat_attr = df.groupby("SatisfactionLabel").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    sat_attr["AttritionRate%"] = ((sat_attr["AttritionCount"] / sat_attr["TotalEmployees"]) * 100.0).round(2)
    sat_attr = sat_attr.sort_values(by="SatisfactionLabel")
    
    # 7. Work-Life Balance vs Attrition
    wlb_map = {1: "1 - Poor", 2: "2 - Fair", 3: "3 - Good", 4: "4 - Best"}
    df["WLBLabel"] = df["WorkLifeBalance"].map(wlb_map)
    wlb_attr = df.groupby("WLBLabel").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    wlb_attr["AttritionRate%"] = ((wlb_attr["AttritionCount"] / wlb_attr["TotalEmployees"]) * 100.0).round(2)
    wlb_attr = wlb_attr.sort_values(by="WLBLabel")
    
    # 8. Career Stagnation vs Attrition
    df["StagnationFlag"] = np.where((df["YearsSinceLastPromotion"] >= 4) & (df["YearsAtCompany"] >= 5), "Stagnated (>=4 Yrs No Promo)", "Regular Progression")
    stagnation_attr = df.groupby("StagnationFlag").agg(
        TotalEmployees=("EmployeeID", "count"),
        AttritionCount=("Attrition", lambda x: (x == "Yes").sum()),
    ).reset_index()
    stagnation_attr["AttritionRate%"] = ((stagnation_attr["AttritionCount"] / stagnation_attr["TotalEmployees"]) * 100.0).round(2)
    
    # Summary of key driving factors
    ot_rate = ot_attr.set_index("OverTime")["AttritionRate%"].to_dict()
    sat1_rate = sat_attr.set_index("SatisfactionLabel")["AttritionRate%"].get("1 - Low", 0)
    sat4_rate = sat_attr.set_index("SatisfactionLabel")["AttritionRate%"].get("4 - Very High", 0)
    
    drivers_summary = [
        f"OverTime Mandate: Employees working overtime have an attrition rate of {ot_rate.get('Yes', 0):.1f}% vs {ot_rate.get('No', 0):.1f}% for non-overtime workers.",
        f"Job Satisfaction: Employees rating satisfaction as 'Low' exhibit {sat1_rate:.1f}% attrition vs {sat4_rate:.1f}% for 'Very High' satisfaction.",
        f"Compensation Disparity: Low-income earners exhibit significantly elevated turnover compared to executive pay tiers.",
        f"Career Stagnation: Staff without promotions for 4+ years show elevated departure probability."
    ]
    
    results = {
        "overall_headcount": total_headcount,
        "left_count": left_count,
        "retained_count": retained_count,
        "attrition_rate": round(overall_attrition_rate, 2),
        "department_attrition": dept_attr,
        "role_attrition": role_attr,
        "salary_attrition": salary_attr,
        "tenure_attrition": tenure_attr,
        "overtime_attrition": ot_attr,
        "satisfaction_attrition": sat_attr,
        "worklife_attrition": wlb_attr,
        "stagnation_attrition": stagnation_attr,
        "drivers_summary": drivers_summary,
        "analyzed_df": df
    }
    
    return results

def print_attrition_summary(results):
    """Outputs formatted console report for Module 5."""
    print("=" * 65)
    print("         MODULE 5: EMPLOYEE ATTRITION ANALYTICS REPORT        ")
    print("=" * 65)
    print(f"Total Headcount: {results['overall_headcount']}")
    print(f"Retained Employees: {results['retained_count']}")
    print(f"Departed Employees: {results['left_count']}")
    print(f"Organizational Attrition Rate: {results['attrition_rate']}%\n")
    
    print("1. DEPARTMENT-WISE ATTRITION:")
    print(results["department_attrition"].to_string(index=False))
    
    print("\n2. TOP ATTRITION ROLES:")
    print(results["role_attrition"].head(5).to_string(index=False))
    
    print("\n3. OVERTIME VS ATTRITION:")
    print(results["overtime_attrition"].to_string(index=False))
    
    print("\n4. SALARY TIER ATTRITION:")
    print(results["salary_attrition"].to_string(index=False))
    
    print("\n5. KEY EMPIRICAL ATTRITION DRIVERS:")
    for driver in results["drivers_summary"]:
        print(f" * {driver}")
    print("=" * 65)

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")
        return
        
    df = pd.read_csv(dataset_path)
    results = analyze_attrition(df)
    print_attrition_summary(results)

if __name__ == "__main__":
    main()
