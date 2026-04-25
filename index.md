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

## Participants

Data acquired from Parkinson’s Progression Markers Initiative (PPMI) dataset (https://www.ppmi-info.org/) on 21 March 2026. PPMI is a multi-center, longitudinal, and observational study that was launched in 2010. Each PPMI site was approved by the appropriate institutional review board before study initiation, and fully adhere to the principles set forth in the Declaration of Helsinki. All subjects provided written informed consent prior participation.

Participants were selected based on following criteria: drug naïve, with a levodopa equivalent daily dose (LEDD) of 0, disease duration within 2 years, early course with Hoehn-Yahr stage (H-Y stage) <3 and without dementia at baseline. Patients below age 50 were also excluded to avoid cases of early onset PD. Maximum follow-up periods were set as 5 years, two or more follow-ups were included, resulting in a total of 855 Parkinson’s Disease participants.



## Statistical analysis

Statistical analyses were performed in R (4.5.3) and Python (3.12.13). Continuous variables were expressed as mean ± standard deviation (SD), categorical variables were presented as number and percentage. Differences among groups were assessed by the Kruskal-Wallis test (continuous variables) and the chi-square test (categorical variables), pairwise comparisons were presented with Mann–Whitney U (continuous variables) and chi-square test (categorical variables), and was corrected by with Benjamini–Hochberg FDR.

To identify the underlying trajectory of multivariate, multlcmm function in the R package lcmm [@proustlima2017lcmm] was applied. The following steps were performed to optimize the analysis:

(1) Literature-based scale selection: we first selected REM Sleep Behavior Disorder Screening Questionnaire (RBDSQ), Scales for Outcomes in Parkinson’s Disease–Autonomic (SCOPA-AUT), State-Trait Anxiety Inventory (STAI), Symbol Digit Modalities Test (SDMT, T-score adjusted for age and education), as 4 non-motor domain representatives based on prior cross-sectional subtyping study [@velucci2025nonmotor], also with MDS-UPDRS Part III Score OFF for motor domain [@he2023motor], however, they did not yield optimal results in multivariate model together with z-standardized with linear link or raw score with nonlinear link function.

(2) Candidate scale screening: to make sure we construct multivariate model from scales with longitudinal signals, we evaluated candidate scales in univariate model under different link function, and prioritized scales that had been studied in univariate latent class mixed model. The final set is RBDSQ total score, Montreal Cognitive Assessment (MoCA) Score (adjusted for education) [@pourzinal2024profiling], MDS-UPDRS Part III Score OFF, ΔSBP (supine SBP minus standing SBP) [@chen2021orthostatic].

(3) Scale contribution assessment: we analyzed residual standard error, Variance Explained proportion, and compared the multidomain class assignments with univariate class assignment using Adjusted Rand Index (ARI), and Cramer’s V. 

(4) Link function assessment: although nonlinear link function can better accommodate ceiling/floor effects and curvilinearity [@proustlima2011misuse], in our data, linear link shows better classification quality with relative entropy>0.7, and Odds of Correct Classification (OCC) >5 in each class. Since MoCA suffers from ceiling effect and curvilinearity, we pre-transformed it with square root to make it approximately normally distributed (Wang, 2025), other scales were raw scores. We z-standardized scales as sensitivity check, results are the same. [Table S1](supplementary.md#supp-model-selection) [Table S2](supplementary.md#supp-class-comparison)

(5) Random effects assessment: random effects with both intercept and slope or only slope were both analyzed. Under linear link, both settings identified 3-class with lowest Bayesian Information Criterion (BIC), however, random effects with both intercept and slope did not converge.

(6) Model selection: the fixed and mixture both included intercept and slope, random effect is specified on slope. Models with 1 to 4 classes were fitted, the final model was selected according to lowest Bayesian Information Criterion (BIC), average posterior probabilities> 70%, class size>5%, relative entropy>0.7. [@lennon2018framework]

(7) Missingness and attrition: the missing rates for RBD, MoCA, delta SBP, and UPDRS3 were 0.9%, 1.1%, 3%, and 16%, respectively. [Figure S1](supplementary.md#missing-pattern) LCMM can accommodate incomplete longitudinal data, so no additional missing-data handling was performed. Little’s MCAR test was significant (p < 0.05), indicating that the data were not missing completely at random. Since participants with more severe disease were more likely to drop out, we assumed the data were missing at random. The majority of participants of three class had dropped by year 5, Class1 showed the highest attrition. [Table S3](supplementary.md#supp-attrition-table)


## XGBoost

The dataset contains PATNO, their respective class assignment (lcmm) , age, sex, race, baseline clinical scales, DaTScan features, Genetics and biomarkers and MRI features. The dataset was split into (70:15:15) train, validation, test set. Hyperparameters were optimised using Random search and 3 fold cross validation. We also used sample weights and balanced accuracy to tackle the problem of imbalanced classes. Model performance was evaluated using AUC.


# Results

## Identification and clinical characterization of subtypes

3-class model was selected for subsequent analyses: class1 n=173(20.23%) severe /stable high burden group, class2 n=568(66.43%) stable/low burden group, class3 n=114(13.33%) late pRBD/increasing burden group. [Table 1](#main-model-selection) [Figure S2](supplementary.md#supp-trajectory)

All three classes had OCC values greater than 5. The residual standard errors were 1.25 for RBD, 14.15 for MoCA, 22.11 for UPDRS3, and 11.58 for ΔSBP. The proportions of variance explained were 39.14%, 0.50%, 0.20%, 0.74%, respectively. We compared the 3-class solution from the multivariate model with the 3-class RBD-only LCMM solution. The high agreement between the two classifications (ARI = 0.96; Cramer’s V = 0.95) indicated that the class structure was largely driven by the RBD trajectory. [Table S4](supplementary.md#supp-rbd-model-selection) [Table S5](supplementary.md#supp-rbd-class-comparison) [Figure S3](supplementary.md#supp-rbd-trajectory)

Baseline differences across classes were mainly observed in RBD and autonomic rather than in age, disease duration, education, cognition, or motor severity. Class 1 represented a high RBD and autonomic burden with broader non-motor impairment and lower DAT binding. Class 2 showed the mildest overall profile, with the lowest RBD, autonomic burden, and relatively preserved DAT. Class 3 showed intermediate severity at baseline, but relatively prominent autonomic and olfactory dysfunction, importantly, its DAT was generally closer to Class 1, indicating substantial dopaminergic deficit despite less extensive non-motor burden than Class 1. [Table S6](supplementary.md#supp-baseline-characteristics)


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

```{csv-table} Multivariate LCMM model selection and classification metrics
:header-rows: 1
:name: main-model-selection
:align: center
:widths: 8, 16, 16, 12, 12, 22, 22, 12

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-35284.04","1.0000000","70594.07","70655.84","100.00000","-","-"
"2","-35180.50","0.7946713","70392.99","70469.01","28.77193<br>71.22807","0.8942<br>0.9606","-"
"3","**-35110.15**","**0.7527719**","**70258.30**","**70348.57**","**20.23392**<br>**66.43275**<br>**13.33333**","**0.8684**<br>**0.9221**<br>**0.7868**","**26.0**<br>**5.98**<br>**24.0**"
"4","-35110.15","0.4963126","70264.30","70368.82","15.08772<br>20.46784<br>64.44444<br>0","0.7431<br>0.8622<br>0.5680<br>NaN","-"
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