"""
Module 1: Dataset Generation Script
Project: Employee Performance and Attrition Analytics Using Data Analytics

This script generates a realistic synthetic dataset of 500 employee records
modeled after standard enterprise HR analytics schemas (e.g., IBM HR Analytics).
It introduces realistic logical correlations between employee compensation,
workplace satisfaction, overtime demands, career stagnation, and attrition risk.
"""

import os
import numpy as np
import pandas as pd

def generate_employee_dataset(num_records=500, random_seed=42):
    """
    Generates a realistic employee performance and attrition dataset.
    
    Parameters:
    - num_records (int): Total number of employee rows to generate (default 500)
    - random_seed (int): Seed for reproducibility
    
    Returns:
    - pd.DataFrame: Generated dataset
    """
    np.random.seed(random_seed)
    
    # 1. Employee Identifiers
    employee_ids = [f"EMP{str(i).zfill(3)}" for i in range(1, num_records + 1)]
    
    # 2. Demographic Attributes
    ages = np.random.randint(21, 59, size=num_records)
    genders = np.random.choice(["Male", "Female"], size=num_records, p=[0.58, 0.42])
    
    # 3. Department and Job Roles Mapping
    dept_roles = {
        "Research & Development": [
            ("Software Engineer", 0.40),
            ("Research Scientist", 0.30),
            ("Laboratory Technician", 0.20),
            ("Manufacturing Director", 0.10)
        ],
        "Sales": [
            ("Sales Executive", 0.55),
            ("Sales Representative", 0.35),
            ("Manager", 0.10)
        ],
        "Human Resources": [
            ("HR Executive", 0.70),
            ("Manager", 0.30)
        ]
    }
    
    departments = np.random.choice(
        ["Research & Development", "Sales", "Human Resources"],
        size=num_records,
        p=[0.55, 0.35, 0.10]
    )
    
    job_roles = []
    for dept in departments:
        roles, probs = zip(*dept_roles[dept])
        job_roles.append(np.random.choice(roles, p=probs))
    job_roles = np.array(job_roles)
    
    # 4. Education & Job Levels
    education_levels = np.random.choice(
        ["High School", "Bachelor", "Master", "Doctorate"],
        size=num_records,
        p=[0.12, 0.52, 0.30, 0.06]
    )
    
    job_levels = []
    for role in job_roles:
        if "Manager" in role or "Director" in role:
            job_levels.append(np.random.choice([4, 5], p=[0.6, 0.4]))
        elif "Scientist" in role or "Executive" in role or "Software" in role:
            job_levels.append(np.random.choice([2, 3], p=[0.6, 0.4]))
        else: # Technician, Representative, etc.
            job_levels.append(1)
    job_levels = np.array(job_levels)
    
    # 5. Compensation (Monthly Income aligned with Job Level + random variance)
    base_salaries = {
        1: (2800, 4200),
        2: (4500, 6800),
        3: (7000, 10500),
        4: (11000, 15500),
        5: (16000, 21000)
    }
    monthly_incomes = [
        int(np.random.uniform(base_salaries[lvl][0], base_salaries[lvl][1]))
        for lvl in job_levels
    ]
    
    # 6. Experience & Tenure (Logically bounded)
    years_at_company = []
    years_in_current_role = []
    years_since_promotion = []
    
    for age in ages:
        max_work_years = max(1, age - 21)
        company_tenure = np.random.randint(0, min(max_work_years, 26))
        years_at_company.append(company_tenure)
        
        role_tenure = np.random.randint(0, company_tenure + 1)
        years_in_current_role.append(role_tenure)
        
        promo_tenure = np.random.randint(0, max(1, role_tenure + 1))
        years_since_promotion.append(promo_tenure)
        
    years_at_company = np.array(years_at_company)
    years_in_current_role = np.array(years_in_current_role)
    years_since_promotion = np.array(years_since_promotion)
    
    # 7. Workplace Feedback & Ratings (Scale 1 to 4)
    # 1: Low, 2: Medium, 3: High, 4: Very High
    job_satisfaction = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.16, 0.28, 0.36, 0.20])
    env_satisfaction = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.15, 0.29, 0.35, 0.21])
    work_life_balance = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.12, 0.32, 0.42, 0.14])
    
    # Performance Rating: 1: Needs Improvement, 2: Good, 3: Excellent, 4: Outstanding
    performance_rating = np.random.choice([1, 2, 3, 4], size=num_records, p=[0.10, 0.40, 0.35, 0.15])
    
    # 8. Work Conditions & Engagement
    overtime = np.random.choice(["Yes", "No"], size=num_records, p=[0.28, 0.72])
    training_times = np.random.choice([0, 1, 2, 3, 4, 5, 6], size=num_records, p=[0.05, 0.15, 0.35, 0.25, 0.12, 0.05, 0.03])
    
    # Absenteeism (Days absent in the last year: 0 to 22 days, higher if low satisfaction)
    absenteeism = []
    for sat in job_satisfaction:
        if sat == 1:
            absenteeism.append(int(np.random.normal(12, 4)))
        elif sat == 2:
            absenteeism.append(int(np.random.normal(8, 3)))
        else:
            absenteeism.append(int(np.random.normal(4, 2)))
    absenteeism = np.clip(absenteeism, 0, 25)
    
    # 9. Realistic Attrition Risk Modeling (Synthesizing ground truth)
    # Calculating an attrition risk log-odds score based on empirical HR patterns
    attrition_flags = []
    for i in range(num_records):
        score = 0.0
        
        # Risk factor 1: Overtime
        if overtime[i] == "Yes":
            score += 1.4
            
        # Risk factor 2: Low Job Satisfaction
        if job_satisfaction[i] == 1:
            score += 1.2
        elif job_satisfaction[i] == 2:
            score += 0.5
        elif job_satisfaction[i] == 4:
            score -= 0.8
            
        # Risk factor 3: Work-life balance
        if work_life_balance[i] == 1:
            score += 1.1
        elif work_life_balance[i] == 4:
            score -= 0.6
            
        # Risk factor 4: Compensation vs Job Level
        # Low salary for their level triggers attrition
        expected_median = (base_salaries[job_levels[i]][0] + base_salaries[job_levels[i]][1]) / 2
        if monthly_incomes[i] < expected_median * 0.9:
            score += 0.9
            
        # Risk factor 5: Stagnation (Long time without promotion)
        if years_since_promotion[i] >= 4 and years_at_company[i] >= 5:
            score += 0.8
            
        # Risk factor 6: Early Career / Young Age job-hopping
        if ages[i] < 28:
            score += 0.6
            
        # Protective factor: High tenure with regular promotions
        if years_at_company[i] > 8 and years_since_promotion[i] <= 2:
            score -= 1.0
            
        # Baseline probability using sigmoid
        prob = 1 / (1 + np.exp(-(score - 1.6)))
        
        # Decide Attrition outcome
        attrition_flags.append("Yes" if np.random.rand() < prob else "No")
        
    df = pd.DataFrame({
        "EmployeeID": employee_ids,
        "Age": ages,
        "Gender": genders,
        "Department": departments,
        "JobRole": job_roles,
        "Education": education_levels,
        "JobLevel": job_levels,
        "MonthlyIncome": monthly_incomes,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_current_role,
        "YearsSinceLastPromotion": years_since_promotion,
        "JobSatisfaction": job_satisfaction,
        "EnvironmentSatisfaction": env_satisfaction,
        "WorkLifeBalance": work_life_balance,
        "PerformanceRating": performance_rating,
        "OverTime": overtime,
        "TrainingTimesLastYear": training_times,
        "Absenteeism": absenteeism,
        "Attrition": attrition_flags
    })
    
    return df

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(target_dir, "employee_data.csv")
    
    print(f"Generating realistic employee dataset with 500 records...")
    df = generate_employee_dataset(num_records=500, random_seed=42)
    
    df.to_csv(output_path, index=False)
    print(f"Dataset successfully created and saved to: {output_path}")
    print(f"Total Rows: {len(df)}, Total Columns: {len(df.columns)}")
    print("\nDataset Column Overview:")
    for col in df.columns:
        print(f" - {col} ({df[col].dtype})")
    
    attrition_counts = df["Attrition"].value_counts()
    attrition_rate = (attrition_counts.get("Yes", 0) / len(df)) * 100
    print(f"\nAttrition Summary:")
    print(f" - Retained ('No'): {attrition_counts.get('No', 0)}")
    print(f" - Left ('Yes'): {attrition_counts.get('Yes', 0)}")
    print(f" - Attrition Rate: {attrition_rate:.2f}%")

if __name__ == "__main__":
    main()
