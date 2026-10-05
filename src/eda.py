"""
Module 3: Exploratory Data Analysis (EDA)
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module generates exploratory data analysis plots and summary statistics:
1. Age & Monthly Income Distributions (Histograms & KDE)
2. Gender & Department Breakdown (Pie & Count Bar)
3. Monthly Income across Job Roles (Box Plot)
4. Job Satisfaction & Work-Life Balance (Categorical Counts)
5. OverTime vs Attrition (Stacked/Grouped Bar)
6. Department-wise Performance Ratings (Grouped Bar)
7. Years at Company vs Monthly Income (Scatter Plot colored by Attrition)
8. Absenteeism vs Job Satisfaction (Box Plot)
9. Pearson Correlation Heatmap across all numerical features
"""

import os
import matplotlib
matplotlib.use("Agg")  # Non-interactive headless backend for automated script execution
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set standard aesthetic theme
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "Arial"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8

def generate_eda_charts(df, output_dir):
    """
    Generates and saves publication-ready EDA charts into output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_charts = []
    
    print("\n--- Generating Exploratory Data Analysis Charts ---")
    
    # Chart 1: Age & Monthly Income Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.histplot(df["Age"], kde=True, ax=axes[0], color="#2b5c8f", bins=15)
    axes[0].set_title("Employee Age Distribution", fontsize=13, weight="bold", pad=12)
    axes[0].set_xlabel("Age (Years)")
    axes[0].set_ylabel("Employee Count")
    
    sns.histplot(df["MonthlyIncome"], kde=True, ax=axes[1], color="#2e8540", bins=20)
    axes[1].set_title("Monthly Income Distribution ($)", fontsize=13, weight="bold", pad=12)
    axes[1].set_xlabel("Monthly Income ($)")
    axes[1].set_ylabel("Employee Count")
    
    plt.tight_layout()
    p1 = os.path.join(output_dir, "01_age_income_distribution.png")
    fig.savefig(p1, dpi=300)
    plt.close(fig)
    saved_charts.append(p1)
    print(f" [Chart 1 Saved] {p1}")

    # Chart 2: Gender and Department Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    gender_counts = df["Gender"].value_counts()
    axes[0].pie(
        gender_counts, 
        labels=gender_counts.index, 
        autopct="%1.1f%%", 
        startangle=140, 
        colors=["#4a90e2", "#e26a6a"],
        wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
    )
    axes[0].set_title("Gender Diversity Ratio", fontsize=13, weight="bold")
    
    sns.countplot(data=df, x="Department", ax=axes[1], palette="Blues_r", hue="Department", legend=False)
    axes[1].set_title("Workforce Headcount by Department", fontsize=13, weight="bold", pad=12)
    axes[1].set_xlabel("Department")
    axes[1].set_ylabel("Headcount")
    
    plt.tight_layout()
    p2 = os.path.join(output_dir, "02_gender_department_distribution.png")
    fig.savefig(p2, dpi=300)
    plt.close(fig)
    saved_charts.append(p2)
    print(f" [Chart 2 Saved] {p2}")

    # Chart 3: Monthly Income by Job Role (Box Plot)
    fig, ax = plt.subplots(figsize=(12, 6))
    order = df.groupby("JobRole")["MonthlyIncome"].median().sort_values(ascending=False).index
    sns.boxplot(data=df, x="MonthlyIncome", y="JobRole", order=order, ax=ax, palette="Set2", hue="JobRole", legend=False)
    ax.set_title("Monthly Income Spread across Job Roles", fontsize=14, weight="bold", pad=14)
    ax.set_xlabel("Monthly Income ($)")
    ax.set_ylabel("Job Role")
    
    plt.tight_layout()
    p3 = os.path.join(output_dir, "03_monthly_income_by_role.png")
    fig.savefig(p3, dpi=300)
    plt.close(fig)
    saved_charts.append(p3)
    print(f" [Chart 3 Saved] {p3}")

    # Chart 4: Job Satisfaction & Work-Life Balance Ratings
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    rating_labels = {1: "1 - Low", 2: "2 - Medium", 3: "3 - High", 4: "4 - Very High"}
    
    sat_counts = df["JobSatisfaction"].map(rating_labels).value_counts()[["1 - Low", "2 - Medium", "3 - High", "4 - Very High"]]
    axes[0].bar(sat_counts.index, sat_counts.values, color="#e67e22")
    axes[0].set_title("Job Satisfaction Levels", fontsize=13, weight="bold", pad=12)
    axes[0].set_ylabel("Number of Employees")
    
    wlb_counts = df["WorkLifeBalance"].map(rating_labels).value_counts()[["1 - Low", "2 - Medium", "3 - High", "4 - Very High"]]
    axes[1].bar(wlb_counts.index, wlb_counts.values, color="#16a085")
    axes[1].set_title("Work-Life Balance Ratings", fontsize=13, weight="bold", pad=12)
    axes[1].set_ylabel("Number of Employees")
    
    plt.tight_layout()
    p4 = os.path.join(output_dir, "04_job_satisfaction_worklife.png")
    fig.savefig(p4, dpi=300)
    plt.close(fig)
    saved_charts.append(p4)
    print(f" [Chart 4 Saved] {p4}")

    # Chart 5: OverTime vs Attrition (Stacked & Percentage Bar)
    fig, ax = plt.subplots(figsize=(8, 5))
    ot_attr = pd.crosstab(df["OverTime"], df["Attrition"], normalize="index") * 100
    ot_attr.plot(kind="bar", stacked=True, color=["#27ae60", "#c0392b"], ax=ax, edgecolor="none", width=0.5)
    ax.set_title("Impact of Overtime Demands on Attrition Rate (%)", fontsize=13, weight="bold", pad=12)
    ax.set_ylabel("Percentage of Employees (%)")
    ax.set_xlabel("Required Overtime")
    ax.legend(title="Attrition", labels=["Stayed (No)", "Left (Yes)"])
    plt.xticks(rotation=0)
    
    # Annotate percentages
    for n, c in enumerate([ot_attr.index[0], ot_attr.index[1]]):
        val_no = ot_attr.loc[c, "No"]
        val_yes = ot_attr.loc[c, "Yes"]
        ax.text(n, val_no / 2, f"{val_no:.1f}%", ha="center", va="center", color="white", weight="bold")
        ax.text(n, val_no + (val_yes / 2), f"{val_yes:.1f}%", ha="center", va="center", color="white", weight="bold")
        
    plt.tight_layout()
    p5 = os.path.join(output_dir, "05_overtime_vs_attrition.png")
    fig.savefig(p5, dpi=300)
    plt.close(fig)
    saved_charts.append(p5)
    print(f" [Chart 5 Saved] {p5}")

    # Chart 6: Performance Rating by Department
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x="Department", hue="PerformanceRating", palette="Blues", ax=ax)
    ax.set_title("Performance Rating Distribution across Departments", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Department")
    ax.set_ylabel("Employee Count")
    ax.legend(title="Rating", labels=["1: Needs Imp.", "2: Good", "3: Excellent", "4: Outstanding"])
    
    plt.tight_layout()
    p6 = os.path.join(output_dir, "06_department_performance.png")
    fig.savefig(p6, dpi=300)
    plt.close(fig)
    saved_charts.append(p6)
    print(f" [Chart 6 Saved] {p6}")

    # Chart 7: Years at Company vs Monthly Income (Scatter colored by Attrition)
    fig, ax = plt.subplots(figsize=(9, 6))
    palette_attr = {"No": "#2980b9", "Yes": "#e74c3c"}
    sns.scatterplot(
        data=df, 
        x="YearsAtCompany", 
        y="MonthlyIncome", 
        hue="Attrition", 
        palette=palette_attr, 
        alpha=0.8, 
        s=60, 
        ax=ax
    )
    ax.set_title("Company Tenure vs Monthly Income by Attrition Status", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Years at Company")
    ax.set_ylabel("Monthly Income ($)")
    
    plt.tight_layout()
    p7 = os.path.join(output_dir, "07_tenure_vs_income_scatter.png")
    fig.savefig(p7, dpi=300)
    plt.close(fig)
    saved_charts.append(p7)
    print(f" [Chart 7 Saved] {p7}")

    # Chart 8: Absenteeism vs Job Satisfaction (Boxplot)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=df, x="JobSatisfaction", y="Absenteeism", palette="Purples", ax=ax, hue="JobSatisfaction", legend=False)
    ax.set_title("Workplace Absenteeism Days vs Job Satisfaction Tier", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Job Satisfaction (1: Low -> 4: Very High)")
    ax.set_ylabel("Absenteeism (Days per Year)")
    
    plt.tight_layout()
    p8 = os.path.join(output_dir, "08_absenteeism_vs_satisfaction.png")
    fig.savefig(p8, dpi=300)
    plt.close(fig)
    saved_charts.append(p8)
    print(f" [Chart 8 Saved] {p8}")

    # Chart 9: Correlation Matrix Heatmap
    num_cols = [
        "Age", "MonthlyIncome", "YearsAtCompany", "YearsInCurrentRole",
        "YearsSinceLastPromotion", "JobSatisfaction", "EnvironmentSatisfaction",
        "WorkLifeBalance", "PerformanceRating", "TrainingTimesLastYear", "Absenteeism"
    ]
    # Include binary Attrition in correlation
    temp_df = df[num_cols].copy()
    temp_df["Attrition_Numeric"] = df["Attrition"].map({"Yes": 1, "No": 0})
    
    corr = temp_df.corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(
        corr, 
        annot=True, 
        fmt=".2f", 
        cmap="coolwarm", 
        center=0, 
        square=True, 
        linewidths=0.5, 
        cbar_kws={"shrink": 0.8},
        ax=ax
    )
    ax.set_title("Correlation Matrix of Employee Metrics", fontsize=14, weight="bold", pad=14)
    
    plt.tight_layout()
    p9 = os.path.join(output_dir, "09_correlation_heatmap.png")
    fig.savefig(p9, dpi=300)
    plt.close(fig)
    saved_charts.append(p9)
    print(f" [Chart 9 Saved] {p9}")
    
    return saved_charts

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    output_dir = os.path.join(base_dir, "visualizations")
    
    if not os.path.exists(dataset_path):
        print(f"Dataset not found at {dataset_path}. Run generate_dataset.py first.")
        return
        
    df = pd.read_csv(dataset_path)
    charts = generate_eda_charts(df, output_dir)
    print(f"\n[Status] Exploratory Data Analysis finished. {len(charts)} charts saved to {output_dir}.")

if __name__ == "__main__":
    main()
