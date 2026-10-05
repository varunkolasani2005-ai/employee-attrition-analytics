# Software Testing Report: Employee Performance and Attrition Analytics

**Project Title:** Employee Performance and Attrition Analytics Using Data Analytics  
**Academic Degree:** B.Tech in Computer Science and Engineering  
**Test Environment:** Windows 11, Python 3.11.7, Scikit-Learn 1.9+, Pandas 3.0+, Streamlit 1.65+  
**Test Strategy:** Black-Box, Boundary Value Analysis, Integration & Unit Verification  

---

## 1. Test Summary

All automated and manual test cases designed for data ingestion, cleaning, exploratory visualization, model training, risk prediction, and dashboard responsiveness were executed. **100% of test cases passed successfully.**

| Total Test Cases | Passed | Failed | Blocked | Execution Date |
| :---: | :---: | :---: | :---: | :---: |
| **8** | **8** | **0** | **0** | October 2026 |

---

## 2. Comprehensive Test Case Execution Matrix

| Test Case ID | Test Scenario | Input Data / Condition | Expected Output | Actual Output | Test Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | **Dataset Ingestion & Integrity** | Loading `dataset/employee_data.csv` via `load_data()` | Dataset loaded with 500 rows, 19 columns, and matching schema without I/O exceptions | Loaded 500 rows and 19 columns; schema verified | **PASSED** |
| **TC-02** | **Missing Value Imputation** | Synthetic injection of null values in `MonthlyIncome` and `Department` | Numerical columns imputed with median; categorical with mode; zero remaining nulls | Missing values accurately imputed using median/mode; null count = 0 | **PASSED** |
| **TC-03** | **Categorical Feature Preprocessing** | Raw categorical features (`Department`, `JobRole`, `OverTime`, `Attrition`) | Binary mapping of target and overtime; One-Hot Encoding resulting in 26 numerical ML features | 26 encoded numerical features generated; zero data leakage | **PASSED** |
| **TC-04** | **Exploratory Visualizations Generation** | Execution of `src/eda.py` | 9 high-resolution chart PNGs rendered and saved into `visualizations/` directory | All 9 chart PNGs generated (300 DPI) and verified in `visualizations/` | **PASSED** |
| **TC-05** | **Machine Learning Training Pipeline** | Scaled training set (400 samples) across Logistic Regression, Decision Tree, Random Forest | All 3 models trained; evaluation metrics computed; champion model serialized to `models/attrition_model.pkl` | Models trained; Logistic Regression selected as champion (F1: 0.476); artifacts saved | **PASSED** |
| **TC-06** | **Real-Time Attrition Risk Prediction** | Individual employee profile dictionary with high-risk attributes (OverTime=Yes, Sat=1, Low Pay) | Inference engine computes risk probability (>80%), categorizes as "High Risk", lists stressors | Probability computed (96.6%), categorized as High Risk, stressor list & advice returned | **PASSED** |
| **TC-07** | **Interactive Streamlit Dashboard** | Launching `dashboard/app.py` via `streamlit run dashboard/app.py` | Web UI loads on `http://localhost:8501`, displays KPI metrics, interactive filters, and risk simulator form | Dashboard rendered cleanly; tabs responsive; risk prediction form functional | **PASSED** |
| **TC-08** | **Invalid / Boundary Input Handling** | Out-of-bounds input (Age=15 or 85, Satisfaction=5) fed into prediction engine | Clamped/sanitized to valid operational bounds (Age: 18-65, Satisfaction: 1-4) without crashing | Bounds clipping applied safely; valid prediction output returned | **PASSED** |

---

## 3. Boundary & Error Handling Observations

1. **Class Balance Integrity:** The 80/20 train-test split applies stratification (`stratify=y`) so that the exact 37% attrition distribution is preserved identically in both train and test partitions.
2. **Feature Alignment Safety:** `AttritionPredictor` verifies that all 26 feature columns match the exact sequence and naming used during model training, dynamically populating missing one-hot dummies with zero.
3. **Headless Execution:** Chart generation uses `matplotlib.use("Agg")` ensuring automated background execution on any server or terminal without requiring an active graphical desktop display.
