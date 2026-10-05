"""
Module 6: Attrition Prediction / Machine Learning Pipeline
Project: Employee Performance and Attrition Analytics Using Data Analytics

This module implements and evaluates three industry-standard classification models:
1. Logistic Regression (Probabilistic linear baseline)
2. Decision Tree Classifier (Rule-based interpretable tree)
3. Random Forest Classifier (Ensemble bagging of decision trees)

Key Operations:
- Training and hyperparameter configuration
- Comprehensive metric benchmarking (Accuracy, Precision, Recall, F1, ROC-AUC)
- Confusion Matrix computation
- Feature Importance extraction
- Model comparison chart & feature importance chart generation
- Serialization of the champion model to models/attrition_model.pkl
"""

import os
import json
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

import sys
# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data_preprocessing import prepare_train_test_data

def train_and_evaluate_models(X_train, X_test, y_train, y_test, feature_names):
    """
    Trains Logistic Regression, Decision Tree, and Random Forest.
    Evaluates each model across standard classification metrics.
    
    Returns:
    - dict: Evaluation metrics, trained models, confusion matrices, and best model name.
    """
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, min_samples_split=8, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=120, max_depth=6, random_state=42)
    }
    
    results = {}
    
    for name, clf in models.items():
        # 1. Fit classifier
        clf.fit(X_train, y_train)
        
        # 2. Predict classes and probabilities
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred
        
        # 3. Calculate evaluation metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc = roc_auc_score(y_test, y_prob)
        cm = confusion_matrix(y_test, y_pred)
        
        results[name] = {
            "model": clf,
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "roc_auc": round(float(auc), 4),
            "confusion_matrix": cm.tolist(),
            "predictions": y_pred,
            "probabilities": y_prob
        }
        
    return results

def save_model_comparison_plots(results, feature_names, best_model_name, output_dir):
    """
    Creates and saves:
    1. Model evaluation metric comparison bar chart
    2. Confusion matrix heatmaps for all models
    3. Feature importance plot from the Random Forest model
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Metric Comparison Bar Chart
    metrics_data = []
    for name, r in results.items():
        metrics_data.append({
            "Model": name,
            "Accuracy": r["accuracy"],
            "Precision": r["precision"],
            "Recall": r["recall"],
            "F1-Score": r["f1_score"],
            "ROC-AUC": r["roc_auc"]
        })
    df_metrics = pd.DataFrame(metrics_data)
    df_melted = df_metrics.melt(id_vars="Model", var_name="Metric", value_name="Score")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_melted, x="Metric", y="Score", hue="Model", palette="deep", ax=ax)
    ax.set_ylim(0, 1.1)
    ax.set_title("Machine Learning Model Performance Comparison", fontsize=14, weight="bold", pad=12)
    ax.set_ylabel("Score (0.0 to 1.0)")
    for p in ax.patches:
        height = p.get_height()
        if height > 0.05:
            ax.annotate(f"{height:.2f}",
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom',
                        fontsize=8, color='black',
                        xytext=(0, 2),
                        textcoords='offset points')
    plt.tight_layout()
    comp_path = os.path.join(output_dir, "10_model_comparison.png")
    fig.savefig(comp_path, dpi=300)
    plt.close(fig)
    print(f" [Plot Saved] {comp_path}")
    
    # 2. Confusion Matrices Subplot
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for idx, (name, r) in enumerate(results.items()):
        cm = np.array(r["confusion_matrix"])
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[idx],
            xticklabels=["Stayed (0)", "Left (1)"],
            yticklabels=["Stayed (0)", "Left (1)"]
        )
        axes[idx].set_title(f"{name}\nAcc: {r['accuracy']*100:.1f}%, F1: {r['f1_score']:.2f}", fontsize=11, weight="bold")
        axes[idx].set_xlabel("Predicted Label")
        axes[idx].set_ylabel("Actual Ground Truth")
    plt.tight_layout()
    cm_path = os.path.join(output_dir, "11_confusion_matrices.png")
    fig.savefig(cm_path, dpi=300)
    plt.close(fig)
    print(f" [Plot Saved] {cm_path}")
    
    # 3. Feature Importance Plot (using Random Forest)
    rf_model = results["Random Forest"]["model"]
    importances = rf_model.feature_importances_
    fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    fi_df = fi_df.sort_values(by="Importance", ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=fi_df, x="Importance", y="Feature", palette="viridis", ax=ax, hue="Feature", legend=False)
    ax.set_title("Top 10 Most Predictive Features for Attrition Risk", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Relative Feature Importance Score")
    plt.tight_layout()
    fi_path = os.path.join(output_dir, "12_feature_importance.png")
    fig.savefig(fi_path, dpi=300)
    plt.close(fig)
    print(f" [Plot Saved] {fi_path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(base_dir, "dataset", "employee_data.csv")
    models_dir = os.path.join(base_dir, "models")
    vis_dir = os.path.join(base_dir, "visualizations")
    
    print("=" * 65)
    print("      MODULE 6: ATTRITION PREDICTION & MODEL TRAINING         ")
    print("=" * 65)
    
    # 1. Preprocess & Scale Data
    X_train, X_test, y_train, y_test, feature_names, scaler, _ = prepare_train_test_data(
        dataset_path, models_dir=models_dir
    )
    
    # 2. Train & Evaluate Models
    results = train_and_evaluate_models(X_train, X_test, y_train, y_test, feature_names)
    
    # 3. Compare Models and Select Champion (based on F1-Score)
    print("\n--- MODEL PERFORMANCE BENCHMARK RESULTS ---")
    summary_table = []
    best_name = None
    highest_f1 = -1.0
    
    for name, r in results.items():
        summary_table.append({
            "Model": name,
            "Accuracy": f"{r['accuracy']*100:.2f}%",
            "Precision": f"{r['precision']:.3f}",
            "Recall": f"{r['recall']:.3f}",
            "F1-Score": f"{r['f1_score']:.3f}",
            "ROC-AUC": f"{r['roc_auc']:.3f}"
        })
        if r["f1_score"] > highest_f1:
            highest_f1 = r["f1_score"]
            best_name = name
            
    print(pd.DataFrame(summary_table).to_string(index=False))
    print(f"\n[Champion Model Selected] >>> {best_name} <<< (Highest F1-Score: {highest_f1:.3f})")
    
    # 4. Save Champion Model & Preprocessing Meta
    best_model = results[best_name]["model"]
    model_save_path = os.path.join(models_dir, "attrition_model.pkl")
    joblib.dump(best_model, model_save_path)
    print(f"[Model Saved] Champion model saved to: {model_save_path}")
    
    # Save benchmark metadata to JSON
    metadata = {
        "best_model": best_name,
        "metrics": {
            k: {m: v for m, v in val.items() if m not in ["model", "predictions", "probabilities"]}
            for k, val in results.items()
        },
        "feature_count": len(feature_names),
        "disclaimer": "This model calculates statistical attrition risk probability based on historical training patterns. It is an analytical decision-support tool, not an absolute guarantee of individual future actions."
    }
    
    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=4)
        
    # 5. Generate and Save Visual Comparison Charts
    save_model_comparison_plots(results, feature_names, best_name, vis_dir)
    
    print("\n[Status] Module 6 Machine Learning training and evaluation finished successfully.")
    print("=" * 65)

if __name__ == "__main__":
    main()
