# Employee Performance and Attrition Analytics Using Data Analytics

**B.Tech Computer Science Engineering Academic Capstone Project**  
**Academic Year:** 2025–2026 | **Domain:** Data Analytics & Supervised Machine Learning  

---

## 📌 Project Overview
This repository contains the complete, working implementation of the B.Tech academic project **Employee Performance and Attrition Analytics Using Data Analytics**.

The project addresses one of the most critical challenges in human resource management: analyzing employee performance patterns, diagnosing organizational turnover drivers (burnout, compensation disparity, promotion stagnation), and predicting individual employee attrition risk in real time.

---

## 🗂️ Complete Project Folder Structure

```
employee_performance_attrition/
│
├── dataset/
│   ├── employee_data.csv            # 500 employee records across 19 standard HR attributes
│   └── generate_dataset.py          # Script to generate reproducible, realistically correlated dataset
│
├── notebooks/
│   ├── employee_analysis.ipynb      # Complete interactive Jupyter Notebook for viva demonstration
│   └── build_notebook.py            # Generator script for Jupyter Notebook
│
├── src/
│   ├── __init__.py                  # Python package initializer
│   ├── data_preprocessing.py        # Module 2: Cleaning, imputation, One-Hot Encoding, scaling, split
│   ├── eda.py                       # Module 3: Exploratory Data Analysis & 9 chart generation
│   ├── performance_analysis.py      # Module 4: Performance rating breakdown & 0-100 composite scoring
│   ├── attrition_analysis.py        # Module 5: Attrition diagnostics by dept, role, salary, overtime
│   ├── model_training.py            # Module 6: Trains Logistic Regression, Decision Tree, Random Forest
│   └── prediction.py                # Module 6: Real-time inference engine & risk prescription
│
├── models/
│   ├── attrition_model.pkl          # Trained champion classification model (Logistic Regression)
│   ├── scaler.pkl                   # Fitted StandardScaler object
│   ├── feature_names.json           # List of 26 one-hot encoded features
│   └── model_metadata.json          # Benchmark evaluation metrics & explainability metadata
│
├── dashboard/
│   └── app.py                       # Module 7: Full interactive Streamlit Web Dashboard
│
├── visualizations/                  # 12 high-resolution generated chart PNGs (300 DPI)
│   ├── 01_age_income_distribution.png
│   ├── 02_gender_department_distribution.png
│   ├── 03_monthly_income_by_role.png
│   ├── 04_job_satisfaction_worklife.png
│   ├── 05_overtime_vs_attrition.png
│   ├── 06_department_performance.png
│   ├── 07_tenure_vs_income_scatter.png
│   ├── 08_absenteeism_vs_satisfaction.png
│   ├── 09_correlation_heatmap.png
│   ├── 10_model_comparison.png
│   ├── 11_confusion_matrices.png
│   └── 12_feature_importance.png
│
├── reports/
│   ├── project_report.md            # Comprehensive 34-chapter academic documentation report
│   ├── presentation_slides.md       # 20-slide presentation script with visuals and verbal scripts
│   ├── viva_questions_answers.md    # 20 curated technical viva questions and detailed answers
│   └── testing_report.md            # Complete test cases matrix (8 core test scenarios)
│
├── requirements.txt                 # Pinned Python package dependencies
├── run_pipeline.py                  # Single-command pipeline runner (Modules 1 through 6)
├── run_project.bat                  # Interactive Windows batch launcher menu
└── README.md                        # Master beginner-friendly guide and documentation
```

---

## ⚙️ Quick Start Guide for Beginners

### Step 1: Open Terminal / PowerShell
Navigate to the project root directory:
```powershell
cd C:\Users\varun\.gemini\antigravity\scratch\employee_performance_attrition
```

### Step 2: Install Required Libraries
Install all required libraries using the pinned `requirements.txt`:
```powershell
pip install -r requirements.txt
```
*(Dependencies: pandas, numpy, matplotlib, seaborn, scikit-learn, streamlit, joblib)*

---

## 🚀 How to Run the Project (Exact Terminal Commands)

### Option A: The One-Command Master Pipeline (Recommended)
To generate the dataset, clean the data, create all 12 charts, calculate performance metrics, train all 3 machine learning models, and run a sample test prediction:
```powershell
python run_pipeline.py
```
**Expected Output:**
- Prints execution steps 1 through 7 in the terminal.
- Saves `dataset/employee_data.csv`.
- Generates 12 high-resolution chart PNGs into `visualizations/`.
- Saves `models/attrition_model.pkl`, `models/scaler.pkl`, and `models/feature_names.json`.
- Runs in approximately 6 to 10 seconds.

---

### Option B: Launch the Interactive Streamlit Web Dashboard
To launch the interactive web dashboard for demonstration to college lecturers:
```powershell
streamlit run dashboard/app.py
```
**Expected Output:**
- Automatically opens your web browser at: `http://localhost:8501`.
- Displays top KPI metric cards (Headcount, Attrition Rate, Avg Salary, Performance).
- Provides dynamic sidebar filters for Department, Job Role, Gender, and Tenure.
- Features 6 interactive tabs: Executive Overview, Performance Analytics, Attrition Diagnostics, Machine Learning Benchmarks, Live Risk Predictor, and Strategic HR Insights.

---

### Option C: Interactive Windows Menu Launcher
On Windows, you can simply run:
```powershell
.\run_project.bat
```
This presents an interactive menu with options `[1]` to Run Pipeline, `[2]` to Launch Dashboard, `[3]` to Run All, `[4]` to Test Inference, and `[5]` to Exit.

---

### Option D: Run Individual Modules (Step-by-Step)

If your professor asks you to demonstrate a specific module individually:

1. **Module 1 – Dataset Generation:**
   ```powershell
   python dataset/generate_dataset.py
   ```
2. **Module 2 – Data Preprocessing & Scaling:**
   ```powershell
   python src/data_preprocessing.py
   ```
3. **Module 3 – Exploratory Data Analysis (EDA):**
   ```powershell
   python src/eda.py
   ```
4. **Module 4 – Employee Performance Analytics:**
   ```powershell
   python src/performance_analysis.py
   ```
5. **Module 5 – Employee Attrition Analytics:**
   ```powershell
   python src/attrition_analysis.py
   ```
6. **Module 6 – Machine Learning Model Training:**
   ```powershell
   python src/model_training.py
   ```
7. **Module 6 (Inference) – Real-Time Attrition Prediction:**
   ```powershell
   python src/prediction.py
   ```

---

## 📊 Summary of Machine Learning Benchmark Results

All models were evaluated on an independent 20% holdout test set (100 samples) under identical 80/20 stratified conditions:

| Algorithm | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Champion)** | **67.00%** | **0.577** | **0.405** | **0.476** | **0.646** |
| **Random Forest Classifier** | 65.00% | 0.562 | 0.243 | 0.340 | 0.633 |
| **Decision Tree Classifier** | 61.00% | 0.458 | 0.297 | 0.361 | 0.602 |

> **Academic Note:** Logistic Regression was selected as the champion model because it achieved the highest balanced F1-score (0.476) and highest recall on the imbalanced attrition target.

---

## 🛠️ Common Errors & Troubleshooting

1. **`ModuleNotFoundError: No module named 'streamlit'` (or `sklearn`, `seaborn`)**  
   *Fix:* Run `pip install -r requirements.txt` in your active terminal.

2. **`FileNotFoundError: Dataset file not found`**  
   *Fix:* Run `python dataset/generate_dataset.py` or run `python run_pipeline.py` from the project root.

3. **`FileNotFoundError: Model file not found at models/attrition_model.pkl`**  
   *Fix:* The machine learning model must be trained first. Run `python src/model_training.py`.

4. **Port 8501 is already in use by another Streamlit process**  
   *Fix:* Launch Streamlit on an alternative port:
   ```powershell
   streamlit run dashboard/app.py --server.port 8502
   ```

---

## 🎓 Academic Presentation Resources
All academic documentation is located in the `reports/` folder:
- **34-Chapter Project Report:** [`reports/project_report.md`](reports/project_report.md)
- **20-Slide Viva Presentation Content:** [`reports/presentation_slides.md`](reports/presentation_slides.md)
- **20 Curated Viva Questions & Detailed Answers:** [`reports/viva_questions_answers.md`](reports/viva_questions_answers.md)
- **Formal Software Testing Report:** [`reports/testing_report.md`](reports/testing_report.md)
- **Interactive Demonstration Notebook:** [`notebooks/employee_analysis.ipynb`](notebooks/employee_analysis.ipynb)
