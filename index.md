---
title: Parallels between RBDSQ Progression and Brain Morphology in Longitudinal Subtyping of PPMI Cohort
abstract: |
    This is a 100-150 word summary of our research, including the main objective, methods, key results, and conclusions. The abstract should provide readers with a clear overview of what the micropublication contains and its significance. Include the research question or hypothesis, the methodology employed, the key findings, and the main conclusions or implications of the work. This summary helps readers quickly assess whether the full content is relevant to their interests.
acknowledgments: |
    This work was supported by the Impact Scholars Program. We acknowledge the contributions of [former team members, teaching assistants, or mentors whose involvement does not meet the criteria of any authorship role].
---

# Introduction

Parkinson’s disease (PD) is one of the fastest-growing neurological disorders globally, presenting a significant challenge to healthcare systems and patient quality of life. Current estimates indicate that over 11 million people worldwide are living with the disease, with prevalent cases having increased by more than 270% since 1990 [@wangEpidemiologyParkinsonsDisease2026]. The economic impact is equally staggering; in the United States alone, the annual burden reached \$82.2 billion in 2024, a figure that surpassed previous projections by more than a decade. Without new interventions, these costs are expected to exceed \$112 billion by 2045 [@michaelj.foxfoundationforparkinsonsresearchEconomicBurdenParkinsons2026].  Despite decades of research, the primary obstacle in developing effective neuroprotective therapies is the sheer complexity of the disease, which is no longer viewed as a single, uniform condition but as a multifaceted syndrome. 

Current research in subtyping is essential to categorize this diversity into predictable patterns that facilitate precision medicine. Historically, subtyping relied on observable motor features, such as distinguishing between tremor-dominant and postural instability-gait difficulty (PIGD) phenotypes [@jankovicVariableExpressionParkinsons1990]. However, modern subtyping has evolved into a data-driven field focused on identifying distinct clinical phenotypes. Much of the existing literature supports a three-class model based on the severity and spread of symptoms [@fereshtehnejadNewClinicalSubtypes2015]. These typically include a "Mild Motor-Predominant" class with slower progression, an "Intermediate" class, and a "Diffuse Malignant" class characterized by rapid motor decline and significant non-motor complications. By identifying these subgroups, researchers can better tailor clinical trials to specific patient trajectories, which is one of the stated goals of PPMI [@marekParkinsonsProgressionMarkers2018].

It is generally observed that PD clinical subtypes are predominantly an early-stage phenomenon, often coalescing into a more uniform clinical presentation as the disease advances [@sauerbierNonMotorSubtypes2016]. While seminal baseline multi-modal clustering studies [@fereshtehnejadClinicalCriteriaSubtyping2017; @velucci2025nonmotor] have provided monumental insights into PD heterogeneity at a static time point, they are inherently limited in capturing the disease's most defining characteristic: its variable rate of progression. A central challenge remains in determining whether these initial clinical snapshots translate into sustained, divergent trajectories over time. Previous research has successfully employed univariate latent class growth models to study individual domains—such as cognition (MoCA) [@pourzinal2024profiling], autonomic function (SBP) [@chen2021orthostatic], sleep (RBDSQ) [@fangSelfperceivedLifeCourse2025] or motor progression (UPDRS) [@he2023motor]—evaluating these axes in isolation limits our understanding of PD as a multi-system disorder. 

To bridge this gap, our research undertakes an exploratory investigation using a multivariate longitudinal latent class model. Rather than assuming equal contribution across all symptom domains, this multi-dimensional approach allows the natural variance of the cohort to dictate the clustering, revealing which clinical scales predominantly drive longitudinal heterogeneity.Finally, we relate these emergent clinical phenotypes to targeted structural biomarkers — as highlighted in recent meta-analyses [@filideiParkinsonsDiseaseClinical2025], bridging the gap between data-driven clinical subtypes and their underlying biological correlates is a critical priority for the field.


# Methodology

## Participants

Data acquired from Parkinson’s Progression Markers Initiative (PPMI) dataset (https://www.ppmi-info.org/), on 21 March 2026. PPMI is a multi-center, longitudinal, and observational study that was launched in 2010. Each PPMI site was approved by the appropriate institutional review board before study initiation, and they all fully adhere to the principles set forth in the Declaration of Helsinki. All subjects provided written informed consent prior participation.

Participants were selected based on following criteria: drug naïve, with a levodopa equivalent daily dose (LEDD) of 0, disease duration within 2 years, early course with Hoehn-Yahr stage (H-Y stage) < 3 and without dementia at baseline. Patients below age 50 were also excluded to avoid cases of early onset PD. Maximum follow-up periods were set as 5 years, two or more follow-ups were included, resulting in a total of 855 Parkinson’s Disease participants.


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


## MRI Processing

Baseline morphological and quality control data were obtained directly from the PPMI repository, derived from the FreeSurfer (v7.3.2) and MRIQC (v23.1.0) pipelines within the nipoppy framework [@bhagwatProcessingAnalysisreadyImagederived2023]. To extend this to a longitudinal framework while maintaining computational efficiency, we independently processed all participants with available structural MRI at two or more visits (n = 382 of the total N = 855 inclusion cohort) using FastSurfer (v2.4.2) [@henschelFastSurferFastAccurate2020]. A total of 1036 scans were segmented, with volume statistics collated for regions defined by the Desikan-Killiany Atlas [@desikanAutomatedLabelingSystem2006]. One participant was subsequently excluded due to technical issues involving missing entries and extreme hemispheric asymmetry. The specific processing parameters and code for this pipeline are documented in the Colab notebooks within our GitHub repository.

## Secondary Analysis

Relating latent class models to external variables requires careful handling of estimation bias. The traditional "one-step" method—where covariates and the latent class model are estimated simultaneously—often suffers from model instability, as the inclusion of predictors can shift the latent structure itself. To avoid this, many studies fall into the trap of the "naive" three-step method (assigning participants to classes before regression), which produces biased parameter estimates by ignoring classification uncertainty. We instead employed the improved three-step and two-step frameworks developed to account for this uncertainty [@bolckEstimatingLatentStructure2004; @vermuntLatentClassModeling2010; @bakkTwoStepEstimationModels2018; @nylund-gibsonCovariatesMixtureModeling2016]. Specifically, we utilized the externVar function in the lcmm package [@proust-limaAccountingLatentClassn.d.], opting for the two-step method over the three-step bootstrap to maintain computational efficiency while achieving comparable bias reduction.

For the cross-sectional multinomial logistic regression, we used Freesurfer outputs, normalized by estimated Total Intracranial Volume (eTIV) to account for head size [@voevodskayaEffectsIntracranialVolume2014]. For the longitudinal Linear Mixed Models (LMM), which investigated atrophy and ventricular expansion rates, we used Fastsurfer outputs. Because Fastsurfer does not provide an eTIV estimate, these volumes were normalized using MaskVol; this shift in normalization was a necessary adaptation to the respective software pipelines rather than a change in statistical strategy.

Quality control for the Freesurfer data involved a rigorous outlier detection process using the Gap Statistic algorithm [@tibshiraniEstimatingNumberClusters2001] via the GapStatistics Python package [@loehrGapStatistics2025]. We focused on three key MRIQC metrics: the coefficient of joint variation (CJV), contrast-to-noise ratio (CNR), and entropy focus criterion.

The relationship between class membership and longitudinal atrophy (LMM) was implemented using the hlme function. We acknowledge that this specific analysis utilized a modal (naive) class assignment, as a corrected bias-adjustment method for LMMs was not available in the current lcmm implementation. Finally, we included UPSIT scores as a phenotypic validation check. Since hyposmia is a primary driver of PD heterogeneity [@velucci2025nonmotor], confirming its association with our latent classes provides a critical benchmark for the clinical validity of the subtypes identified by multilcmm.

## XGBoost

We employed XGBoost, a gradient boosting framework optimised for tabular data to predict the latent classes(found by lcmm) from baseline features only, with the of developing a lightweight model for real world resource constrained clinical application. It would enable clinicians to predict the subtype of Parkinson's patient in the first visit, only from baseline data to adjust dosage and trails subsequently with meaningful accuracy.

The dataset contains PATNO, their respective class assignment (lcmm) , age, sex, race, baseline clinical scales, DaTScan features, Genetics and biomarkers and MRI features. The dataset was split into (70:15:15) train, validation, test set. Hyperparameters were optimised using Random search and 3 fold cross validation. We also used sample weights and balanced accuracy to tackle the problem of imbalanced classes. Model performance was evaluated using AUC. SHAP was employed to explain the results of XGBoost.

# Results

<br/><br/>

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

<br/><br/>

3-class model was selected for subsequent analyses: class1 n=173(20.23%) severe/stable high burden group, class2 n=568(66.43%) stable/low burden group, class3 n=114(13.33%) late pRBD/increasing burden group. [Table 1](#main-model-selection) [Figure S2](supplementary.md#supp-trajectory)

All three classes had OCC values greater than 5. The residual standard errors were 1.25 for RBD, 14.15 for MoCA, 22.11 for UPDRS3, and 11.58 for ΔSBP. The proportions of variance explained were 39.14%, 0.50%, 0.20%, 0.74%, respectively. We compared the 3-class solution from the multivariate model with the 3-class RBD-only LCMM solution. The high agreement between the two classifications (ARI = 0.96; Cramer’s V = 0.95) indicated that the class structure was largely driven by the RBD trajectory. [Table S4](supplementary.md#supp-rbd-model-selection) [Table S5](supplementary.md#supp-rbd-class-comparison) [Figure S3](supplementary.md#supp-rbd-trajectory)

Baseline differences across classes were mainly observed in RBD and autonomic rather than in age, disease duration, education, cognition, or motor severity. Class 1 represented a high RBD and autonomic burden with broader non-motor impairment and lower DAT binding. Class 2 showed the mildest overall profile, with the lowest RBD, autonomic burden, and relatively preserved DAT. Class 3 showed intermediate severity at baseline, but relatively prominent autonomic and olfactory dysfunction, importantly, its DAT was generally closer to Class 1, indicating substantial dopaminergic deficit despite less extensive non-motor burden than Class 1. [Table S6](supplementary.md#supp-baseline-characteristics)


<br/><br/>

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

<br/><br/>

Red blood cells represent a significant source of interference in \alpha-synuclein assays [@barbourRedBloodCells2008]. To account for this, we leveraged the PPMI hemoglobin (Hb) threshold indicators. Comparative analysis confirmed that \alpha-synuclein levels did not differ significantly in median (Mann-Whitney $U$, $p$ = .627) or distribution (Kolmogorov-Smirnov, $p$ = .495) between samples with detectable Hb (n = 60) and those without (n = 265); consequently, the full sample was retained to maximize statistical power. Associations between monogenic PD variants and class membership were not evaluated due to the high prevalence of sporadic cases (N = 808, 94.5%). Furthermore, APOE\ epsilon4 status was binarized (carrier vs. non-carrier) because homozygous cases were too infrequent for independent analysis.

Multicollinearity was assessed using Variance Inflation Factors (VIF) via the car library [@johnfoxCompanionAppliedRegression2019], with all predictors yielding acceptable values (VIF < 5). To ensure model stability and numerical convergence, predictors were structured into two primary thematic blocks: MRI regional volumes (N = 474) and biofluid/clinical biomarkers (N = 240). Age, sex, and education were included as covariates in both models. Finally, UPSIT, Specific Binding Ratios (SBR), and APOE were evaluated using their maximum available sample sizes, with the more restricted combined model (N = 240) serving as a sensitivity analysis to verify the consistency of effect sizes and directions across cohorts.

Logistic regression was performed using the raw scales for all predictors to ensure model integrity. However, for the reported results, ORs for MRI metrics were calculated by standardizing the coefficients per standard deviation. This transformation was necessary because the raw numerical scales of normalized brain volumes (often <0.1% of eTIV) produce ORs that are either extreme or indistinguishable from 1.0, hindering cross-domain comparison. Clinical and biofluid markers remain on their raw scales for direct clinical interpretation.

To validate the clinical relevance of the identified latent classes, we compared baseline UPSIT scores across groups. Olfactory function was significantly lower for the high burden group ($p$ = .005) and the increasing burden group ($p$ = .002), providing a critical external benchmark for the model's validity. Because hyposmia is a robust herald of the "Diffuse Malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015], this confirms that our data-driven model successfully captured established biological patterns of PD heterogeneity, even though UPSIT scores were not included as indicators during the primary latent class estimation.

Our longitudinal analysis revealed distinct temporal dynamics between the identified phenotypes relative to the stable, low-burden baseline class. Notably, while the high burden class was characterized by more pronounced volumetric differences at baseline, the  increasing burden group distinguished itself primarily through differences in the rates of structural change over time. With a broad trend of accelerated ventricular and choroid plexus expansion aligning with the latter. However, given the exploratory nature of testing multiple regions and the statistical power constraints of our longitudinal subsample (n=382), the penalty of False Discovery Rate correction resulted in only the slope of Inferior Lateral Ventricle surviving threshold (q < .10). 

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

These findings suggest good predictive performance of baseline data, indicating potential utility while reinforcing our findings from latent class model.


# Discussion

The identification of three distinct longitudinal phenotypes within the PPMI cohort highlights the primacy of non-motor symptoms, specifically RBD, as the fundamental driver of PD heterogeneity. The high alignment between the multivariate model and RBDSQ trajectories (ARI = 0.96) suggests that sleep related dysfunction is a sentinel marker for the most aggressive disease pathways, outperforming traditional motor scales in early subtyping. 

These clinical classes are mirrored by clear structural neuroanatomical signatures, where the stable high burden group (Class 1) exhibits significant baseline atrophy in subcortical hubs like the thalamus and putamen. This is contrasted by a Hippocampal Paradox, in which larger baseline hippocampal volumes (OR = 1.64) are associated with Class 1, potentially indicating a selective vulnerability pattern where memory centers are initially spared in body first PD endotypes or exhibit early stage neuroinflammatory swelling.

In the increasing burden group (Class 3), the larger baseline pallidum may represent an early, albeit temporary, compensatory mechanism. However, the subsequent rapid ventricular expansion in this group serves as a superior longitudinal marker of widespread, non-dopaminergic neurodegeneration, characterizing its aggressive clinical trajectory.

By employing a robust two step estimation method via the externVar function to eliminate classification bias, this study provides a validated framework for using baseline clinical and imaging biomarkers to identify high risk patients at their first visit, facilitating more precise therapeutic interventions and clinical trial enrichment.


[^1]: **Bolded** values indicate $p < 0.05$.
[^2]: Demographic variables (Age, Sex, Education) were included as controls in all models.
[^3]: Results surviving False Discovery Rate (FDR) correction are indicated in **bold** in addition to unadjusted $p < 0.05$ results.