# XGBOOST MULTI-CLASS CLASSIFIER FOR LCMM TRAJECTORY CLASSES


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns


from sklearn.model_selection import (
    StratifiedKFold,
    train_test_split,
    RandomizedSearchCV,
)
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve,
    auc,
    balanced_accuracy_score,
    f1_score,
    ConfusionMatrixDisplay,
)
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.inspection import permutation_importance

import xgboost as xgb
import shap
import os
from scipy.stats import uniform, randint
import warnings

warnings.filterwarnings("ignore")


# 0. CONFIGURATION


DATA_PATH = "/Users/pragata/Books_&_papers/neuro_reviews/datasets/inner_merged_final.csv"  # <-- Change to your file path
PATNO_COL = "PATNO"  # <-- Patient ID column name
TARGET_COL = "class"  # <-- Target column name
RANDOM_STATE = 42
TEST_SIZE = 0.15  # 15% held-out test set
VAL_SIZE = 0.15  # 15% validation from training
N_CV_FOLDS = 3  # 3-fold cross validation
N_ITER_SEARCH = 100  # Hyperparameter search iterations
OUTPUT_DIR = "/Users/pragata/Books_&_papers/neuro_reviews/datasets/xgboost_results/"  # Output directory

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\n" + "=" * 70)
print("PHASE 4: XGBOOST CLASSIFICATION PIPELINE")
print("=" * 70)

df = pd.read_csv(DATA_PATH)

print(f"\n[1] DATA LOADED")
print(f"    Shape: {df.shape}")
print(f"    Columns: {df.shape[1]}")
print(f"    Patients: {df.shape[0]}")


df = df.drop(columns=[PATNO_COL], errors="ignore")

# Separate features and target
X_raw = df.drop(columns=[TARGET_COL])
y_raw = df[TARGET_COL]
print(y_raw.dtype)

print(f"\n[2] CLASS DISTRIBUTION")
class_counts = y_raw.value_counts().sort_index()
for cls, cnt in class_counts.items():
    print(f"    Class {cls}: {cnt} ({100 * cnt / len(y_raw):.1f}%)")

# TARGET VARIABLE

le = LabelEncoder()
y = le.fit_transform(y_raw)
class_names = [f"Class {c}" for c in le.classes_]

print(f"\n    Encoded classes: {dict(zip(le.classes_, range(len(le.classes_))))}")

# categorical variable

print(f"\n[3] HANDLING CATEGORICAL VARIABLES")

# Identify column types
cat_cols = X_raw.select_dtypes(include=["object", "category"]).columns.tolist()
num_cols = X_raw.select_dtypes(include=[np.number]).columns.tolist()

print(f"    Numeric columns:     {len(num_cols)}")
print(f"    Categorical columns: {len(cat_cols)}")
if cat_cols:
    print(f"    Categorical vars:    {cat_cols}")

X = X_raw.copy()


if cat_cols:
    oe = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
    X[cat_cols] = oe.fit_transform(X[cat_cols].astype(str))
    print(f"    Categorical variables encoded using OrdinalEncoder")
else:
    oe = None
    print(f"    No categorical variables found")

# 4. TRAIN  TEST SPLIT

print(f"\n[4] SPLITTING DATA")

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
)

val_size_adjusted = VAL_SIZE / (1 - TEST_SIZE)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval,
    y_trainval,
    test_size=val_size_adjusted,
    stratify=y_trainval,
    random_state=RANDOM_STATE,
)

print(
    f"    Training set:   {X_train.shape[0]} subjects ({100 * X_train.shape[0] / len(X):.1f}%)"
)
print(
    f"    Validation set: {X_val.shape[0]} subjects ({100 * X_val.shape[0] / len(X):.1f}%)"
)
print(
    f"    Test set:       {X_test.shape[0]} subjects ({100 * X_test.shape[0] / len(X):.1f}%)"
)

# CLASS IMBALANCE

print(f"\n[5] HANDLING CLASS IMBALANCE")
print(f"    Using sample_weight (balanced weighting)")

# Compute sample weights to handle imbalance
sample_weights_train = compute_sample_weight(class_weight="balanced", y=y_train)

# 6. HYPERPARAMETER TUNING  + CV

print(f"\n[6] HYPERPARAMETER TUNING")
print(
    f"    Strategy: RandomizedSearchCV ({N_ITER_SEARCH} iterations, {N_CV_FOLDS}-fold CV)"
)
print(f"    This may take several minutes...\n")

# Define hyperparameter search space
param_distributions = {
    "n_estimators": randint(100, 1000),
    "max_depth": randint(3, 10),
    "learning_rate": uniform(0.01, 0.3),
    "subsample": uniform(0.5, 0.5),
    "colsample_bytree": uniform(0.5, 0.5),
    "min_child_weight": randint(1, 10),
    "gamma": uniform(0, 0.5),
    "reg_alpha": uniform(0, 1),  # L1
    "reg_lambda": uniform(0.5, 2),  # L2
    "scale_pos_weight": [1],
}

# Base XGBoost model
base_model = xgb.XGBClassifier(
    objective="multi:softprob",
    num_class=len(le.classes_),
    eval_metric="mlogloss",
    use_label_encoder=False,
    tree_method="hist",
    enable_categorical=True if cat_cols else False,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    verbosity=0,
)

# Stratified K-Fold CV
skf = StratifiedKFold(n_splits=N_CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

# Randomized search
search = RandomizedSearchCV(
    estimator=base_model,
    param_distributions=param_distributions,
    n_iter=N_ITER_SEARCH,
    cv=skf,
    scoring="balanced_accuracy",
    n_jobs=-1,
    random_state=RANDOM_STATE,
    verbose=1,
    refit=True,
)

search.fit(X_train, y_train, sample_weight=sample_weights_train)

best_params = search.best_params_
best_cv_score = search.best_score_

print(f"\n    Best CV Balanced Accuracy: {best_cv_score:.4f}")
print(f"\n    Best Hyperparameters:")
for k, v in best_params.items():
    print(f"      {k}: {v}")

# best params
pd.DataFrame([best_params]).to_csv(f"{OUTPUT_DIR}best_hyperparameters.csv", index=False)

# 7. TRAIN

print(f"\n[7] TRAINING FINAL MODEL WITH EARLY STOPPING")

final_model = xgb.XGBClassifier(
    **best_params,
    objective="multi:softprob",
    num_class=len(le.classes_),
    eval_metric="mlogloss",
    use_label_encoder=False,
    tree_method="hist",
    enable_categorical=True if cat_cols else False,
    random_state=RANDOM_STATE,
    n_jobs=-1,
    early_stopping_rounds=30,
    verbosity=0,
)

# Fit with early stopping on validation set
final_model.fit(
    X_train,
    y_train,
    sample_weight=sample_weights_train,
    eval_set=[(X_val, y_val)],
    verbose=False,
)

print(f"    Optimal n_estimators (early stopping): {final_model.best_iteration}")

# 8. EVALUATION ON VALIDATION SET

print(f"\n[8] VALIDATION SET PERFORMANCE")

y_val_pred = final_model.predict(X_val)
y_val_pred_proba = final_model.predict_proba(X_val)

val_balanced_acc = balanced_accuracy_score(y_val, y_val_pred)
val_f1_macro = f1_score(y_val, y_val_pred, average="macro")
val_f1_weighted = f1_score(y_val, y_val_pred, average="weighted")

print(f"    Balanced Accuracy: {val_balanced_acc:.4f}")
print(f"    F1 Macro:          {val_f1_macro:.4f}")
print(f"    F1 Weighted:       {val_f1_weighted:.4f}")
print(f"\n    Classification Report (Validation):")
print(classification_report(y_val, y_val_pred, target_names=class_names))

# 9. FINAL EVALUATION ON TEST SET

print(f"\n[9] TEST SET PERFORMANCE (FINAL EVALUATION)")

y_test_pred = final_model.predict(X_test)
y_test_pred_proba = final_model.predict_proba(X_test)

test_balanced_acc = balanced_accuracy_score(y_test, y_test_pred)
test_f1_macro = f1_score(y_test, y_test_pred, average="macro")
test_f1_weighted = f1_score(y_test, y_test_pred, average="weighted")

# AUC-ROC
test_auc = roc_auc_score(y_test, y_test_pred_proba, multi_class="ovr", average="macro")

print(f"    Balanced Accuracy: {test_balanced_acc:.4f}")
print(f"    F1 Macro:          {test_f1_macro:.4f}")
print(f"    F1 Weighted:       {test_f1_weighted:.4f}")
print(f"    AUC-ROC (macro):   {test_auc:.4f}")
print(f"\n    Classification Report (Test):")
print(classification_report(y_test, y_test_pred, target_names=class_names))

# Save metrics
metrics_dict = {
    "balanced_accuracy": test_balanced_acc,
    "f1_macro": test_f1_macro,
    "f1_weighted": test_f1_weighted,
    "auc_roc_macro": test_auc,
    "best_cv_score": best_cv_score,
    "best_n_estimators": final_model.best_iteration,
}
pd.DataFrame([metrics_dict]).to_csv(f"{OUTPUT_DIR}test_metrics.csv", index=False)

#  RESULTS SUMMARY

print(f"\n[10] 3-FOLD CROSS-VALIDATION SUMMARY")

cv_results = pd.DataFrame(search.cv_results_)
cv_best = cv_results.sort_values("mean_test_score", ascending=False).head(10)

print(f"\n    Top 10 configurations by CV balanced accuracy:")
print(
    cv_best[["mean_test_score", "std_test_score", "rank_test_score"]]
    .rename(
        columns={
            "mean_test_score": "mean_balanced_acc",
            "std_test_score": "std_balanced_acc",
            "rank_test_score": "rank",
        }
    )
    .to_string(index=False)
)

cv_results.to_csv(f"{OUTPUT_DIR}cv_results_full.csv", index=False)

# 11. PLOTS

print(f"\n[11] GENERATING PLOTS")
plt.style.use("seaborn-v0_8-whitegrid")
colors = ["#4575b4", "#d73027", "#fdae61"]

# CONFUSION MATRIX ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, (y_true, y_pred, title) in zip(
    axes, [(y_val, y_val_pred, "Validation Set"), (y_test, y_test_pred, "Test Set")]
):
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"Confusion Matrix – {title}", fontsize=13, fontweight="bold")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}confusion_matrix.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: confusion_matrix.png")

#  ROC CURVES (One-vs-Rest) ----
fig, ax = plt.subplots(figsize=(8, 6))

for i, cls_name in enumerate(class_names):
    y_bin = (y_test == i).astype(int)
    fpr, tpr, _ = roc_curve(y_bin, y_test_pred_proba[:, i])
    roc_auc = auc(fpr, tpr)
    ax.plot(
        fpr,
        tpr,
        label=f"{cls_name} (AUC = {roc_auc:.3f})",
        color=colors[i],
        linewidth=2,
    )

ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Chance")
ax.set_xlabel("False Positive Rate", fontsize=12)
ax.set_ylabel("True Positive Rate", fontsize=12)
ax.set_title("ROC Curves – One vs Rest (Test Set)", fontsize=13, fontweight="bold")
ax.legend(loc="lower right", fontsize=10)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}roc_curves.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: roc_curves.png")

# CLASS PROBABILITY DISTRIBUTIONS ----
fig, axes = plt.subplots(1, len(class_names), figsize=(15, 5))
for i, (ax, cls_name) in enumerate(zip(axes, class_names)):
    for j, color in zip(range(len(class_names)), colors):
        mask = y_test == j
        ax.hist(
            y_test_pred_proba[mask, i],
            bins=20,
            alpha=0.6,
            label=f"True {class_names[j]}",
            color=colors[j],
            density=True,
        )
    ax.set_title(f"P({cls_name}) by True Class", fontsize=11, fontweight="bold")
    ax.set_xlabel("Predicted Probability", fontsize=10)
    ax.set_ylabel("Density", fontsize=10)
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}probability_distributions.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: probability_distributions.png")

#  XGBOOST NATIVE FEATURE IMPORTANCE
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

importance_types = ["weight", "gain", "cover"]
importance_labels = ["Frequency (weight)", "Information Gain", "Cover"]

for ax, imp_type, imp_label in zip(axes, importance_types, importance_labels):
    importances = final_model.get_booster().get_score(importance_type=imp_type)
    if not importances:
        continue
    imp_df = pd.DataFrame(list(importances.items()), columns=["feature", "importance"])
    imp_df = imp_df.sort_values("importance", ascending=False).head(20)

    ax.barh(imp_df["feature"], imp_df["importance"], color="#4575b4", alpha=0.8)
    ax.set_title(f"Feature Importance\n({imp_label})", fontsize=11, fontweight="bold")
    ax.set_xlabel(imp_label, fontsize=10)
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}feature_importance_native.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: feature_importance_native.png")

# SHAP VALUES ----
print(f"\n[12] COMPUTING SHAP VALUES")

explainer = shap.TreeExplainer(final_model)
shap_values = explainer.shap_values(X_test)  # Shape: (n_samples, n_features, n_classes)

# SHAP Summary Plot (per class)
for i, cls_name in enumerate(class_names):
    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(
        shap_values[:, :, i] if shap_values.ndim == 3 else shap_values[i],
        X_test,
        plot_type="bar",
        show=False,
        max_display=20,
    )
    plt.title(f"SHAP Feature Importance – {cls_name}", fontsize=13, fontweight="bold")
    plt.tight_layout()
    plt.savefig(
        f"{OUTPUT_DIR}shap_bar_{cls_name.replace(' ', '_')}.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close()
    print(f"    Saved: shap_bar_{cls_name.replace(' ', '_')}.png")

# SHAP Beeswarm
fig, ax = plt.subplots(figsize=(10, 10))
shap.summary_plot(
    shap_values[:, :, 0] if shap_values.ndim == 3 else shap_values[0],
    X_test,
    show=False,
    max_display=20,
)
plt.title(f"SHAP Beeswarm – {class_names[0]}", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}shap_beeswarm_class0.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: shap_beeswarm_class0.png")

#  CV SCORE DISTRIBUTION ----
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(
    cv_results["mean_test_score"],
    bins=30,
    color="#4575b4",
    alpha=0.8,
    edgecolor="white",
)
ax.axvline(
    best_cv_score,
    color="#d73027",
    linewidth=2,
    linestyle="--",
    label=f"Best: {best_cv_score:.4f}",
)
ax.set_xlabel("Mean Balanced Accuracy (CV)", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title(
    "Hyperparameter Search: CV Score Distribution", fontsize=13, fontweight="bold"
)
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}cv_score_distribution.png", dpi=300, bbox_inches="tight")
plt.close()
print(f"    Saved: cv_score_distribution.png")

# ---- PLOT 7: LEARNING CURVE (train vs val loss) ----
results = final_model.evals_result()
if results:
    fig, ax = plt.subplots(figsize=(8, 5))
    val_loss = results.get("validation_0", {}).get("mlogloss", [])
    if val_loss:
        ax.plot(val_loss, color="#4575b4", linewidth=2, label="Validation loss")
        ax.axvline(
            final_model.best_iteration,
            color="#d73027",
            linestyle="--",
            label=f"Best iteration: {final_model.best_iteration}",
        )
        ax.set_xlabel("Iteration", fontsize=12)
        ax.set_ylabel("Log Loss", fontsize=12)
        ax.set_title(
            "Early Stopping: Validation Loss Curve", fontsize=13, fontweight="bold"
        )
        ax.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}learning_curve.png", dpi=300, bbox_inches="tight")
        plt.close()
        print(f"    Saved: learning_curve.png")

# 12. SAVE PREDICTIONS

print(f"\n[13] SAVING PREDICTIONS")

test_predictions = pd.DataFrame(
    {
        "true_class": le.inverse_transform(y_test),
        "predicted_class": le.inverse_transform(y_test_pred),
        **{f"prob_{cls}": y_test_pred_proba[:, i] for i, cls in enumerate(le.classes_)},
    }
)

test_predictions.to_csv(f"{OUTPUT_DIR}test_predictions.csv", index=False)
print(f"    Saved: test_predictions.csv")

# 13. FINAL SUMMARY

print(f"\n{'=' * 70}")
print(f"FINAL RESULTS SUMMARY")
print(f"{'=' * 70}")
print(f"  Dataset:              {len(df)} subjects, {X.shape[1]} features")
print(f"  Classes:              {', '.join(class_names)}")
print(f"  Class distribution:   {dict(zip(class_names, class_counts.values))}")
print(f"\n  --- Cross-Validation ---")
print(f"  Best CV Balanced Acc: {best_cv_score:.4f}")
print(f"\n  --- Validation Set ---")
print(f"  Balanced Accuracy:    {val_balanced_acc:.4f}")
print(f"  F1 Macro:             {val_f1_macro:.4f}")
print(f"\n  --- Test Set ---")
print(f"  Balanced Accuracy:    {test_balanced_acc:.4f}")
print(f"  F1 Macro:             {test_f1_macro:.4f}")
print(f"  F1 Weighted:          {test_f1_weighted:.4f}")
print(f"  AUC-ROC (macro):      {test_auc:.4f}")
print(f"\n  All outputs saved to: {OUTPUT_DIR}")
print(f"{'=' * 70}\n")
