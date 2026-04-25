---
title: Parallels between RBDSQ Progression and Brain Morphology in Longitudinal Subtyping of PPMI Cohort
abstract: |
    This is a 100-150 word summary of our research, including the main objective, methods, key results, and conclusions. The abstract should provide readers with a clear overview of what the micropublication contains and its significance. Include the research question or hypothesis, the methodology employed, the key findings, and the main conclusions or implications of the work. This summary helps readers quickly assess whether the full content is relevant to their interests.
acknowledgments: |
    This work was supported by the Impact Scholars Program. We acknowledge the contributions of [former team members, teaching assistants, or mentors whose involvement does not meet the criteria of any authorship role].
---

# Introduction

We employed XGBoost, a gradient boosting framework optimised for tabular data to predict the latent classes(found by lcmm) from baseline features only, with the of developing a lightweight model for real world resource constrained clinical application. It would enable clinicians to predict the subtype of Parkinson's patient in the first visit, only from baseline data to adjust dosage and trails subsequently with meaningful accuracy.


# Methodology

## Inclusion criteria

Data acquired from Parkinson’s Progression Markers Initiative (PPMI) dataset (https://www.ppmi-info.org/), on 21 March 2026. PPMI is a multi-center, longitudinal, and observational study that was launched in 2010. Each PPMI site was approved by the appropriate institutional review board before study initiation, and they all fully adhere to the principles set forth in the Declaration of Helsinki. All subjects provided written informed consent prior participation.

Drug naïve, with a levodopa equivalent daily dose (LEDD) of 0, disease duration within 2 years, early course with Hoehn-Yahr stage (H-Y stage) <3 and excluded participants with dementia at baseline; Patients below age 50 were also excluded to avoid cases of early onset PD; Maximum follow-up periods were set as 5 years; Two or more follow-ups were included, resulting in a total of 855 Parkinson’s Disease participants.


## Statistical analysis

Statistical analyses were performed in R (4.5.3) and Python (3.12.13).

Continuous variables were expressed as mean ± standard deviation (SD), categorical variables were presented as number and percentage. Differences among groups were assessed by the Kruskal-Wallis test for continuous variables and the chi-square test for categorical variables

To identify the underlying trajectory of multivariate, multlcmm function in the R package lcmm (Proust-Lima, 2017) was applied. Since MoCA suffers from ceiling effect and curvilinearity, we pre-transformed it with square root to make it approximately normally distributed (Wang, MY, 2025), other scales are REM Sleep Behavior Disorder Screening Questionnaire (RBDSQ) total score, MDS-UPDRS Part III Score OFF (includes OFF and untreated scores), ΔSBP (supine SBP minus standing SBP) (Chen K, 2021). We applied Z-score as sensitivity check, results are the same. (supplementary table)

Although nonlinear link function can better accommodate ceiling/floor effects and curvilinearity (Proust-Lima, 2011), in our data, linear link shows better classification quality with OCC>5 in each class. (supplementary table)

The fixed and mixture both included intercept and slope, random effect is specified on slope. Models with 1 to 4 classes were fitted, the final model was selected according to lowest Bayesian Information Criterion (BIC), mean posterior probabilities> 70%, class size>5%, relative entropy>0.7.


## XGBoost

The dataset contains PATNO, their respective class assignment (lcmm) , age, sex, race, baseline clinical scales, DaTScan features, Genetics and biomarkers and MRI features. The dataset was split into (70:15:15) train, validation, test set. Hyperparameters were optimised using Random search and 3 fold cross validation. We also used sample weights and balanced accuracy to tackle the problem of imbalanced classes. Model performance was evaluated using AUC.


# Results

3-class model was selected for subsequent analyses: class1 n=173(20.23%) severe/stable high burden group, class2 n=568(66.43%) stable/low burden group, class3 n=114(13.33%) late pRBD/increasing burden group.

All three classes had OCC values greater than 5. The residual standard errors were 1.25 for RBD, 14.15 for MoCA, 22.11 for UPDRS3, and 11.58 for delta SBP. The proportions of variance explained were 39.14%, 0.50%, 0.20%, 0.74%, respectively. We also compared the 3-class solution from the multivariate model with the 3-class RBD-only LCMM solution. The high agreement between the two classifications (ARI = 0.96; Cramer’s V = 0.95) indicated that the class structure was largely driven by the RBD trajectory.

Their baseline characteristics are summarized. (supplementary table) Baseline differences across classes were mainly observed in RBD and autonomic rather than in age, disease duration, education, cognition, or motor severity. Class 1 represented a high RBD and autonomic burden with broader non-motor impairment and lower DAT binding. Class 2 showed the mildest overall profile, with the lowest RBD and autonomic burden and relatively preserved DAT. Class 3 showed intermediate clinical severity at baseline, but relatively prominent autonomic and olfactory dysfunction, importantly, its DAT was generally closer to Class 1, indicating substantial dopaminergic deficit despite less extensive non-motor burden than Class 1.


```{figure} figure.png
:name: figure-main
:alt: Multi-panel figure supporting the main findings

\
**A.** Here we describe panel A.
\
**B.** Here we describe panel B.
\
**C.** Here we describe panel C.
```

```{csv-table} Multinomial Logistic Regression on Baseline Biomarkers (Reference: Class 2)[^1]
:header-rows: 1
:name: multinomial-reg-table
:align: center
:widths: 40, 10, 12, 13, 12, 13

"Predictor","N","Odds Ratio<br>(Class 1)","p-value<br>(Class 1)","Odds Ratio<br>(Class 3)","p-value<br>(Class 3)"
"Sex (Male=1)[^2]","834","**3.28**","**<.001**","1.45","0.215"
"Education (Years)[^2]","834","0.97","0.396","0.98","0.667"
"Age[^2]","834","1.01","0.597","0.99","0.765"
"UPSIT","834","**0.96**","**0.005**","**0.95**","**0.002**"
"Thalamus","474","**0.55**","**0.020**","0.98","0.954"
"Caudate","474","1.47","0.057","0.78","0.226"
"Putamen","474","**0.52**","**0.004**","0.84","0.420"
"Hippocampus","474","**1.64**","**0.038**","0.90","0.653"
"Choroid Plexus","474","0.72","0.105","1.04","0.853"
"Pallidum","474","1.23","0.271","**1.65**","**0.013**"
"Lateral Ventricle","474","1.05","0.835","0.79","0.344"
"Inf. Lat. Ventricle","474","1.31","0.175","1.07","0.751"
"WM Hypointensities","474","0.64","0.181","1.11","0.646"
"Cerebral White Matter","474","1.60","0.121","0.73","0.277"
"CSF $\alpha$-synuclein","240","1.00","0.130","1.00","0.490"
"CSF phosphorylated-$\tau$","240","1.12","0.203","1.06","0.345"
"CSF amyloid-$\beta$","240","1.00","0.630","1.00","0.248"
"UPSIT (sensitivity analysis)","240","0.97","0.233","0.95","0.076"
"Serum NfL Chain","240","1.04","0.167","0.98","0.560"
"Striatal SBR Caudate","240","0.38","0.425","1.09","0.941"
"Striatal SBR Putamen","240","0.16","0.222","0.10","0.092"
"APOE $\epsilon$4 (Carrier=1)","240","0.91","0.875","0.74","0.575"
```

```{csv-table} Comparison of MRI Volume Trajectory Slopes (Reference: Class 2)[^3]
:header-rows: 1
:name: lmm-slope-table
:align: center
:widths: 40, 10, 12, 13, 12, 13

"Region","p-value<br>(Class 1)","FDR q<0.10<br>(Class 1)","p-value<br>(Class 3)","FDR q<0.10<br>(Class 3)"
"Thalamus","0.950","0.990","0.835","0.928"
"Caudate","0.684","0.977","**0.036**","0.109"
"Putamen","0.433","0.865","0.306","0.510"
"Hippocampus","0.561","0.935","0.090","0.180"
"Choroid Plexus","0.990","0.990","**0.044**","0.109"
"Pallidum","0.271","0.865","0.990","0.990"
"Lateral Ventricle","0.393","0.865","**0.020**","0.101"
"Inf. Lat. Ventricle","0.054","0.336","**0.009**","**0.089**"
"Cerebral White Matter","0.799","0.990","0.430","0.538"
"WM Hypointensities","0.067","0.336","0.378","0.538"
```


[^1]: **Bolded** values indicate $p < 0.05$.
[^2]: Demographic variables (Age, Sex, Education) were included as controls in all models.
[^3]: Results surviving False Discovery Rate (FDR) correction are indicated in **bold** in addition to unadjusted $p < 0.05$ results.