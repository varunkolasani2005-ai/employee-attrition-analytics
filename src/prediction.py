"""
Module 6 (Inference): Attrition Risk Prediction Engine
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module provides real-time risk assessment for individual employee profiles:
1. Loads the champion trained model (attrition_model.pkl)
2. Loads the feature scaler and feature alignment dictionary
3. Prepares input raw employee attributes into the exact one-hot encoded vector
4. Computes Attrition Risk Probability (0.0% to 100.0%)
5. Categorizes Risk into Tiers: Low Risk, Moderate Risk, High Risk
6. Diagnoses individual risk drivers (e.g., OverTime, Salary gaps, Satisfaction)
7. Generates actionable HR retention recommendations
"""

import os
import json
import joblib
import numpy as np
import pandas as pd

class AttritionPredictor:
    """
    Inference class to predict employee attrition risk from raw HR attributes.
    """
    def __init__(self, models_dir=None):
        if models_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_dir = os.path.join(base_dir, "models")
            
        self.model_path = os.path.join(models_dir, "attrition_model.pkl")
        self.scaler_path = os.path.join(models_dir, "scaler.pkl")
        self.features_path = os.path.join(models_dir, "feature_names.json")
        
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at {self.model_path}. Run model_training.py first.")
            
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        with open(self.features_path, "r") as f:
            self.feature_names = json.load(f)

    def _prepare_vector(self, employee_data):
        """
        Converts a dictionary or single-row DataFrame of employee attributes
        into a scaled numerical vector matching the model's training columns.
        """
        df_input = pd.DataFrame([employee_data])
        
        # Binary encoding
        df_input["OverTime"] = df_input["OverTime"].map({"Yes": 1, "No": 0})
        
        # Multi-class one-hot encoding
        cat_cols = ["Department", "JobRole", "Education", "Gender"]
        df_encoded = pd.get_dummies(df_input, columns=cat_cols, drop_first=True, dtype=int)
        
        # Align with training features (create all expected columns with default 0 if missing)
        for col in self.feature_names:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
                
        # Order columns identically
        df_aligned = df_encoded[self.feature_names]
        
        # Scale features
        X_scaled = self.scaler.transform(df_aligned)
        return X_scaled

    def predict_risk(self, employee_data):
        """
        Predicts attrition probability, risk category, and key factors for an employee.
        
        Parameters:
        - employee_data (dict): Dictionary of employee features.
        
        Returns:
        - dict: Structured prediction assessment.
        """
        X_scaled = self._prepare_vector(employee_data)
        
        # Predict probability
        if hasattr(self.model, "predict_proba"):
            prob_attrition = float(self.model.predict_proba(X_scaled)[0, 1])
        else:
            pred = int(self.model.predict(X_scaled)[0])
            prob_attrition = 0.85 if pred == 1 else 0.15
            
        prob_percent = round(prob_attrition * 100, 1)
        
        # Determine Risk Tier
        if prob_percent < 35.0:
            risk_tier = "Low Risk"
            risk_color = "Green"
            retention_status = "Employee appears well-engaged and stable."
        elif prob_percent < 60.0:
            risk_tier = "Moderate Risk"
            risk_color = "Orange"
            retention_status = "Employee displays emerging attrition indicators. Proactive check-in recommended."
        else:
            risk_tier = "High Risk"
            risk_color = "Red"
            retention_status = "Employee is at high risk of departure. Immediate HR intervention advised."
            
        # Analyze individual risk contributors
        detected_risks = []
        if employee_data.get("OverTime") == "Yes":
            detected_risks.append("Sustained Overtime Demand (High burnout risk)")
        if employee_data.get("JobSatisfaction", 3) <= 2:
            detected_risks.append("Sub-optimal Job Satisfaction Rating (<= 2/4)")
        if employee_data.get("WorkLifeBalance", 3) <= 2:
            detected_risks.append("Impaired Work-Life Balance Rating (<= 2/4)")
        if employee_data.get("YearsSinceLastPromotion", 0) >= 4 and employee_data.get("YearsAtCompany", 0) >= 4:
            detected_risks.append("Promotion Stagnation (>= 4 years without role advancement)")
        if employee_data.get("MonthlyIncome", 6000) < 4000:
            detected_risks.append("Low Compensation Bracket relative to industry benchmark")
            
        if not detected_risks:
            detected_risks.append("No critical organizational stressors detected in current profile.")
            
        # Retention Recommendations
        recommendations = []
        if employee_data.get("OverTime") == "Yes":
            recommendations.append("Review project distribution to alleviate chronic overtime workload.")
        if employee_data.get("YearsSinceLastPromotion", 0) >= 4:
            recommendations.append("Initiate internal career development and role appraisal discussion.")
        if employee_data.get("JobSatisfaction", 3) <= 2 or employee_data.get("WorkLifeBalance", 3) <= 2:
            recommendations.append("Schedule 1-on-1 mentorship session with people manager to address workplace feedback.")
        if employee_data.get("MonthlyIncome", 6000) < 4000:
            recommendations.append("Evaluate market parity salary adjustment or performance-linked incentive.")
        if not recommendations:
            recommendations.append("Maintain regular performance reviews and provide leadership enablement opportunities.")
            
        return {
            "attrition_probability": prob_percent,
            "risk_tier": risk_tier,
            "risk_color": risk_color,
            "retention_status": retention_status,
            "detected_risks": detected_risks,
            "recommendations": recommendations,
            "disclaimer": "This score represents an estimated probability based on statistical trends in workforce data and is intended solely for decision support."
        }

def main():
    print("=" * 65)
    print("      MODULE 6 (INFERENCE): REAL-TIME ATTRITION PREDICTION    ")
    print("=" * 65)
    
    predictor = AttritionPredictor()
    
    # Test Profile 1: High Risk Profile (Overtime, Low satisfaction, Low pay)
    high_risk_employee = {
        "Age": 26,
        "Gender": "Male",
        "Department": "Sales",
        "JobRole": "Sales Representative",
        "Education": "Bachelor",
        "JobLevel": 1,
        "MonthlyIncome": 3100,
        "YearsAtCompany": 3,
        "YearsInCurrentRole": 2,
        "YearsSinceLastPromotion": 3,
        "JobSatisfaction": 1,
        "EnvironmentSatisfaction": 1,
        "WorkLifeBalance": 1,
        "PerformanceRating": 2,
        "OverTime": "Yes",
        "TrainingTimesLastYear": 1,
        "Absenteeism": 14
    }
    
    print("\n--- Test Profile 1: Junior Sales Rep with Overtime & Low Satisfaction ---")
    res1 = predictor.predict_risk(high_risk_employee)
    print(f"Attrition Probability: {res1['attrition_probability']}%")
    print(f"Risk Tier:             {res1['risk_tier']}")
    print(f"Status:                {res1['retention_status']}")
    print("Identified Stressors:")
    for r in res1["detected_risks"]:
        print(f" - {r}")
    print("Recommended HR Actions:")
    for a in res1["recommendations"]:
        print(f" * {a}")
        
    # Test Profile 2: Low Risk Profile (No Overtime, High Satisfaction, Good Pay)
    low_risk_employee = {
        "Age": 42,
        "Gender": "Female",
        "Department": "Research & Development",
        "JobRole": "Research Scientist",
        "Education": "Doctorate",
        "JobLevel": 3,
        "MonthlyIncome": 9800,
        "YearsAtCompany": 8,
        "YearsInCurrentRole": 4,
        "YearsSinceLastPromotion": 1,
        "JobSatisfaction": 4,
        "EnvironmentSatisfaction": 4,
        "WorkLifeBalance": 3,
        "PerformanceRating": 3,
        "OverTime": "No",
        "TrainingTimesLastYear": 3,
        "Absenteeism": 3
    }
    
    print("\n--- Test Profile 2: Senior Scientist with Strong Satisfaction & Fair Pay ---")
    res2 = predictor.predict_risk(low_risk_employee)
    print(f"Attrition Probability: {res2['attrition_probability']}%")
    print(f"Risk Tier:             {res2['risk_tier']}")
    print(f"Status:                {res2['retention_status']}")
    print("Identified Stressors:")
    for r in res2["detected_risks"]:
        print(f" - {r}")
    print("Recommended HR Actions:")
    for a in res2["recommendations"]:
        print(f" * {a}")
    print("=" * 65)

if __name__ == "__main__":
    main()
