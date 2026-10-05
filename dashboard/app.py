"""
Module 7: Interactive HR Analytics & Attrition Prediction Dashboard
Project: Employee Performance and Attrition Analytics Using Data Analytics

Streamlit Web Application designed for B.Tech CSE Academic Project Demonstration.
Includes:
- Interactive Multi-Criteria Sidebar Filters
- Executive KPI Overview Cards
- Performance Analytics Deep-Dive
- Attrition Diagnostics & Behavioral Stressors
- Machine Learning Model Benchmark Comparisons
- Live Interactive Employee Attrition Risk Simulator
- Strategic HR Recommendations & Academic Conclusion
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure project root is in sys.path
_current_dir = os.path.dirname(os.path.abspath(__file__))
if os.path.exists(os.path.join(_current_dir, "dataset")):
    PROJECT_ROOT = _current_dir
elif os.path.exists(os.path.join(os.path.dirname(_current_dir), "dataset")):
    PROJECT_ROOT = os.path.dirname(_current_dir)
else:
    PROJECT_ROOT = os.getcwd()

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.performance_analysis import calculate_composite_performance_score
from src.prediction import AttritionPredictor

# Page Setup
st.set_page_config(
    page_title="Employee Performance & Attrition Analytics",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        border-left: 4px solid #1f77b4;
        margin-bottom: 12px;
    }
    .metric-title {
        color: #6c757d;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        color: #212529;
        font-size: 1.6rem;
        font-weight: 700;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dataset():
    data_path = os.path.join(PROJECT_ROOT, "dataset", "employee_data.csv")
    if not os.path.exists(data_path):
        from dataset.generate_dataset import generate_employee_dataset
        df = generate_employee_dataset(500)
        df.to_csv(data_path, index=False)
    else:
        df = pd.read_csv(data_path)
    return calculate_composite_performance_score(df)

@st.cache_resource
def get_predictor():
    return AttritionPredictor(os.path.join(PROJECT_ROOT, "models"))

df = load_dataset()

# ==========================================
# SIDEBAR FILTERS
# ==========================================
st.sidebar.image("https://img.icons8.com/color/96/business-group.png", width=70)
st.sidebar.title("HR Analytics Controls")
st.sidebar.markdown("**B.Tech CSE Capstone Project**")

# Department Filter
departments = ["All"] + sorted(list(df["Department"].unique()))
selected_dept = st.sidebar.selectbox("Filter Department:", departments)

# Role Filter
if selected_dept != "All":
    available_roles = ["All"] + sorted(list(df[df["Department"] == selected_dept]["JobRole"].unique()))
else:
    available_roles = ["All"] + sorted(list(df["JobRole"].unique()))
selected_role = st.sidebar.selectbox("Filter Job Role:", available_roles)

# Gender Filter
gender_filter = st.sidebar.radio("Gender:", ["All", "Male", "Female"], horizontal=True)

# OverTime Filter
overtime_filter = st.sidebar.radio("Overtime Requirement:", ["All", "Yes", "No"], horizontal=True)

# Tenure Slider
min_tenure, max_tenure = int(df["YearsAtCompany"].min()), int(df["YearsAtCompany"].max())
tenure_range = st.sidebar.slider("Years at Company:", min_tenure, max_tenure, (min_tenure, max_tenure))

# Filter Application
filtered_df = df.copy()
if selected_dept != "All":
    filtered_df = filtered_df[filtered_df["Department"] == selected_dept]
if selected_role != "All":
    filtered_df = filtered_df[filtered_df["JobRole"] == selected_role]
if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]
if overtime_filter != "All":
    filtered_df = filtered_df[filtered_df["OverTime"] == overtime_filter]
filtered_df = filtered_df[
    (filtered_df["YearsAtCompany"] >= tenure_range[0]) & 
    (filtered_df["YearsAtCompany"] <= tenure_range[1])
]

# Sidebar Metadata
st.sidebar.markdown("---")
st.sidebar.info(f"Showing **{len(filtered_df)}** of **{len(df)}** employees.")

# ==========================================
# MAIN DASHBOARD HEADER
# ==========================================
st.title("📊 Employee Performance & Attrition Analytics")
st.markdown("An end-to-end Data Analytics & Machine Learning system to diagnose organizational health, assess workforce performance, and predict employee attrition risk.")

# ==========================================
# TOP KPI METRICS BAR
# ==========================================
total_emp = len(filtered_df)
attr_count = (filtered_df["Attrition"] == "Yes").sum() if total_emp > 0 else 0
attr_rate = (attr_count / total_emp * 100) if total_emp > 0 else 0.0
avg_perf = filtered_df["PerformanceRating"].mean() if total_emp > 0 else 0.0
avg_score = filtered_df["CompositePerformanceScore"].mean() if total_emp > 0 else 0.0
avg_salary = filtered_df["MonthlyIncome"].mean() if total_emp > 0 else 0.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"""<div class='metric-card'><div class='metric-title'>Workforce Headcount</div><div class='metric-value'>{total_emp:,}</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #d9534f;'><div class='metric-title'>Attrition Count</div><div class='metric-value'>{attr_count}</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #f0ad4e;'><div class='metric-title'>Attrition Rate</div><div class='metric-value'>{attr_rate:.1f}%</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #5cb85c;'><div class='metric-title'>Avg Performance</div><div class='metric-value'>{avg_perf:.2f}/4.0</div></div>""", unsafe_allow_html=True)
with col5:
    st.markdown(f"""<div class='metric-card' style='border-left-color: #6f42c1;'><div class='metric-title'>Avg Monthly Pay</div><div class='metric-value'>${avg_salary:,.0f}</div></div>""", unsafe_allow_html=True)

# ==========================================
# TABBED INTERFACE
# ==========================================
tab_overview, tab_perf, tab_attr, tab_ml, tab_predict, tab_insights = st.tabs([
    "📈 Executive Overview",
    "⭐ Performance Analytics",
    "🚪 Attrition Diagnostics",
    "🤖 Machine Learning Evaluation",
    "🔮 Live Attrition Risk Predictor",
    "💡 Strategic HR Insights"
])

# ------------------------------------------
# TAB 1: EXECUTIVE OVERVIEW
# ------------------------------------------
with tab_overview:
    st.subheader("Demographic & Structural Workforce Distribution")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Headcount by Department**")
        dept_counts = filtered_df["Department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Count"]
        st.bar_chart(dept_counts.set_index("Department"), color="#1f77b4")
        
    with c2:
        st.markdown("**Monthly Salary Distribution by Job Level**")
        fig, ax = plt.subplots(figsize=(6, 3.8))
        sns.boxplot(data=filtered_df, x="JobLevel", y="MonthlyIncome", palette="Blues", ax=ax)
        ax.set_title("Salary Range across Job Levels", fontsize=11, weight="bold")
        ax.set_xlabel("Job Level (1 = Entry -> 5 = Executive)")
        ax.set_ylabel("Monthly Income ($)")
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Gender Diversity Representation**")
        gender_data = filtered_df["Gender"].value_counts()
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(gender_data, labels=gender_data.index, autopct="%1.1f%%", colors=["#4a90e2", "#e26a6a"], startangle=90)
        st.pyplot(fig)
        plt.close(fig)
        
    with c4:
        st.markdown("**Work-Life Balance vs Job Satisfaction Matrix**")
        cross = pd.crosstab(filtered_df["WorkLifeBalance"], filtered_df["JobSatisfaction"])
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.heatmap(cross, annot=True, fmt="d", cmap="YlGnBu", cbar=False, ax=ax)
        ax.set_xlabel("Job Satisfaction (1-4)")
        ax.set_ylabel("Work Life Balance (1-4)")
        st.pyplot(fig)
        plt.close(fig)

# ------------------------------------------
# TAB 2: PERFORMANCE ANALYTICS
# ------------------------------------------
with tab_perf:
    st.subheader("Employee Performance Rating & Composite Scoring")
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.markdown("**Workforce Breakdown by Performance Tier**")
        tier_counts = filtered_df["PerformanceCategory"].value_counts().reset_index()
        tier_counts.columns = ["Category", "Count"]
        st.dataframe(tier_counts, use_container_width=True, hide_index=True)
        
        fig, ax = plt.subplots(figsize=(6, 3.2))
        sns.barplot(data=tier_counts, x="Count", y="Category", palette="mako", ax=ax)
        ax.set_title("Employees per Performance Category", fontsize=11, weight="bold")
        st.pyplot(fig)
        plt.close(fig)
        
    with p_col2:
        st.markdown("**Composite Performance Score vs Monthly Salary**")
        fig, ax = plt.subplots(figsize=(6, 3.8))
        sns.scatterplot(
            data=filtered_df, 
            x="MonthlyIncome", 
            y="CompositePerformanceScore", 
            hue="PerformanceRating", 
            palette="viridis", 
            alpha=0.8,
            ax=ax
        )
        ax.set_title("Performance Score vs Salary", fontsize=11, weight="bold")
        ax.set_xlabel("Monthly Salary ($)")
        ax.set_ylabel("Composite Score (0-100)")
        st.pyplot(fig)
        plt.close(fig)
        
    st.markdown("---")
    st.markdown("### Top Benchmark Performers")
    top_cols = ["EmployeeID", "Department", "JobRole", "PerformanceRating", "CompositePerformanceScore", "TrainingTimesLastYear", "Absenteeism"]
    top_df = filtered_df.sort_values(by="CompositePerformanceScore", ascending=False)[top_cols].head(8)
    st.dataframe(top_df, use_container_width=True, hide_index=True)

# ------------------------------------------
# TAB 3: ATTRITION DIAGNOSTICS
# ------------------------------------------
with tab_attr:
    st.subheader("Organizational Attrition Drivers & Root Cause Analysis")
    a_col1, a_col2 = st.columns(2)
    
    with a_col1:
        st.markdown("**Departmental Attrition Comparison**")
        dept_attr = filtered_df.groupby("Department").agg(
            Headcount=("EmployeeID", "count"),
            Departed=("Attrition", lambda x: (x == "Yes").sum())
        ).reset_index()
        dept_attr["AttritionRate%"] = (dept_attr["Departed"] / dept_attr["Headcount"] * 100).round(1)
        st.dataframe(dept_attr, use_container_width=True, hide_index=True)
        
        fig, ax = plt.subplots(figsize=(6, 3.2))
        sns.barplot(data=dept_attr, x="Department", y="AttritionRate%", palette="Reds_r", ax=ax)
        ax.set_title("Attrition Rate by Department (%)", fontsize=11, weight="bold")
        ax.set_ylabel("Attrition Rate (%)")
        st.pyplot(fig)
        plt.close(fig)
        
    with a_col2:
        st.markdown("**The Critical Role of OverTime Demands**")
        fig, ax = plt.subplots(figsize=(6, 3.8))
        ot_data = pd.crosstab(filtered_df["OverTime"], filtered_df["Attrition"], normalize="index") * 100
        ot_data.plot(kind="bar", stacked=True, color=["#27ae60", "#c0392b"], ax=ax, width=0.45)
        ax.set_title("Attrition % by Overtime Status", fontsize=11, weight="bold")
        ax.set_ylabel("Proportion (%)")
        ax.set_xlabel("Mandatory Overtime")
        ax.legend(title="Attrition", labels=["Retained", "Departed"])
        plt.xticks(rotation=0)
        st.pyplot(fig)
        plt.close(fig)

    st.markdown("---")
    a_col3, a_col4 = st.columns(2)
    with a_col3:
        st.markdown("**Job Satisfaction vs Attrition Frequency**")
        sat_attr = pd.crosstab(filtered_df["JobSatisfaction"], filtered_df["Attrition"])
        st.dataframe(sat_attr, use_container_width=True)
    with a_col4:
        st.markdown("**Career Stagnation (Years Since Last Promotion)**")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.histplot(data=filtered_df, x="YearsSinceLastPromotion", hue="Attrition", multiple="stack", palette=["#27ae60", "#c0392b"], ax=ax, bins=10)
        ax.set_title("Promotion Stagnation vs Departures", fontsize=11, weight="bold")
        st.pyplot(fig)
        plt.close(fig)

# ------------------------------------------
# TAB 4: MACHINE LEARNING EVALUATION
# ------------------------------------------
with tab_ml:
    st.subheader("Machine Learning Algorithm Comparison & Feature Importance")
    st.markdown("""
    Three distinct classification algorithms were implemented and trained using an 80/20 stratified split:
    1. **Logistic Regression:** Linear baseline estimating log-odds probabilities.
    2. **Decision Tree:** Non-linear rule-based hierarchical tree.
    3. **Random Forest:** Ensemble bagging technique combining diverse decision trees to reduce variance.
    """)
    
    meta_path = os.path.join(PROJECT_ROOT, "models", "model_metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            
        m_list = []
        for model_name, metrics in metadata["metrics"].items():
            m_list.append({
                "Model Algorithm": model_name,
                "Accuracy": f"{metrics['accuracy']*100:.1f}%",
                "Precision": f"{metrics['precision']:.3f}",
                "Recall": f"{metrics['recall']:.3f}",
                "F1-Score": f"{metrics['f1_score']:.3f}",
                "ROC-AUC": f"{metrics['roc_auc']:.3f}"
            })
        st.table(pd.DataFrame(m_list))
        st.success(f"🏆 Champion Model: **{metadata['best_model']}** (Selected based on balanced F1-Score for imbalanced attrition prediction).")
        st.caption(f"Note: {metadata['disclaimer']}")
    else:
        st.warning("Model metadata file not found. Run src/model_training.py to train models.")

    st.markdown("---")
    st.subheader("Top Predictive Features for Attrition (Random Forest)")
    fi_img_path = os.path.join(PROJECT_ROOT, "visualizations", "12_feature_importance.png")
    cm_img_path = os.path.join(PROJECT_ROOT, "visualizations", "11_confusion_matrices.png")
    
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        if os.path.exists(fi_img_path):
            st.image(fi_img_path, caption="Feature Importance Ranking", use_container_width=True)
    with col_img2:
        if os.path.exists(cm_img_path):
            st.image(cm_img_path, caption="Confusion Matrices across All 3 Models", use_container_width=True)

# ------------------------------------------
# TAB 5: LIVE RISK PREDICTOR
# ------------------------------------------
with tab_predict:
    st.subheader("🔮 Individual Employee Attrition Risk Simulator")
    st.markdown("Enter employee demographic and workplace feedback metrics below to compute real-time attrition risk probability and prescriptive HR retention actions.")
    
    with st.form("risk_prediction_form"):
        r_col1, r_col2, r_col3 = st.columns(3)
        
        with r_col1:
            st.markdown("**Demographics & Organizational Role**")
            in_age = st.slider("Employee Age:", 20, 65, 29)
            in_gender = st.selectbox("Gender:", ["Male", "Female"])
            in_dept = st.selectbox("Department:", ["Research & Development", "Sales", "Human Resources"])
            in_role = st.selectbox("Job Role:", [
                "Software Engineer", "Research Scientist", "Sales Executive",
                "Sales Representative", "Laboratory Technician", "Manufacturing Director",
                "HR Executive", "Manager"
            ])
            in_edu = st.selectbox("Education Level:", ["High School", "Bachelor", "Master", "Doctorate"], index=1)
            in_level = st.selectbox("Job Level:", [1, 2, 3, 4, 5], index=0)
            
        with r_col2:
            st.markdown("**Tenure & Compensation**")
            in_salary = st.number_input("Monthly Income ($):", min_value=1500, max_value=25000, value=3500, step=250)
            in_tenure = st.slider("Years at Company:", 0, 30, 3)
            in_role_yrs = st.slider("Years in Current Role:", 0, 20, 2)
            in_promo_yrs = st.slider("Years Since Last Promotion:", 0, 15, 3)
            in_overtime = st.radio("Mandatory Overtime:", ["Yes", "No"], index=0, horizontal=True)
            
        with r_col3:
            st.markdown("**Engagement & Behavior**")
            in_job_sat = st.select_slider("Job Satisfaction Rating:", options=[1, 2, 3, 4], value=1, format_func=lambda x: {1: "1-Low", 2: "2-Med", 3: "3-High", 4: "4-Very High"}[x])
            in_env_sat = st.select_slider("Environment Satisfaction:", options=[1, 2, 3, 4], value=2, format_func=lambda x: {1: "1-Low", 2: "2-Med", 3: "3-High", 4: "4-Very High"}[x])
            in_wlb = st.select_slider("Work-Life Balance:", options=[1, 2, 3, 4], value=1, format_func=lambda x: {1: "1-Bad", 2: "2-Fair", 3: "3-Good", 4: "4-Best"}[x])
            in_perf = st.select_slider("Performance Rating:", options=[1, 2, 3, 4], value=2, format_func=lambda x: {1: "1-Needs Imp.", 2: "2-Good", 3: "3-Excellent", 4: "4-Outstanding"}[x])
            in_training = st.slider("Training Sessions Attended Last Year:", 0, 6, 1)
            in_absent = st.slider("Absenteeism (Days Last Year):", 0, 30, 12)
            
        submit_btn = st.form_submit_button("🚀 Compute Attrition Risk Assessment")
        
    if submit_btn:
        predictor = get_predictor()
        input_profile = {
            "Age": in_age,
            "Gender": in_gender,
            "Department": in_dept,
            "JobRole": in_role,
            "Education": in_edu,
            "JobLevel": in_level,
            "MonthlyIncome": in_salary,
            "YearsAtCompany": in_tenure,
            "YearsInCurrentRole": in_role_yrs,
            "YearsSinceLastPromotion": in_promo_yrs,
            "JobSatisfaction": in_job_sat,
            "EnvironmentSatisfaction": in_env_sat,
            "WorkLifeBalance": in_wlb,
            "PerformanceRating": in_perf,
            "OverTime": in_overtime,
            "TrainingTimesLastYear": in_training,
            "Absenteeism": in_absent
        }
        
        assessment = predictor.predict_risk(input_profile)
        
        st.markdown("### Risk Diagnostic Results")
        prob = assessment["attrition_probability"]
        tier = assessment["risk_tier"]
        
        color_code = "#28a745" if tier == "Low Risk" else ("#ffc107" if tier == "Moderate Risk" else "#dc3545")
        
        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            st.markdown(f"""
            <div style="background-color: {color_code}; color: white; padding: 24px; border-radius: 10px; text-align: center;">
                <div style="font-size: 1.1rem; font-weight: 600;">ESTIMATED RISK TIER</div>
                <div style="font-size: 2.2rem; font-weight: 800; margin: 8px 0;">{tier.upper()}</div>
                <div style="font-size: 1.4rem; font-weight: 700;">{prob}% Probability</div>
            </div>
            """, unsafe_allow_html=True)
            
        with res_col2:
            st.markdown(f"**Diagnostic Status:** {assessment['retention_status']}")
            st.markdown("**Identified Stressors:**")
            for stressor in assessment["detected_risks"]:
                st.markdown(f"- ⚠️ {stressor}")
                
            st.markdown("**Actionable HR Interventions:**")
            for rec in assessment["recommendations"]:
                st.markdown(f"- ✅ **{rec}**")
                
        st.caption(f"Academic Disclaimer: {assessment['disclaimer']}")

# ------------------------------------------
# TAB 6: STRATEGIC HR INSIGHTS
# ------------------------------------------
with tab_insights:
    st.subheader("💡 Key Strategic Findings & Recommendations for HR Leadership")
    
    st.markdown("""
    ### 1. Key Analytical Findings
    - **Overtime is the #1 Predictor of Attrition:** Staff regularly working overtime exhibit nearly double the departure probability of their peers.
    - **Salary Parity Gaps Trigger Early Departures:** Employees in entry-level job levels whose compensation lags behind peer medians have higher voluntary turnover.
    - **Promotion Stagnation:** Employees remaining 4 or more years without role advancement or title adjustments demonstrate elevated attrition risk.
    - **Satisfaction & Work-Life Balance are Early Indicators:** Low job satisfaction consistently precedes elevated absenteeism and subsequent departure.
    
    ### 2. Actionable HR Strategies
    | Strategic Pillar | Tactical Action | Expected Impact |
    | :--- | :--- | :--- |
    | **Workload Balancing** | Audit teams logging >15% overtime; enforce rest cycles and hire temporary staff during peak release cycles. | 25-35% reduction in burnout attrition. |
    | **Compensation Benchmarking** | Conduct quarterly market salary band reviews, particularly for entry and mid-level roles. | Prevents loss of trained talent to external competitors. |
    | **Transparent Career Progression** | Implement formal biannual promotion and lateral mobility assessments for employees at 3+ years tenure. | Eliminates promotion stagnation departures. |
    | **Proactive Pulse Surveys** | Conduct monthly anonymous employee satisfaction surveys to catch dipping sentiment early. | Enables timely 1-on-1 manager interventions. |

    ### 3. Academic Conclusion & Future Scope
    - **Conclusion:** This project successfully unifies workforce descriptive statistics, multivariate exploratory data analysis, and supervised machine learning to deliver a transparent, data-driven HR decision-support pipeline.
    - **Future Scope:** Expanding the model to ingest time-series sentiment from Slack/Teams communications, NLP analysis of exit interviews, and deep learning architectures for enterprise scale.
    """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Employee Performance & Attrition Analytics System | B.Tech CSE Final Year Capstone Project</p>", unsafe_allow_html=True)
