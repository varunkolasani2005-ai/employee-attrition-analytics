"""
Master Pipeline Runner: Employee Performance and Attrition Analytics
B.Tech Academic Project Automation Script

This script sequentially executes all analytical and machine learning stages:
1. Module 1: Dataset Generation (dataset/generate_dataset.py)
2. Module 2: Data Preprocessing & Scaling (src/data_preprocessing.py)
3. Module 3: Exploratory Data Analysis Charts (src/eda.py)
4. Module 4: Performance Analytics (src/performance_analysis.py)
5. Module 5: Attrition Analytics (src/attrition_analysis.py)
6. Module 6: Model Training & Evaluation (src/model_training.py)
7. Verification of Output Artifacts & Launch Instructions
"""

import os
import sys
import time

def print_step_header(step_num, title):
    print("\n" + "=" * 70)
    print(f" STEP {step_num}: {title.upper()}")
    print("=" * 70)

def main():
    start_time = time.time()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("*" * 70)
    print("  EMPLOYEE PERFORMANCE & ATTRITION ANALYTICS PIPELINE RUNNER  ")
    print("  B.Tech Computer Science Engineering Academic Project        ")
    print("*" * 70)
    
    # Step 1: Generate Dataset
    print_step_header(1, "Generating Dataset (Module 1)")
    from dataset.generate_dataset import generate_employee_dataset
    csv_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    df = generate_employee_dataset(500, random_seed=42)
    df.to_csv(csv_path, index=False)
    print(f"-> Dataset saved to: {csv_path} ({len(df)} records)")
    
    # Step 2: Data Preprocessing & Scaling
    print_step_header(2, "Data Cleaning & Preprocessing (Module 2)")
    from src.data_preprocessing import prepare_train_test_data
    models_dir = os.path.join(base_dir, "models")
    X_train_sc, X_test_sc, y_train, y_test, feature_names, scaler, clean_df = prepare_train_test_data(
        csv_path, models_dir=models_dir
    )
    print(f"-> Preprocessing finished. Train set: {len(X_train_sc)}, Test set: {len(X_test_sc)}")
    
    # Step 3: Exploratory Data Analysis
    print_step_header(3, "Exploratory Data Analysis (Module 3)")
    from src.eda import generate_eda_charts
    vis_dir = os.path.join(base_dir, "visualizations")
    saved_charts = generate_eda_charts(clean_df, vis_dir)
    print(f"-> Generated {len(saved_charts)} high-resolution charts in {vis_dir}")
    
    # Step 4: Employee Performance Analytics
    print_step_header(4, "Employee Performance Analytics (Module 4)")
    from src.performance_analysis import analyze_performance, print_performance_summary
    perf_results = analyze_performance(clean_df)
    print_performance_summary(perf_results)
    
    # Step 5: Employee Attrition Analytics
    print_step_header(5, "Employee Attrition Analytics (Module 5)")
    from src.attrition_analysis import analyze_attrition, print_attrition_summary
    attr_results = analyze_attrition(clean_df)
    print_attrition_summary(attr_results)
    
    # Step 6: Machine Learning Training & Model Selection
    print_step_header(6, "Machine Learning Training & Benchmarks (Module 6)")
    from src.model_training import train_and_evaluate_models, save_model_comparison_plots
    ml_results = train_and_evaluate_models(X_train_sc, X_test_sc, y_train, y_test, feature_names)
    
    best_name = None
    highest_f1 = -1.0
    for name, r in ml_results.items():
        if r["f1_score"] > highest_f1:
            highest_f1 = r["f1_score"]
            best_name = name
            
    import joblib, json
    best_model = ml_results[best_name]["model"]
    model_path = os.path.join(models_dir, "attrition_model.pkl")
    joblib.dump(best_model, model_path)
    
    save_model_comparison_plots(ml_results, feature_names, best_name, vis_dir)
    
    metadata = {
        "best_model": best_name,
        "metrics": {
            k: {m: v for m, v in val.items() if m not in ["model", "predictions", "probabilities"]}
            for k, val in ml_results.items()
        },
        "feature_count": len(feature_names),
        "disclaimer": "This model calculates statistical attrition risk probability based on historical training patterns."
    }
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    print(f"\n-> Selected Champion Model: {best_name} (F1-Score: {highest_f1:.3f})")
    print(f"-> Model saved to: {model_path}")
    
    # Step 7: Sample Prediction
    print_step_header(7, "Verification of Real-Time Prediction Engine")
    from src.prediction import AttritionPredictor
    predictor = AttritionPredictor(models_dir)
    sample_emp = {
        "Age": 28, "Gender": "Male", "Department": "Sales", "JobRole": "Sales Representative",
        "Education": "Bachelor", "JobLevel": 1, "MonthlyIncome": 3200, "YearsAtCompany": 2,
        "YearsInCurrentRole": 2, "YearsSinceLastPromotion": 2, "JobSatisfaction": 1,
        "EnvironmentSatisfaction": 2, "WorkLifeBalance": 1, "PerformanceRating": 2,
        "OverTime": "Yes", "TrainingTimesLastYear": 1, "Absenteeism": 12
    }
    pred_res = predictor.predict_risk(sample_emp)
    print(f"Sample Prediction Test:")
    print(f" - Risk Tier: {pred_res['risk_tier']} ({pred_res['attrition_probability']}%)")
    print(f" - Status: {pred_res['retention_status']}")
    
    elapsed = time.time() - start_time
    print("\n" + "*" * 70)
    print(f"  ALL MODULES EXECUTED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print("*" * 70)
    print("\nHOW TO LAUNCH THE INTERACTIVE STREAMLIT DASHBOARD:")
    print("  Command: streamlit run dashboard/app.py")
    print("\nHOW TO OPEN IN BROWSER:")
    print("  URL: http://localhost:8501")
    print("*" * 70)

if __name__ == "__main__":
    main()
