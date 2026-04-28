---
title: Parallels between RBDSQ Progression and Brain Morphology in Longitudinal Subtyping of PPMI Cohort
abstract: |
    Parkinson’s disease (PD) exhibits significant clinical heterogeneity, yet the longitudinal interplay between multidomain symptoms and structural biomarkers remains underexplored. We analyzed 5-year data from the PPMI cohort (N=855) using multivariate latent class mixed modeling (multlcmm) to identify distinct progression phenotypes. A two-step externVar approach assessed class predictors, while Linear Mixed Models and XGBoost characterized longitudinal atrophy and early-stage subtype prediction. Three classes emerged: Stable High-Burden (Class 1, n=173), Low-Burden (Class 2, n=568), and Increasing-Burden (Class 3, n=114). Model assignment was primarily driven by RBDSQ trajectories (ARI = 0.96) and validated by significantly lower baseline UPSIT scores in Classes 1 and 3 ($p$ < .01). Class 1 exhibited pronounced baseline atrophy, whereas Class 3 demonstrated accelerated longitudinal structural change. SHAP analysis identified baseline RBDSQ and CSF $\alpha$-synuclein as the most critical predictors of class membership.
acknowledgments: |
    This work was supported by the Impact Scholars Program. We thank the PPMI participants and staff.
---

# Introduction

Parkinson’s disease (PD) is one of the fastest-growing neurological disorders globally, presenting a significant challenge to healthcare systems and patient quality of life [@wangEpidemiologyParkinsonsDisease2026; @michaelj.foxfoundationforparkinsonsresearchEconomicBurdenParkinsons2026]. It is generally observed that PD clinical subtypes are predominantly an early-stage phenomenon, often coalescing into a more uniform clinical presentation as the disease advances [@sauerbierNonMotorSubtypes2016]. While seminal baseline multi-modal clustering studies [@fereshtehnejadClinicalCriteriaSubtyping2017; @velucci2025nonmotor] have provided monumental insights into PD heterogeneity at a static time point, they are inherently limited in capturing the disease’s most defining characteristic: its variable rate of progression. A central challenge remains in determining whether these initial clinical snapshots translate into sustained, divergent trajectories over time. Previous research has successfully employed univariate latent class growth models to study individual domains—such as cognition (MoCA) [@pourzinal2024profiling], autonomic function (ΔSBP) [@chen2021orthostatic], and motor progression (MDS-UPDRS Part  III) [@he2023motor]. For sleep domain, previous studies often use the RBD screening questionnaire (RBDSQ), a verified easily applicable self-screening tool [@StiasnyKolster2007RBDSQ] to perform cross-sectional analysis [@Iijima2021RBDOlfactoryPD; @Bjornara2013RBDGenderPD], limited in discovering the heterogeneous evolution pattern in early-stage Parkinson’s disease[@Ye2022RBDProgressionPD]. Evaluating these axes in isolation limits our understanding of PD as a multi-system disorder. To offer multidemential perspective, our research undertakes an exploratory investigation using a multivariate longitudinal latent class model. We also relate these emergent clinical phenotypes to targeted structural biomarkers as highlighted in recent meta-analyses [@filideiParkinsonsDiseaseClinical2025], bridging the gap between data-driven clinical subtypes and their underlying biological correlates is a critical priority for the field.

<br/><br/>

# Methodology

## Trajectory Analysis

Statistical analyses were performed in R (4.5.3) and Python (3.12.13) ([Supp.Participants](#supp-participants); [Supp.Missingness and attrition](#supp-missingness-attrition)). We employed a systematic optimization of the multlcmm framework [@proustlima2017lcmm] to identify multidomain trajectories:

1.	**Indicator Selection & Filtration:** Seven candidate class indicators (RBDSQ, SCOPA-AUT, STAI, SDMT, MDS-UPDRS III, MoCA, and $\Delta$SBP) were selected based on @velucci2025nonmotor, @he2023motor, and @chen2021orthostatic. Following univariate screening and multivariate testing, three (SCOPA-AUT, STAI, SDMT) were excluded as they failed to contribute to optimal class separability or provided redundant longitudinal signal.

2.	**Structural Optimization:** Initial models evaluated both random intercepts and slopes. However, to prevent uninformative severity-driven clusters and ensure the algorithm identified true multidomain heterogeneity rather than just "mild vs. severe" groupings, we restricted the model to a random-intercept-only structure.

3.	**Link Function & Transform:** A parsimonious linear link combined with square-root transformed MoCA to resolve ceiling effects [@wangPredictiveModelLongitudinal2025] was required to achieve sufficient class separability. This specification satisfied @lennon2018framework criteria with OCC > 5 across all classes (concurrently with entropy > 0.7), whereas nonlinear functions (splines/beta) failed to meet these standards.

4.	**Model Selection & Validation:** Iterative versions were evaluated via VarExpl() to quantify indicator contributions. We used confusion matrices, Adjusted Rand Index (ARI), and Cramer’s V to compare multivariate assignments against univariate benchmarks. Notably, the linear link produced identical class assignments for both raw and z-standardized models — a unique stability not observed with alternative links.

The final 3-class model (RBDSQ, MoCA, MDS-UPDRS III, $\Delta$SBP) was selected based on the lowest Bayesian Information Criterion (BIC) and class sizes $> 5\%$. The z-standardized model was utilized for secondary analysis.


## Secondary Analysis

MRI processing, quality control and other data preparation details are described in [Supp.MRI](#supp-mri-processing) and [Supp.Data](#supp-data-preparation). 

Relating latent class models to external variables requires careful handling of estimation bias. The traditional "one-step" method—where covariates and the latent class model are estimated simultaneously—often suffers from model instability, as the inclusion of predictors can shift the latent structure itself. To avoid this, many studies fall into the trap of the "naive" three-step method (assigning participants to classes before regression), which produces biased parameter estimates by ignoring classification uncertainty. We instead employed the improved three-step and two-step frameworks developed to account for this uncertainty [@bolckEstimatingLatentStructure2004; @vermuntLatentClassModeling2010; @bakkTwoStepEstimationModels2018; @nylund-gibsonCovariatesMixtureModeling2016]. Specifically, we utilized the externVar function in the lcmm package [@proust-limaAccountingLatentClassn.d.], opting for the two-step method over the three-step bootstrap to maintain computational efficiency while achieving comparable bias reduction.

The relationship between class membership and longitudinal atrophy (LMM) was implemented using the hlme function. We acknowledge that this specific analysis utilized a modal (naive) class assignment, as a corrected bias-adjustment method for LMMs was not available in the current lcmm implementation. 


## XGBoost

We employed XGBoost, a gradient boosting framework optimised for tabular data to predict the latent classes from baseline features. The dataset contains PATNO, their respective class assignment , age, sex, race, baseline clinical scales, DaTScan features, genetics and biofluid markers. The dataset was split into (70:15:15) train, validation, test set. Hyperparameters were optimised using Random search and 3 fold cross validation. We also used sample weights and balanced accuracy to tackle the problem of imbalanced classes. Model performance was evaluated using AUC. SHAP was employed to explain the results of XGBoost.

<br/><br/>

# Results

<br/><br/>

```{figure} figure.png
:name: figure-main
:alt: Multi-panel figure supporting the main findings

\
**A–D:** Trajectories of the 4 class indicator variables that defined the multilcmm model - Class 1 is the stable high burden group, Class 2 is stable low burden group and Class 3 is the increasing burden group.
\
**E:** Boxplots of the Individual annual slopes (Empirical Bayes estimates) demonstrate significantly accelerated atrophy or expansion in Class 3 (orange) compared to the relatively stable Class 2 (green), with a red dashed line indicating the threshold of no change.
```

<br/><br/>

3-class model was selected for subsequent analyses: class1 n=173(20.23%) severe/stable high burden group, class2 n=568(66.43%) stable/low burden group, class3 n=114(13.33%) late pRBD/increasing burden group. [Table 1](#main-model-selection) [Figure S2](supplementary.md#supp-trajectory)

All three classes had OCC values greater than 5. The residual standard errors were 1.25 for RBD, 14.15 for MoCA, 22.11 for UPDRS3, and 11.58 for ΔSBP. The proportions of variance explained were 39.14%, 0.50%, 0.20%, 0.74%, respectively. We compared the 3-class solution from the multivariate model with the 3-class RBD-only LCMM solution. The high agreement between the two classifications (ARI = 0.96; Cramer’s V = 0.95) indicated that the class structure was largely driven by the RBD trajectory. [Table S4](supplementary.md#supp-rbd-model-selection) [Table S5](supplementary.md#supp-rbd-class-comparison) [Figure S3](supplementary.md#supp-rbd-trajectory)

For the description of baseline characteristics see [Supp.Baseline](#supp-baseline).

<br/><br/>

```{csv-table} Multivariate LCMM model (z-score) selection and classification metrics
:header-rows: 1
:name: main-model-selection
:align: center

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-18471.82","1.0000000","36969.64","37031.40","100.00000","-","-"
"2","-18368.28","0.7946719","36768.56","36844.58","28.77193<br>71.22807","0.8942<br>0.9606","-"
"3","-18297.93","0.7527719","36633.87","36724.14","20.23392<br>66.43275<br>13.33333","0.8684<br>0.9221<br>0.7868","26.0<br>5.98<br>24.0"
"4","-18387.10","0.2705212","36818.20","36922.73","33.80117<br>0.35088<br>34.15205<br>31.69591","0.7633<br>0.3481<br>0.3461<br>0.3431","-"
```

<br/><br/>

To ensure model stability and numerical convergence, predictors were structured into two primary thematic blocks: MRI regional volumes (N = 474) and biofluid/clinical biomarkers (N = 240). Age, sex, and education were included as covariates in both models. Finally, UPSIT, Specific Binding Ratios (SBR), and APOE were evaluated using their maximum available sample sizes, with the more restricted combined model (N = 240) serving as a sensitivity analysis to verify the consistency of effect sizes and directions across cohorts.

Logistic regression was performed using the raw scales for all predictors to ensure model integrity. However, for the reported results, ORs for MRI metrics were calculated by standardizing the coefficients per standard deviation. This transformation was necessary because the raw numerical scales of normalized brain volumes (often <0.1% of eTIV) produce ORs that are either extreme or indistinguishable from 1.0, hindering cross-domain comparison. Clinical and biofluid markers remain on their raw scales for direct clinical interpretation.

To validate the clinical relevance of the identified classes, we compared baseline UPSIT scores as an external benchmark. Olfactory function was significantly lower in both the high-burden ($p$ = .005) and increasing-burden ($p$ = .002) groups. Aligning with the "Diffuse Malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015], these findings confirm the model’s capacity to capture established biological patterns of PD heterogeneity using non-indicator variables.

Longitudinal analysis revealed divergent temporal dynamics: while the high-burden class exhibited pronounced volumetric differences at baseline, the increasing-burden group was characterized by accelerated rates of structural change. We observed broad trends of accelerated ventricular and choroid plexus expansion in the latter; however, under rigorous False Discovery Rate correction (n = 382), only the inferior lateral ventricle slope survived the significance threshold ($q$ < .10).

<br/><br/>


```{csv-table} Multinomial Logistic Regression on Baseline Biomarkers (Reference: Class 2)[^1][^2]
:header-rows: 1
:name: multinomial-reg-table
:align: center
:widths: 40, 10, 12, 13, 12, 13

"Predictor","N","Odds Ratio<br>(Class 1)","p-value<br>(Class 1)","Odds Ratio<br>(Class 3)","p-value<br>(Class 3)"
"Sex (Male=1)","834","**3.28**","**<.001**","1.45","0.215"
"Education (Years)","834","0.97","0.396","0.98","0.667"
"Age","834","1.01","0.597","0.99","0.765"
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

<br/><br/>

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

<br/><br/>

The XGBoost model achieved an AUC of 0.88 and a CV balanced accuracy of 0.73 on test set with a maximum tree depth of 4 and learning rate of 0.06. SHAP analysis revealed REM (RBDSQ) as the most important predictor of classes followed by CSF ɑ-synuclein levels at baseline.


# Discussion

Three longitudinal phenotypes identified in the PPMI cohort establish REM sleep behavior disorder (RBD) as a primary driver of Parkinson’s disease (PD) heterogeneity. The near-total alignment between multivariate and RBDSQ-only trajectories (ARI = 0.96) positions sleep dysfunction as a sentinel marker for aggressive disease pathways, surpassing traditional motor scales in early subtyping utility.

These clinical phenotypes map to distinct neuroanatomical signatures. The stable high-burden group (Class 1) exhibited significant baseline atrophy in the thalamus and putamen, contrasted by a "Hippocampal Paradox" (OR = 1.64) where larger baseline volumes were associated with high-burden status [@vanpettenRelationshipHippocampalVolume2004; dickersonIncreasedHippocampalActivation2005]. This may reflect early-stage neuroinflammatory swelling or the selective preservation of memory centers in "body-first" endotypes [@borghammerBrainFirstGutFirstParkinsons2019]. Conversely, in the increasing-burden group (Class 3), larger baseline pallidal volumes — potentially representing transient compensatory mechanisms — preceded rapid ventricular expansion. This expansion serves as a robust longitudinal marker for the widespread non-dopaminergic neurodegeneration characterizing this group's aggressive trajectory.

<br/><br/>

$^\dagger$ These authors contributed equally to this work.

<br/><br/>


[^1]: **Bolded** values indicate $p < 0.05$.
[^2]: Demographic variables (Age, Sex, Education) were included as controls in all models.
[^3]: Results surviving False Discovery Rate (FDR) correction are indicated in **bold** in addition to unadjusted $p < 0.05$ results.




















# Supplementary Material

## Trajectory analysis
(supp-participants)=
### Participants
PPMI is an ongoing multicenter longitudinal observational study, launched in 2010. Before study initiation, each site was approved by the appropriate institutional review, and fully in accordance with the Declaration of Helsinki. All subjects provided written informed consent before participation.
Inclusion criteria: drug naïve, with a levodopa equivalent daily dose (LEDD) of 0, disease duration within 2 years, early course with Hoehn-Yahr stage (H-Y stage) < 3 and without dementia at baseline. Patients below age 50 were also excluded to avoid cases of early onset PD. Maximum follow-up periods were set as 5 years, two or more follow-ups were included, resulting in a total of 855 Parkinson’s Disease participants.

(supp-missingness-attrition)=
### Missingness and attrition
the missing rates for RBD, MoCA, delta SBP, and UPDRS3 were 0.9%, 1.1%, 3%, and 16%, respectively. Figure S1 LCMM can accommodate incomplete longitudinal data, so no additional missing-data handling was performed. Little’s MCAR test was significant (p < 0.05), indicating that the data were not missing completely at random. Since participants with more severe disease were more likely to drop out, we assumed the data were missing at random. The majority of participants of three class had dropped by year 5, Class1 showed the highest attrition. 

(supp-baseline)=
### Baseline Characteristics
Baseline differences across classes were mainly observed in RBD and autonomic rather than in age, disease duration, education, cognition, or motor severity. Class 1 represented a high RBD and autonomic burden with broader non-motor impairment and lower DAT binding. Class 2 showed the mildest overall profile, with the lowest RBD, autonomic burden, and relatively preserved DAT. Class 3 showed intermediate severity at baseline, but relatively prominent autonomic and olfactory dysfunction, importantly, its DAT was generally closer to Class 1, indicating substantial dopaminergic deficit despite less extensive non-motor burden than Class 1. [Table S6](supplementary.md#supp-baseline-characteristics)


### Table S1
```{csv-table} Multivariate LCMM model selection and classification metrics
:header-rows: 1
:name: supp-model-selection
:align: center
:widths: 8, 16, 16, 12, 12, 22, 22, 12

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-35284.04","1.0000000","70594.07","70655.84","100.00000","-","-"
"2","-35180.50","0.7946713","70392.99","70469.01","28.77193<br>71.22807","0.8942<br>0.9606","-"
"3","**-35110.15**","**0.7527719**","**70258.30**","**70348.57**","**20.23392**<br>**66.43275**<br>**13.33333**","**0.8684**<br>**0.9221**<br>**0.7868**","**26.0**<br>**5.98**<br>**24.0**"
"4","-35110.15","0.4963126","70264.30","70368.82","15.08772<br>20.46784<br>64.44444<br>0","0.7431<br>0.8622<br>0.5680<br>NaN","-"
```

```{csv-table} Agreement of multidomain class assignments between the raw-score/transformed-MoCA model (A) and the z-score model (B)
:header-rows: 1
:name: supp-class-comparison
:align: center
:widths: 20, 15, 15, 15, 15

"","B: Class 1","B: Class 2","B: Class 3","Total"
"A: Class 1","173","0","0","173"
"A: Class 2","0","568","0","568"
"A: Class 3","0","0","114","114"
"Total","173","568","114","855"
```
ARI = 1; Cramér's V = 1.


```{figure} ./s3.png
:name: missing-pattern
:align: center
:width: 60%

Missing data pattern.
```


```{csv-table} Attrition by latent class across follow-up years
:header-rows: 1
:name: supp-attrition-table
:align: center
:widths: 18, 16, 16, 16, 16, 16, 16

"Class","Baseline","Year 1","Year 2","Year 3","Year 4","Year 5"
"Class 1","173<br>(100.0%)","170<br>(98.3%)","125<br>(72.3%)","80<br>(46.2%)","48<br>(27.7%)","35<br>(20.2%)"
"Class 2","568<br>(100.0%)","548<br>(96.5%)","447<br>(78.7%)","319<br>(56.2%)","217<br>(38.2%)","162<br>(28.5%)"
"Class 3","114<br>(100.0%)","110<br>(96.5%)","99<br>(86.8%)","82<br>(71.9%)","65<br>(57.0%)","47<br>(41.2%)"
```


```{figure} ./s1.png
:name: supp-trajectory
:align: center
:width: 80%

Multivariate model - Estimated mean with 95% CI and observed mean.
```



```{csv-table} RBD LCMM model selection and classification metrics
:header-rows: 1
:name: supp-rbd-model-selection
:align: center
:widths: 8, 16, 16, 12, 12, 22, 22, 12

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-7504.377","1.0000000","15016.75","15035.76","100.00000","-","-"
"2","-7403.282","0.7973444","14820.56","14853.82","27.36842<br>72.63158","0.9015<br>0.9577","-"
"3","**-7326.080**","**0.7573811**","**14672.16**","**14719.67**","**19.29825**<br>**66.43275**<br>**14.26901**","**0.8697**<br>**0.9236**<br>**0.7935**","**27.9**<br>**6.11**<br>**23.1**"
"4","-7326.080","0.5375571","14678.16","14739.92","15.32164<br>19.41520<br>65.26316<br>0.00000","0.7700<br>0.8665<br>0.6770<br>NaN","-"
```

```{csv-table} Comparison of class assignments between the raw-score/transformed-MoCA multivariate LCMM model (A) and the RBD-only LCMM model (C)
:header-rows: 1
:name: supp-rbd-class-comparison
:align: center
:widths: 20, 15, 15, 15, 15

"","A: Class 1","A: Class 2","A: Class 3","Total"
"C: Class 1","163","2","0","165"
"C: Class 2","1","564","3","568"
"C: Class 3","9","2","111","122"
"Total","173","568","114","855"
```

ARI = 0.956; Cramér's V = 0.950.


```{figure} ./s2.png
:name: supp-rbd-trajectory
:align: center
:width: 100%

RBD LCMM - Estimated mean trajectory with 95% CI and raw individual trajectories.
```

```{csv-table} Baseline characteristics by latent class
:header-rows: 1
:name: supp-baseline-characteristics
:align: center
:widths: 26, 14, 14, 14, 12, 12, 12, 12, 12

"Variable","Class 1","Class 2","Class 3","P-value","Class 1 vs 2","Class 1 vs 3","Class 2 vs 3","P-value (FDR)"
"RBD","8.7 (1.8)","2.8 (1.8)","3.8 (1.9)","<0.0001","<0.0001","<0.0001","<0.0001","<0.0001"
"MoCA","26.5 (2.6)","26.8 (2.4)","26.6 (2.5)","0.498","0.655","0.655","0.655","0.611"
"UPDRS Part III","22.7 (10.6)","22.3 (9.6)","22.1 (9.5)","0.940","0.935","0.935","0.935","0.960"
"ΔSBP","6.6 (13.6)","3.0 (11.8)","6.8 (15.1)","0.003","0.006","0.608","0.067","0.007"
"Age at PD diagnosis","65.4 (7.1)","65.0 (7.2)","65.5 (6.5)","0.700","0.839","0.839","0.839","0.802"
"Years of education capped at 20","15.9 (2.9)","16.0 (2.8)","16.0 (2.8)","0.882","0.808","0.808","0.808","0.921"
"Duration from PD diagnosis to enrollment (years)","0.6 (0.5)","0.7 (0.5)","0.6 (0.5)","0.386","0.545","0.944","0.545","0.511"
"Men","140 (80.9)","349 (61.4)","85 (74.6)","<0.0001","<0.0001","0.256","0.016","<0.0001"
"UPSIT raw score","20.3 (7.8)","23.0 (8.1)","19.8 (6.2)","<0.0001","<0.001","0.915","<0.001","<0.0001"
"SCOPA-AUT total score","14.3 (7.5)","9.4 (5.9)","11.4 (6.4)","<0.0001","<0.001","<0.001","0.001","<0.0001"
"State-Trait Anxiety Index (STAI) total score","66.7 (18.5)","62.7 (17.6)","62.9 (18.7)","0.022","0.020","0.084","0.856","0.038"
"Geriatric Depression Scale score","2.8 (2.6)","2.2 (2.6)","2.2 (2.2)","<0.001","<0.001","0.047","0.446","0.003"
"Epworth Sleepiness Scale score","6.4 (3.8)","5.4 (3.4)","5.5 (3.3)","0.003","0.002","0.081","0.573","0.008"
"Questionnaire for Impulsive-Compulsive Disorders in PD (QUIP) score","0.4 (0.8)","0.2 (0.5)","0.3 (0.7)","0.036","0.033","0.374","0.374","0.059"
"DVT_CLKDRAW","64.4 (15.1)","64.7 (13.9)","66.3 (9.8)","0.981","0.954","0.954","0.954","0.981"
"DVT_TOTAL_RECALL","45.0 (10.8)","46.3 (11.2)","45.0 (10.7)","0.437","0.596","0.903","0.596","0.555"
"DVT_DELAYED_RECALL","44.1 (11.3)","44.6 (12.3)","44.4 (12.3)","0.808","0.830","0.830","0.830","0.883"
"DVT_RETENTION","45.1 (12.0)","45.8 (12.2)","45.5 (12.2)","0.507","0.642","0.642","0.995","0.611"
"DVT_FAS","50.3 (10.9)","49.8 (10.9)","49.4 (11.4)","0.857","0.836","0.836","0.836","0.916"
"DVS_JLO_MSSAE","11.7 (2.8)","11.9 (2.9)","12.2 (3.0)","0.318","0.577","0.321","0.344","0.440"
"DVT_SDM","45.2 (9.9)","46.7 (9.7)","45.1 (8.5)","0.392","0.596","0.647","0.596","0.511"
"DVS_LNS","11.5 (2.7)","11.7 (2.9)","11.2 (2.9)","0.176","0.442","0.457","0.262","0.251"
"MSEADLG","92.8 (6.6)","94.2 (6.1)","93.0 (5.3)","0.003","0.018","0.755","0.016","0.007"
"PIGD","0.3 (0.3)","0.2 (0.2)","0.2 (0.2)","0.003","0.034","0.002","0.034","0.007"
"UPDRS1 score","8.3 (5.1)","5.7 (4.0)","6.3 (4.0)","<0.0001","<0.0001","<0.0001","0.090","<0.0001"
"UPDRS2 score","8.0 (5.1)","5.8 (4.2)","6.2 (3.7)","<0.0001","<0.0001","0.006","0.169","<0.0001"
"UPDRS total score","39.2 (15.9)","33.8 (13.9)","34.5 (13.2)","<0.001","<0.001","0.047","0.343","0.002"
"MIA_CAUDATE_L","0.7 (0.3)","0.8 (0.3)","0.7 (0.3)","0.002","0.006","0.694","0.029","0.005"
"MIA_CAUDATE_R","0.7 (0.3)","0.8 (0.3)","0.8 (0.3)","0.015","0.014","0.279","0.289","0.027"
"MIA_CAUDATE_BILAT","0.7 (0.3)","0.8 (0.3)","0.8 (0.3)","0.002","0.004","0.413","0.082","0.007"
"MIA_PUTAMEN_L","0.7 (0.3)","0.8 (0.3)","0.7 (0.3)","0.013","0.109","0.314","0.026","0.025"
"MIA_PUTAMEN_R","0.7 (0.3)","0.8 (0.3)","0.7 (0.3)","0.056","0.127","0.857","0.149","0.085"
"MIA_PUTAMEN_BILAT","0.7 (0.3)","0.8 (0.3)","0.7 (0.3)","0.005","0.039","0.463","0.017","0.010"
"MIA_STRIATUM_L","0.7 (0.2)","0.8 (0.3)","0.7 (0.2)","0.001","0.009","0.550","0.009","0.004"
"MIA_STRIATUM_R","0.8 (0.3)","0.8 (0.3)","0.8 (0.2)","0.007","0.012","0.523","0.100","0.014"
"MIA_STRIATUM_BILAT","0.7 (0.2)","0.8 (0.2)","0.8 (0.2)","<0.001","0.005","0.891","0.007","0.002"
"DOMSIDE = 1.0","73 (43.2)","246 (43.5)","40 (35.1)","0.110","0.532","0.115","0.115","0.161"
"DOMSIDE = 2.0","95 (56.2)","309 (54.7)","69 (60.5)","","","","",""
"DOMSIDE = 3.0","1 (0.6)","10 (1.8)","5 (4.4)","","","","",""
"NHY = 1.0","58 (33.5)","203 (35.8)","36 (31.6)","0.639","0.829","0.829","0.829","0.751"
"NHY = 2.0","115 (66.5)","364 (64.2)","78 (68.4)","","","","",""
"cogstate = 1.0","117 (88.6)","382 (89.7)","59 (92.2)","0.744","0.860","0.860","0.860","0.833"
"cogstate = 2.0","15 (11.4)","44 (10.3)","5 (7.8)","","","","",""
```


## Secondary analysis
(supp-mri-processing)=
### MRI processing
Baseline morphological and quality control data were obtained directly from the PPMI repository, derived from the FreeSurfer (v7.3.2) and MRIQC (v23.1.0) pipelines within the nipoppy framework [@bhagwatProcessingAnalysisreadyImagederived2023]. To extend this to a longitudinal framework while maintaining computational efficiency, we independently processed all participants with available structural MRI at two or more visits (n = 382 of the total N = 855 inclusion cohort) using FastSurfer (v2.4.2) [@henschelFastSurferFastAccurate2020]. A total of 1036 scans were segmented, with volume statistics collated for regions defined by the Desikan-Killiany Atlas [@desikanAutomatedLabelingSystem2006]. One participant was subsequently excluded due to technical issues involving missing entries and extreme hemispheric asymmetry. The specific processing parameters and code for this pipeline are documented in the Colab notebooks within our GitHub repository.

For the cross-sectional multinomial logistic regression, we used Freesurfer outputs, normalized by estimated Total Intracranial Volume (eTIV) to account for head size [@voevodskayaEffectsIntracranialVolume2014]. For the longitudinal Linear Mixed Models (LMM), which investigated atrophy and ventricular expansion rates, we used Fastsurfer outputs. Because Fastsurfer does not provide an eTIV estimate, these volumes were normalized using MaskVol; this shift in normalization was a necessary adaptation to the respective software pipelines rather than a change in statistical strategy.

Quality control for the Freesurfer data involved a rigorous outlier detection process using the Gap Statistic algorithm [@tibshiraniEstimatingNumberClusters2001] via the GapStatistics Python package [@loehrGapStatistics2025]. We focused on three key MRIQC metrics: the coefficient of joint variation (CJV), contrast-to-noise ratio (CNR), and entropy focus criterion.


(supp-data-preparation)=
### Data preparation
Red blood cells represent a significant source of interference in $\alpha$-synuclein assays [@barbourRedBloodCells2008]. To account for this, we leveraged the PPMI hemoglobin (Hb) threshold indicators. Comparative analysis confirmed that \alpha-synuclein levels did not differ significantly in median (Mann-Whitney U, p = .627) or distribution (Kolmogorov-Smirnov, p = .495) between samples with detectable Hb (n = 60) and those without (n = 265); consequently, the full sample was retained to maximize statistical power. Associations between monogenic PD variants and class membership were not evaluated due to the high prevalence of sporadic cases (N = 808, 94.5%). Furthermore, APOE\ epsilon4 status was binarized (carrier vs. non-carrier) because homozygous cases were too infrequent for independent analysis.

Multicollinearity was assessed using Variance Inflation Factors (VIF) via the car library [@johnfoxCompanionAppliedRegression2019], with all predictors yielding acceptable values (VIF < 5).


```{figure} ./s4.png
:name: lmm-predicty
:align: center
:width: 100%

LMM Predicted Trajectories, for regions where nominal differences were found between Class 2 and Class 3
```


```{figure} ./s5.png
:name: beeswarm-plot
:align: center
:width: 100%

SHAP beeswarm plot
REM (RBDSQ) is the most important baseline predictor of classes
```

```{figure} ./s6.png
:name: roc-curve
:align: center
:width: 100%

AUC ROC curve for XGBoost model (test set).
Total AUC = 0.88
```