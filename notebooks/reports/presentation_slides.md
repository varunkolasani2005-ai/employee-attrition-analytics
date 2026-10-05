# Academic Presentation Slides Content (20 Slides)

**Project Title:** Employee Performance and Attrition Analytics Using Data Analytics  
**Degree:** Bachelor of Technology in Computer Science & Engineering (B.Tech CSE)  
**Format:** Presentation Deck Structure with Slide Bullets, Visual References, and Verbal Presentation Scripts  

---

### Slide 1: Title Slide
- **Slide Title:** Employee Performance and Attrition Analytics Using Data Analytics
- **Bullet Points:**
  - Capstone B.Tech Academic Project Presentation
  - Domain: Human Resource Data Analytics & Supervised Machine Learning
  - Student Presenter: B.Tech Computer Science and Engineering
  - Department of Computer Science & Engineering
  - Academic Year: 2026
- **Suggested Visual:** University Crest / Logo alongside high-tech HR Analytics banner diagram.
- **Verbal Explanation Script:**  
  *"Good morning respected evaluators, project coordinator, and faculty members. Today I am presenting my B.Tech CSE capstone project titled 'Employee Performance and Attrition Analytics Using Data Analytics'. This project bridges data science techniques with organizational human resource management to proactively analyze employee performance and predict attrition risk."*

---

### Slide 2: Introduction
- **Slide Title:** Introduction to HR Analytics
- **Bullet Points:**
  - Human capital represents the most valuable yet volatile asset of any enterprise.
  - Unplanned employee turnover disrupts operations, damages morale, and incurs massive replacement costs (upwards of 50-200% of annual salary).
  - Modern organizations generate vast volumes of internal employee data across appraisals, surveys, and attendance.
  - Transitioning from reactive exit interviews to proactive data-driven workforce analytics is critical.
- **Suggested Visual:** Conceptual diagram showing Employee Data $\to$ Machine Learning $\to$ Proactive HR Retention Decisions.
- **Verbal Explanation Script:**  
  *"In modern knowledge economies, replacing skilled talent costs companies up to double an employee's annual salary when factoring in recruiting, onboarding, and lost productivity. While traditional HR approaches rely on exit interviews after an employee has already resigned, data analytics allows us to identify dissatisfaction and burnout before departure occurs."*

---

### Slide 3: Problem Statement
- **Slide Title:** Problem Statement
- **Bullet Points:**
  - High and unpredictable voluntary employee attrition across knowledge-intensive sectors.
  - Inability of traditional human resource teams to identify subtle, multi-factor burnout patterns across departments.
  - Disconnect between employee performance appraisals, compensation parity, and career progression timelines.
  - Lack of accessible, centralized predictive decision-support tools for talent managers.
- **Suggested Visual:** Infographic showing the cycle of Overtime $\to$ Low Satisfaction $\to$ Unnoticed Burnout $\to$ Sudden Resignation.
- **Verbal Explanation Script:**  
  *"The core problem we address is that voluntary employee turnover is often multi-factorial and difficult to identify manually. A manager might notice an employee working overtime, but miss that their compensation is below market median and their promotion has stagnated for four years. Without analytics, these compound stressors lead to unexpected resignations."*

---

### Slide 4: Project Objectives
- **Slide Title:** Project Objectives
- **Bullet Points:**
  - **Data Curation & Preprocessing:** Clean, encode, and standardize comprehensive employee datasets.
  - **Exploratory Data Analysis (EDA):** Uncover statistical correlations between demographics, compensation, and turnover.
  - **Performance Evaluation:** Develop an objective 0-100 Composite Performance Score combining ratings, training, and attendance.
  - **Predictive Modeling:** Train and benchmark classification algorithms (Logistic Regression, Decision Tree, Random Forest).
  - **Interactive Web Dashboard:** Build a real-time Streamlit dashboard with dynamic filtering and live risk simulation.
- **Suggested Visual:** 5-step numbered roadmap diagram illustrating the five main project phases.
- **Verbal Explanation Script:**  
  *"Our objectives are structured across five key pillars: first, robust data engineering; second, in-depth statistical exploratory analysis; third, an objective composite performance scoring model; fourth, machine learning classification to estimate attrition probabilities; and finally, deploying an interactive Streamlit dashboard for real-time risk assessment."*

---

### Slide 5: Existing System & Its Limitations
- **Slide Title:** Existing System & Limitations
- **Bullet Points:**
  - **Existing System:**
    - Manual spreadsheets (Excel) managed locally with disjointed records.
    - Periodic subjective annual performance reviews.
    - Post-mortem exit interviews conducted after resignation notices are submitted.
  - **Major Limitations:**
    - Purely retrospective—identifies problems only after talent is lost.
    - Vulnerable to human appraisal bias and recency effects.
    - Inability to uncover non-linear relationships across hundreds of attributes.
- **Suggested Visual:** Comparison diagram showing 'Traditional HR: Purely Reactive' vs 'Analytics-Driven HR: Proactive'.
- **Verbal Explanation Script:**  
  *"Existing HR systems are overwhelmingly reactive. Spreadsheets are kept in silos, appraisals happen once a year, and the primary mechanism for understanding attrition is the exit interview. By that point, the organization has already lost the employee and the intellectual property they hold."*

---

### Slide 6: Research Gap & Industry Need
- **Slide Title:** Research Gap
- **Bullet Points:**
  - Most existing literature analyzes attrition in isolation without linking it directly to granular performance indexes.
  - Commercial enterprise HR software (e.g., Workday, SAP SuccessFactors) are expensive proprietary black-boxes inaccessible to mid-market firms.
  - Existing open-source predictive scripts lack accessible web user interfaces for non-technical HR managers.
  - Need for an end-to-end, interpretable framework with actionable prescriptive retention recommendations.
- **Suggested Visual:** Venn diagram showing the intersection of Data Science, HR Management, and Interactive Dashboarding.
- **Verbal Explanation Script:**  
  *"Our review of existing research highlighted two critical gaps: first, academic studies often treat attrition as a purely mathematical classification problem without generating actionable HR retention policies; second, existing tools rarely integrate transparent performance metrics alongside real-time web simulation for people managers."*

---

### Slide 7: Proposed System Architecture
- **Slide Title:** Proposed System Architecture
- **Bullet Points:**
  - End-to-end modular pipeline consisting of 8 cohesive subsystems.
  - Scalable data preprocessing layer with automated imputation, encoding, and standardization.
  - Dual analytical branches: Performance Analytics Engine and Attrition Analytics Engine.
  - Model benchmarking suite evaluating Logistic Regression, Decision Tree, and Random Forest.
  - Web deployment layer powered by Streamlit connecting serialized models with interactive front-end widgets.
- **Suggested Visual:** High-level System Architecture Mermaid Block Diagram (Data $\to$ Preprocessing $\to$ Analysis $\to$ ML $\to$ Streamlit UI).
- **Verbal Explanation Script:**  
  *"The proposed system architecture is designed as a modular pipeline. Raw HR records are validated, cleaned, and normalized. They feed into two analytical engines—one for workforce performance and one for attrition diagnostics. Preprocessed data trains multiple machine learning classifiers, and the champion model is served through a responsive Streamlit web application."*

---

### Slide 8: System Workflow & Use Case Model
- **Slide Title:** System Workflow & Actors
- **Bullet Points:**
  - **Workflow:** Input Dataset $\to$ Cleaning $\to$ EDA $\to$ Performance Scoring $\to$ Feature Scaling $\to$ Model Training $\to$ Inference Engine $\to$ Dashboard.
  - **Primary Actors:**
    - **Data Analyst:** Ingests data, configures features, evaluates ML benchmarks.
    - **HR Manager:** Explores departmental trends, identifies at-risk cohorts, receives retention recommendations.
    - **System Administrator:** Maintains data integrity and deploys dashboard updates.
- **Suggested Visual:** UML Use Case Diagram showing HR Manager, Analyst, and Administrator interacting with system use cases.
- **Verbal Explanation Script:**  
  *"This workflow traces the data lifecycle from raw CSV ingestion to model prediction. Three primary actors benefit: the Data Analyst oversees feature engineering and model training; the HR Manager utilizes the interactive dashboard and risk simulator to guide retention interventions; and the Administrator ensures system availability."*

---

### Slide 9: Dataset Description & Schema
- **Slide Title:** Dataset Description & Schema
- **Bullet Points:**
  - 500 employee records modeled after standard enterprise schemas (IBM HR Analytics).
  - 19 standardized attributes covering demographic, organizational, and behavioral metrics.
  - **Key Variables:**
    - *Demographics:* Age, Gender, Education.
    - *Job Structure:* Department, JobRole, JobLevel, MonthlyIncome.
    - *Tenure:* YearsAtCompany, YearsInCurrentRole, YearsSinceLastPromotion.
    - *Workplace Metrics:* JobSatisfaction, WorkLifeBalance, OverTime, Absenteeism.
    - *Target Variable:* Attrition (`Yes` / `No`).
- **Suggested Visual:** Dataset schema table showing variable names, data types, and operational value ranges.
- **Verbal Explanation Script:**  
  *"Our dataset comprises 500 employee records with 19 distinct features across three departments—Research & Development, Sales, and Human Resources. The data reflects realistic organizational dynamics, capturing both demographic variables and workplace sentiment ratings on standardized 1 to 4 scales."*

---

### Slide 10: Data Cleaning & Preprocessing (Module 2)
- **Slide Title:** Data Cleaning & Preprocessing Pipeline
- **Bullet Points:**
  - **Deduplication:** Automatic verification of unique employee identifiers.
  - **Imputation:** Median replacement for numerical features; Mode replacement for categorical features.
  - **Categorical Transformation:** Target variable (`Attrition`) and `OverTime` converted to binary numerical flags.
  - **One-Hot Encoding:** Multi-class nominal variables (`Department`, `JobRole`, `Education`, `Gender`) encoded with `drop_first=True` (expanding to 26 ML features).
  - **Feature Scaling:** `StandardScaler` applied to normalize numerical scales to zero mean and unit variance.
- **Suggested Visual:** Flowchart showing raw columns transforming into scaled 26-feature numerical matrix.
- **Verbal Explanation Script:**  
  *"Module 2 transforms raw data into an ML-ready state. We handle potential null values using median and mode imputation, encode categorical variables into 26 numerical features using One-Hot Encoding while dropping first columns to prevent multicollinearity, and standardize all numerical inputs using StandardScaler."*

---

### Slide 11: Exploratory Data Analysis - Demographics (Module 3)
- **Slide Title:** Exploratory Data Analysis: Demographics & Roles
- **Bullet Points:**
  - **Age Spread:** Normally distributed around median age of 39 years (range: 21 to 58).
  - **Workforce Distribution:** Research & Development (52.4%), Sales (37.0%), Human Resources (10.6%).
  - **Gender Diversity:** 58% Male to 42% Female representation across departments.
  - **Compensation Hierarchy:** Median monthly salary increases monotonically with Job Level (\$3.5k at Level 1 to \$18.5k at Level 5).
- **Suggested Visual:** Side-by-side plots: Age Distribution Histogram with KDE and Department Headcount Bar Chart.
- **Verbal Explanation Script:**  
  *"During Exploratory Data Analysis, we first inspected workforce demographics. We observed a balanced age curve centered around 39 years, with R&D being the largest department at 52.4%. Salary spreads conform accurately to organizational hierarchies, scaling systematically from entry-level to director-level positions."*

---

### Slide 12: Exploratory Data Analysis - Stressors & Heatmap (Module 3)
- **Slide Title:** Exploratory Data Analysis: Behavioral Stressors
- **Bullet Points:**
  - **Correlation Heatmap:** Highlighted strong positive relationships between Job Level and Monthly Income ($r = 0.89$), and Years at Company with Years in Current Role ($r = 0.76$).
  - **Absenteeism vs Satisfaction:** Employees with lowest satisfaction (Rating 1) average 12.4 absent days versus 4.1 days for Rating 4.
  - **OverTime Disparity:** Stacked analysis revealed mandatory overtime workers depart at nearly double the baseline rate.
- **Suggested Visual:** High-resolution Pearson Correlation Matrix Heatmap generated from `visualizations/09_correlation_heatmap.png`.
- **Verbal Explanation Script:**  
  *"The correlation heatmap validates key operational relationships. Crucially, we observe that low job satisfaction directly correlates with higher absenteeism. Furthermore, the cross-tabulation of overtime against attrition reveals that employees subjected to chronic overtime leave the company at nearly double the rate of standard-hour employees."*

---

### Slide 13: Employee Performance Analytics (Module 4)
- **Slide Title:** Employee Performance Analytics & Scoring
- **Bullet Points:**
  - Annual appraisal rating distribution: Needs Improvement (12.0%), Average (40.6%), High (31.6%), Outstanding (15.8%).
  - Developed a comprehensive **0-100 Composite Performance Index**:
    $$\text{Score} = \left(\frac{\text{Rating}}{4} \times 50\right) + \left(\frac{\text{Training}}{6} \times 20\right) + \left(\left(1 - \frac{\text{Absenteeism}}{25}\right) \times 15\right) + \left(\frac{\text{Satisfaction}}{4} \times 15\right)$$
  - Departmental composite averages remain tightly aligned: R&D (60.77), HR (60.43), Sales (59.88).
  - Successfully segregated top benchmark performers from employees requiring performance improvement programs.
- **Suggested Visual:** Histogram of Composite Performance Scores and Top 5 Performers leaderboard table.
- **Verbal Explanation Script:**  
  *"In Module 4, we enhanced traditional 1-to-4 ratings by creating a normalized 0-to-100 Composite Performance Score. By incorporating training attendance, low absenteeism, and engagement alongside raw manager ratings, we obtain a fair, objective measure of employee organizational contribution."*

---

### Slide 14: Employee Attrition Diagnostics (Module 5)
- **Slide Title:** Employee Attrition Analytics & Root Causes
- **Bullet Points:**
  - Overall organizational attrition rate observed at **37.0%** (185 departures out of 500 staff).
  - **Department Attrition:** Human Resources (39.6%), Sales (37.8%), Research & Development (35.9%).
  - **OverTime Risk Multiplier:** Overtime staff exhibit **56.8% attrition** vs **29.9%** for non-overtime staff.
  - **Satisfaction Risk:** Lowest satisfaction employees show **57.5% attrition** vs **25.8%** for highest satisfaction.
  - **Tenure Stagnation:** Employees without promotions for $\ge 4$ years show significantly increased departure probability.
- **Suggested Visual:** Grouped Bar Chart of OverTime vs Attrition and Satisfaction vs Attrition (`visualizations/05_overtime_vs_attrition.png`).
- **Verbal Explanation Script:**  
  *"Module 5 quantifies the primary drivers of voluntary employee departure. The numbers are unmistakable: mandatory overtime increases attrition from 29.9% to 56.8%. Similarly, employees in the lowest satisfaction bracket depart at more than double the rate of highly satisfied colleagues, with promotion stagnation acting as a compounding trigger."*

---

### Slide 15: Machine Learning Methodology & Training (Module 6)
- **Slide Title:** Machine Learning Methodology & Pipeline
- **Bullet Points:**
  - Supervised binary classification formulated to predict target $y \in \{0, 1\}$.
  - 80/20 Stratified Train-Test Split (400 training samples, 100 testing samples).
  - Implemented three distinct algorithm families:
    1. *Logistic Regression:* Linear log-odds decision boundary.
    2. *Decision Tree:* Non-linear hierarchical splits (Max Depth = 5).
    3. *Random Forest:* 120-tree bagging ensemble with feature subspace sampling.
  - Rigorous evaluation across Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
- **Suggested Visual:** Scikit-Learn training workflow diagram (Data $\to$ Train/Test Split $\to$ Scaling $\to$ Model Fitting $\to$ Benchmarking).
- **Verbal Explanation Script:**  
  *"In Module 6, we implemented supervised machine learning. We split the data into 80% training and 20% testing sets using stratification to maintain exact class proportions. We trained Logistic Regression, Decision Trees, and Random Forests, optimizing hyper-parameters to avoid overfitting."*

---

### Slide 16: Model Evaluation, Comparison & Selection (Module 6)
- **Slide Title:** Model Benchmarks & Champion Selection
- **Bullet Points:**
  - **Benchmark Evaluation Results on Test Set:**
    - *Logistic Regression:* Accuracy: **67.00%**, Precision: **0.577**, Recall: **0.405**, F1-Score: **0.476**, ROC-AUC: **0.646**
    - *Decision Tree:* Accuracy: 61.00%, Precision: 0.458, Recall: 0.297, F1-Score: 0.361, ROC-AUC: 0.602
    - *Random Forest:* Accuracy: 65.00%, Precision: 0.562, Recall: 0.243, F1-Score: 0.340, ROC-AUC: 0.633
  - **Champion Selection:** Logistic Regression achieved the highest balanced F1-Score and ROC-AUC.
  - Serialized champion model to `models/attrition_model.pkl` along with feature scaler.
- **Suggested Visual:** Model Performance Comparison Bar Chart (`visualizations/10_model_comparison.png`) and Confusion Matrix heatmaps.
- **Verbal Explanation Script:**  
  *"Evaluating across test metrics, Logistic Regression achieved the highest balanced F1-Score of 0.476 and accuracy of 67.0%, outperforming the more complex models on our normalized feature set. We selected Logistic Regression as the champion model and serialized it for production deployment."*

---

### Slide 17: Interactive Streamlit Dashboard (Module 7)
- **Slide Title:** Interactive Web Dashboard Demonstration
- **Bullet Points:**
  - Developed full-stack web application using Python and Streamlit (`dashboard/app.py`).
  - **Key Dashboard Features:**
    - Real-time multi-criteria sidebar filtering (Department, Role, Gender, Tenure).
    - Top executive KPI summary cards (Headcount, Attrition Rate, Avg Salary, Performance).
    - Six modular tabs covering Overview, Performance, Attrition, ML Evaluation, Risk Simulator, and HR Insights.
  - Interactive simulator allows HR managers to test any employee profile and view instantaneous risk scoring.
- **Suggested Visual:** Screenshot of the Streamlit Dashboard UI showing KPI cards and interactive charts.
- **Verbal Explanation Script:**  
  *"Module 7 provides an intuitive web interface for non-technical users. Built with Streamlit, the dashboard provides interactive filters, departmental cross-tabulations, and visual KPI cards. The live risk simulator allows an HR manager to adjust an employee's parameters and view immediate probability assessments."*

---

### Slide 18: Real-Time Prediction & Prescriptive HR Strategy (Module 8)
- **Slide Title:** Prescriptive HR Interventions & Strategy
- **Bullet Points:**
  - The inference engine translates mathematical probabilities into four operational risk tiers: Low, Moderate, High, and Critical.
  - **Actionable HR Recommendations:**
    - *Overtime Reduction:* Enforce project workload balancing and hire temporary contract support.
    - *Compensation Parity:* Review salaries against market medians for Level 1 & 2 staff.
    - *Career Mobility:* Conduct biannual promotion appraisals for employees at 3+ years tenure.
    - *Engagement:* Conduct monthly pulse surveys and manager check-ins for declining satisfaction.
- **Suggested Visual:** Decision tree diagram showing Identified Stressor $\to$ Tailored HR Retention Action.
- **Verbal Explanation Script:**  
  *"Crucially, our system does not just predict departures—it diagnoses root causes and prescribes solutions. If an employee is flagged at High Risk due to overtime and low pay, the dashboard specifically recommends workload rebalancing and compensation review, turning data into preventive action."*

---

### Slide 19: Conclusion & Academic Contributions
- **Slide Title:** Conclusion & Contributions
- **Bullet Points:**
  - Successfully demonstrated an end-to-end B.Tech Data Analytics and Machine Learning project.
  - Designed an objective composite performance scoring algorithm uniting multiple HR dimensions.
  - Statistically confirmed overtime, salary gaps, and satisfaction as the primary drivers of workforce attrition.
  - Delivered a working interactive web application with zero deployment dependencies outside standard Python libraries.
  - Validated ethical AI guidelines: treating models as probabilistic decision-support tools rather than deterministic verdicts.
- **Suggested Visual:** Summary checklist highlighting all 8 completed modules with green checkmarks.
- **Verbal Explanation Script:**  
  *"In conclusion, this project fulfills all B.Tech academic objectives. We have built an end-to-end, working software solution that handles raw data, performs deep EDA, engineers composite performance metrics, benchmarks machine learning classifiers, and serves actionable insights through a polished web dashboard."*

---

### Slide 20: Future Scope & References
- **Slide Title:** Future Scope & References
- **Bullet Points:**
  - **Future Research Directions:**
    - Integrate Natural Language Processing (NLP) for unstructured exit interview transcripts and pulse survey comments.
    - Incorporate survival analysis to estimate the expected *time-to-departure* window.
    - Real-time enterprise integration with Microsoft Teams / Slack for automated managerial check-in alerts.
  - **Key References:**
    - IBM HR Analytics Employee Attrition & Performance Dataset.
    - Pedregosa et al., *Scikit-learn: Machine Learning in Python*, JMLR, 2011.
    - McKinney, W., *Data Structures for Statistical Computing in Python (Pandas)*, 2010.
- **Suggested Visual:** 'Thank You / Q&A' closing banner with author contact and project repository path.
- **Verbal Explanation Script:**  
  *"Looking forward, this project can be expanded with NLP for sentiment analysis and survival models for time-based attrition forecasting. Thank you, respected evaluators. I am now ready to demonstrate the live code and answer your questions."*
