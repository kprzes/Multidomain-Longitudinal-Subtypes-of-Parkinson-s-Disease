---
title: REM Sleep Behaviour Disorder Dominates Heterogeneity in Longitudinal Analysis of Parkinson's Disease
abstract: |
    Parkinson’s disease (PD) exhibits significant clinical heterogeneity, yet the longitudinal interplay between multidomain symptoms and structural biomarkers remains underexplored. We analyzed 5-year data from the PPMI cohort (N=855) using multivariate latent class mixed modeling (multlcmm) to identify distinct progression phenotypes. A two-step externVar approach assessed class predictors, while Linear Mixed Models and XGBoost characterized longitudinal atrophy and early-stage subtype prediction. Three classes emerged: Stable High-Burden (Class 1, n=173), Low-Burden (Class 2, n=568), and Increasing-Burden (Class 3, n=114). Model assignment was primarily driven by RBDSQ trajectories (ARI = 0.96) and validated by significantly lower baseline UPSIT scores in Classes 1 and 3 ($p$ < .01). Class 1 exhibited pronounced baseline atrophy, whereas Class 3 demonstrated accelerated longitudinal structural change. SHAP analysis identified baseline RBDSQ as the most critical predictors of class membership.
acknowledgments: |
    This work was supported by the Impact Scholars Program. We thank the PPMI participants and staff.
---

# Introduction

Translational research mandates from the National Institutes of Health emphasize the urgent need to characterize the natural history of Parkinson’s disease (PD) and develop objective stratification tools [@sieberPrioritizedResearchRecommendations2014]. Large-scale cohort studies, such as the Parkinson’s Precision Medicine Initiative (PPMI), now provide the infrastructure necessary to discover data-driven progression subtypes and accelerate targeted therapeutic trials [@marekParkinsonsProgressionMarkers2018]. Historically, this stratification relied on baseline motor features, distinguishing between tremor-dominant and postural instability and gait difficulty (PIGD) phenotypes [@jankovicVariableExpressionParkinsons1990]. However, both clinical and data-driven subtypes are predominantly early-stage phenomena, often coalescing into a more uniform clinical presentation as the disease advances [@sauerbierNonMotorSubtypes2016].

Comprehensive multidomain clustering studies have significantly advanced our understanding of PD heterogeneity. By defining phenotypic profiles at a static baseline, standard distance-based clustering approaches have successfully identified subgroups with distinctly divergent clinical outcomes, such as the fast-progressing "diffuse malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015; @fereshtehnejadClinicalCriteriaSubtyping2017; @velucci2025nonmotor]. Notably, this same temporal approach is frequently mirrored even in studies utilizing advanced machine learning frameworks [@markelloMultimodalPhenotypicAxes2021]: phenotypic classes are established cross-sectionally, and longitudinal follow-up is only used post hoc to observe the progression of these fixed groups. Conversely, approaches that explicitly subtype patients based on progression rates have demonstrated the immense prognostic value of temporal data [@faghriPredictingOnsetProgression2018]. Yet, these machine learning methods often compress longitudinal follow-up into static summary vectors, obscuring the dynamic shape of the disease course. 

To capture actual symptom evolution, recent research has employed univariate latent class models to map individual domains over time, such as cognition [@pourzinal2024profiling], autonomic function [@chen2021orthostatic], and motor severity [@he2023motor]. Evaluating these axes in isolation limits our understanding of PD as a multi-system disorder. To bridge this gap, our research undertakes an exploratory investigation using a multivariate longitudinal Latent Class Mixed Model (LCMM). Rather than assuming equal contribution across all symptom domains, this multi-dimensional approach allows the natural variance of the cohort to dictate the clustering, revealing which clinical scales predominantly drive longitudinal heterogeneity. 

Finally, we relate these emergent clinical phenotypes to targeted biological metrics. Specifically, we focus on structural MRI, as morphological atrophy patterns have been shown to directly track both clinical disease severity and the trans-neuronal spread of PD pathology [@zeighamiNetworkStructureBrain2015]. As highlighted in a recent review [@filideiParkinsonsDiseaseClinical2025], bridging this gap between data-driven clinical subtypes and their underlying biological correlates is a critical priority for the field to ensure clinical classifications reflect true pathophysiological differences.

<br/><br/>

# Results

<br/><br/>

```{figure} figure.png
:name: figure-main
:alt: Multi-panel figure supporting the main findings

\
**A–D:** Observed mean trajectories of the 4 class indicator variables that defined the `multilcmm` model - Class 1 is the stable high burden group, Class 2 is stable low burden group and Class 3 is the increasing burden group.
\
**E:** Boxplots of subject-specific annual change rates (random slopes from LMM) for regions showing nominal differences between Class 2 (stable reference, green) and Class 3 (orange). Positive slopes = expansion, negative slopes = atrophy.  Red dashed line = no change. Only the inferior lateral ventricle difference survived false discovery rate correction (q<0.10).
\
**F:** Class-specific SHAP feature importance profiles. Bars indicate the mean absolute SHAP values, representing the global contribution of baseline features to XGBoost class assignment.
```

<br/><br/>

## Latent Class Identification and Trajectories
Multivariate LCMM identified a three-class solution as optimal based on the lowest BIC, mean posterior probabilities >70%, minimum class size >5%, and relative entropy >0.7 [Table 1](#main-model-selection), full methodological details are provided in [Supp.Methodology](#supp-methodology) : a Stable High-Burden class (Class 1, n = 173, 20.2%), a Low-Burden class (Class 2, n = 568, 66.4%), and an Increasing-Burden class (Class 3, n = 114, 13.3%). Observed mean trajectories are shown in [Figure 1 (A-D)](#figure-main). Class 1 maintained stably elevated RBDSQ scores above the diagnostic cutoff (≥5) throughout follow-up. Class 2 remained consistently below the cutoff across all five years. Class 3 started below the cutoff at baseline, crossed the threshold at approximately Year 2, and approached Class 1 levels by Year 5. ΔSBP increased progressively in Classes 1 and 3 while remaining stable in Class 2. UPDRS-III increased across all classes, most steeply in Class 1 from Year 3 onward. MoCA declined in Class 3 from Year 3–4 onward, falling below 26 by Year 5, while remaining relatively stable in Classes 1 and 2. Among the four indicators, residual standard errors were 1.25 for RBDSQ, 14.15 for MoCA, 22.11 for UPDRS-III, and 11.58 for ΔSBP, with RBDSQ accounting for the largest proportion of variance explained (39.1%), substantially exceeding ΔSBP (0.74%), MoCA (0.50%), and UPDRS-III (0.20%)., with the multivariate class structure showing strong agreement with the RBDSQ-only solution (ARI = 0.96; Cramér's V = 0.95) [Table S1](#supp-rbd-model-selection) [Table S2](#supp-rbd-class-comparison). For the description of baseline characteristics see [Supp.Baseline](#supp-baseline).



<br/><br/>

```{csv-table} Multivariate LCMM model (z-score) selection and classification metrics
:header-rows: 1
:name: main-model-selection
:align: center

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-18471.82","1.00","36969.64","37031.40","100.00","-","-"
"2","-18368.28","0.79","36768.56","36844.58","28.77<br>71.23","0.89<br>0.96","-"
"**3**","**-18297.93**","**0.75**","**36633.87**","**36724.14**","**20.23<br>66.43<br>13.33**","**0.87<br>0.92<br>0.79**","**26.00<br>5.98<br>24.00**"
"4","-18387.10","0.27","36818.20","36922.73","33.80<br>0.35<br>34.15<br>31.70","0.76<br>0.35<br>0.35<br>0.34","-"
```

<br/><br/>

## Baseline Neuroimaging and Biomarker Associations
To ensure computation stability and numerical convergence, predictors were structured into two primary thematic blocks: MRI regional volumes (N = 474) and biofluid/clinical biomarkers (N = 240). Age, sex, and education were included as covariates in both models. Finally, UPSIT, Specific Binding Ratios (SBR), and APOE were evaluated using their maximum available sample sizes, with the more restricted combined model (N = 240) serving as a sensitivity analysis to verify the consistency of effect sizes and directions across cohorts.

Logistic regression was performed using the raw scales for all predictors to ensure model integrity. However, for the reported results, ORs for MRI metrics were calculated by standardizing the coefficients per standard deviation. This transformation was necessary because the raw numerical scales of normalized brain volumes (often <0.1% of eTIV) produce ORs that are either extreme or indistinguishable from 1.0, hindering cross-domain comparison. Clinical and biofluid markers remain on their raw scales for direct clinical interpretation.

To validate the clinical relevance of the identified classes, we compared baseline UPSIT scores as an external benchmark. Olfactory function was significantly lower in both the high-burden ($p$ = .005) and increasing-burden ($p$ = .002) groups [Table 2](#multinomial-reg-table). Aligning with the "Diffuse Malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015], these findings confirm the model’s capacity to capture established biological patterns of PD heterogeneity using non-indicator variables.

## Longitudinal Structural Change
Longitudinal analysis revealed divergent temporal dynamics: while the high-burden class exhibited pronounced volumetric differences at baseline, the increasing-burden group was characterized by accelerated rates of structural change [Figure 1 (E)](#figure-main). We observed broad trends of accelerated ventricular and choroid plexus expansion in the latter; however, under rigorous False Discovery Rate correction (n = 382), only the inferior lateral ventricle slope survived the significance threshold ($q$ < .10) [Table 3](#lmm-slope-table).

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

## Early-Stage Subtype Prediction
The XGBoost model achieved an AUC of 0.88 and cross-validated balanced accuracy of 0.73. Baseline RBDSQ was the single most discriminative predictor of class membership by both split frequency and information gain, tripling the next-ranked feature. Class-specific SHAP analysis [Figure 1 (F)](#figure-main) revealed that Class 1 was overwhelmingly driven by RBD severity; Class 2 showed a more distributed profile led by RBD, olfactory function, autonomic dysfunction, and anxiety; and Class 3 had the broadest SHAP profile with postural instability and dopaminergic imaging as notable contributors, consistent with its lower classification accuracy (F1 = 0.36). CSF α-synuclein SAA ranked prominently in native tree metrics but not in SHAP values, reflecting population-level rather than patient-level discriminative utility.

<br/><br/>

# Discussion
While REM sleep behavior disorder is a well-established prognostic marker, it is typically deployed in progression studies as a static or binary baseline feature [@velucci2025nonmotor; @liuLongitudinalChangesParkinsons2021]. Our findings highlight its dynamic evolution. In our longitudinal analysis, many individual clinical scales failed to form distinct subtypes independently (with BIC favoring single-class solutions). Instead, longitudinal RBDSQ trajectories contributed the vast majority of the variance, driving the latent class structure and demonstrating that RBD-related heterogeneity evolves well beyond the prodromal stage.

This longitudinal approach yields markedly different prognostic insights compared to baseline clustering. For instance, the highly cited diffuse/malignant phenotype [@fereshtehnejadNewClinicalSubtypes2015] couples a wide breadth of severe baseline symptoms with rapid global progression. While our Class 1 shares this severe baseline multi-domain profile (Table S6) and resembles the RBD+ cluster [@velucci2025nonmotor], its symptom progression was not exclusively the most rapid. Instead, Class 3 demonstrated the steepest multi-domain deterioration despite much milder baseline symptoms. Because our multivariate LCMM models domain-specific trajectories rather than collapsing metrics into a single composite score, these results confirm that initial symptom burden and subsequent progression rates represent distinct, decoupled dimensions of Parkinson's disease heterogeneity.

Consequently, our trajectory-derived subtypes align less with traditional baseline clustering and more closely with studies focused specifically on longitudinal RBD progression. Notably, our data-driven classes remarkably mirror the a priori clinical groups defined by @Ye2022RBDProgressionPD. Their largest group, the non-RBD-stable phenotype, matches our low-burden stable class (Class 2). Our Class 3 strongly aligns with their "late-RBD" group (12.1% of their cohort), showing a late-emerging probable RBD trajectory that crosses the clinical threshold around Year 2. This transitional, high-risk phenotype exhibits baseline olfactory impairment and orthostatic hypotension [@y.saitohImpactLateonsetREM], signaling non-motor vulnerability before overt RBD emergence. Finally, our high-burden Class 1 likely represents a combination of their pRBD-stable and pRBD-reversion phenotypes—supported by a slight reversion in Class 1's RBDSQ scores during Years 4 and 5—as our fit metrics (AIC/BIC) did not support splitting into a four-class solution.

Finally, while we did not directly measure α-synuclein pathology, these distinct trajectories tentatively align with proposed models of Lewy body spatial progression. Class 1's early concurrent triad of RBD, autonomic, and olfactory dysfunction resembles a "body-first" or brainstem-early trajectory [@borghammerBrainFirstGutFirstParkinsons2019; @mastenbroekDiseaseProgressionModelling2024]. Conversely, Class 3's post-motor RBD onset and rapid cognitive decline suggests a "brain-first" origin with delayed, steep brainstem involvement. Class 2, persistently lacking RBD, may represent a phenotype where pathology remains temporarily confined to olfactory regions. Ultimately, the longitudinal timing of RBD expression appears to carry critical, albeit interpretive, pathophysiological weight.

Smaller baseline thalamus and putamen volumes predict membership in the high-burden class relative to the low-burden stable class, matching literature identifying these regions as structural markers for pRBD and aggressive PD [@boucettaStructuralBrainAlterations2016; @ellmoreReducedVolumePutamen2010; @rahayelBrainAtrophyParkinsons2019; @salsoneReducedThalamicVolume2014]. Conversely, the high-burden and increasing-burden classes predicted larger baseline volumes in the hippocampus and pallidum, respectively. While pRBD is sometimes associated with volume loss in these structures [@limNeuralSubstratesRapid2016], morphometric analysis demonstrates that PD patients without RBD exhibit significant localized surface shape contraction in both the hippocampus and pallidum [@rahayelBrainAtrophyParkinsons2019]. Because this low-burden stable population serves as our statistical reference group, we hypothesize that their localized shape deformations distort automated boundary detection, artificially manifesting as relative hypertrophy in our tracking classes.

Longitudinally, neurodegeneration tracks clinical evolution; the increasing-burden class displays accelerated ventricular and choroid plexus expansion — a marker of progressive central atrophy and altered cerebrospinal fluid dynamics linked to impaired glymphatic clearance [@he2023motor]—alongside slower caudate atrophy relative to the low-burden stable class, highlighting distinct subcortical phenotypes requiring future whole-brain context.

<br/><br/>

$^\dagger$ These authors contributed equally to this work.

<br/><br/>


[^1]: **Bolded** values indicate $p < 0.05$.
[^2]: Demographic variables (Age, Sex, Education) were included as controls in all models.
[^3]: Results surviving False Discovery Rate (FDR) correction are indicated in **bold** in addition to unadjusted $p < 0.05$ results.






# Supplementary material

## List of Abbreviations

AIC
: Akaike Information Criterion

APOE $\epsilon$4
: Apolipoprotein E (gene) $\epsilon$4 variant

ARI
: Adjusted Rand Index

AUC
: Area Under the Curve

BIC
: Bayesian Information Criterion

CSF
: Cerebrospinal Fluid

CV
: Cross-Validation

DAT
: Dopamine Transporter (imaging)

$\Delta$SBP
: Delta Systolic Blood Pressure

eTIV
: estimated Total Intracranial Volume

Hb
: Hemoglobin

LCMM
: Latent Class Mixed Model (R function)

LEDD
: Levodopa Equivalent Daily Dose

LMM
: Linear Mixed Model

MCAR
: Missing Completely at Random (statistical test)

MDS-UPDRS
: Movement Disorder Society Unified Parkinson's Disease Rating Scale

MoCA
: Montreal Cognitive Assessment

MRIQC
: MRI Quality Control (pipeline)

OCC
: Odds of Correct Classification

OR
: Odds Ratio

PATNO
: Patient Number (in PPMI)

PIGD
: Postural Instability and Gait Difficulty

PD
: Parkinson’s Disease

PPMI
: Parkinson's Precision Medicine Initiative (formerly Parkinson's Progression Markers Initiative)

RBD
: REM Sleep Behaviour Disorder

RBDSQ
: REM Sleep Behaviour Disorder Screening Questionnaire

ROC
: Receiver Operating Characteristic

SAA
: Seed Amplification Assay

SBR
: Striatal Binding Ratio

SCOPA-AUT
: Scales for Outcomes in Parkinson's Disease - Autonomic Dysfunction

SHAP
: SHapley Additive exPlanations

STAI
: State-Trait Anxiety Inventory

UPSIT
: University of Pennsylvania Smell Identification Test

VIF
: Variance Inflation Factor

WM
: White Matter

<br/><br/>

(supp-methodology)=
## Methodology


### Participants

Data acquired from Parkinson’s Progression Markers Initiative (PPMI) dataset (https://www.ppmi-info.org/), on 21 March 2026. PPMI is a multi-center, longitudinal, and observational study that was launched in 2010. Each PPMI site was approved by the appropriate institutional review board before study initiation, and they all fully adhere to the principles set forth in the Declaration of Helsinki. All subjects provided written informed consent prior participation.

Participants were included if they met the following criteria at baseline: (1) drug-naïve with a levodopa equivalent daily dose (LEDD) of 0; (2) disease duration within 2 years; (3) early-stage disease defined by Hoehn-Yahr stage < 3; (4) no dementia; and (5) age onset ≥ 50 years to exclude early-onset Parkinson's disease. Participants were followed for up to 5 years, and only those with two or more follow-up visits were included, resulting in a total of 855 participants with Parkinson's disease.


### Trajectory analysis
Analyses were performed in R (4.5.3) and Python (3.12.13). `multlcmm` function in the R package `lcmm` [@proustlima2017lcmm] was applied for trajectory analysis. This approach follows the rationale of group-based trajectory modeling [@naginGroupBasedTrajectory2010], allowing several longitudinal markers measured on different clinical scales, to inform a common underlying latent disease process while accounting for marker-specific measurement relationships. Latent classes and individual membership probabilities were estimated within a maximum-likelihood framework, providing asymptotically unbiased parameter estimates under a missing-at-random assumption. Follow-up time since baseline, measured in years, was used as the time indicator. The following steps were performed to optimize the analysis:

1.	**Literature-informed scale selection:** Candidate scales were chosen to represent major PD progression domains based on prior subtyping studies. The initial set included RBDSQ, SCOPA-AUT, STAI, age- and education-adjusted SDMT T-scores, and the MDS-UPDRS Part III OFF-medication score (UPDRS Part III) [@velucci2025nonmotor; @he2023motor]. However, modeling above five scales together failed to meet minimum criteria: mean posterior probabilities > 0.7 or minimum class proportions > 5%.

2.	**Indicator refinement:** To ensure model constrction from scales with longitudinal signals and optimal class seperation, we evaluated candidate scales in univariate LCMM, and prioritized scales that had been studied in univariate model. The final set is RBDSQ, MoCA[@wangPredictiveModelLongitudinal2025], UPDRS Part III, ΔSBP [@chen2021orthostatic]. 

3.	**Link function & distributioanl consideration:** Although nonlinear link functions better accommodate ceiling/floor effects and curvilinearity of psychometric scales [@proustlima2011misuse], their application in our multivariate framework resulted in reduced classification quality (relative entropy <0.7 or OCC <5). Therefore, a linear link function was adopted for all indicators. To address MoCA's known curvilinearity and ceiling effect, square root transformation was applied prior to modeling [@wangPredictiveModelLongitudinal2025]. 

4.	**Random effects specification:** Models with random intercept-slope and random intercept only were both evaluated. Both identified a 3-class solution as optimal under linear link; however, the random intercept and slope model did not converge. The final model therefore specified random intercept only, with fixed and mixture components including both intercept and slope terms.

5.	**Model selection:** Models with 1 to 4 classes were fitted. The final model was selected based on lowest BIC, mean posterior probabilities >70%, minimum class size >5%, and relative entropy >0.7 [@lennon2018framework].

6.	**Scale contribution assessment:** Residual standard error and variance explained proportion were examined to evaluate each indicator's contribution to the multivariate model.

7.	**Class assignment validation:** To assess the consistency of class solutions, comparisons were performed using confusion matrices, Adjusted Rand Index (ARI), and Cramér's V.

8.	**Sensitivity analyses:** Models were initially estimated using raw/pre-transformed scores. As z-standardized scores yielded identical class solutions (ARI = 1, Cramér's V = 1) while facilitating convergence in downstream analyses, z-standardized scores were adopted as the primary model specification.


### Missingness and attrition
The missing rates for RBDSQ, MoCA, ΔSBP, and UPDRS Part III were 0.88%, 1.09%, 2.99%, and 15.99%, respectively. LCMM accommodates incomplete longitudinal data, so no additional missingness handling was performed. Little's MCAR test was significant (χ² = 208, df = 28, p < .001), indicating that data were not missing completely at random. Differential attrition was observed across classes, with Year 5 completion rates of 20.2%, 28.5%, and 41.2% for Classes 1, 2, and 3, respectively. As Class 1 also exhibited the overall highest baseline disease burden, attrition was likely associated with observed disease severity, supporting MAR as a reasonable assumption. Although LCMM is expected to limit the impact of differential attrition under MAR, later trajectory estimates for Class 1 are based on a smaller and potentially less severely affected subsample, which may limit their representativeness.


### Clinical assessments
The above selected four input clinical scales, each representing a core clinical domain (sleep, cognitive, autonomic, and motor):

1.	**REM sleep behavior disorder (RBD):** Defined by a score ≥5 on the REM Sleep Behavior Disorder Screening Questionnaire (RBDSQ), a 10-item self-report instrument (maximum total score 13 points) designed to screen for RBD [@stiasnykolster2007rbd].

2.	**Global cognitive function:** Assessed through the Montreal Cognitive Assessment (MoCA), adjusted for education. A score below 26 was used as the cutoff for cognitive impairment [@nasreddine2005moca].

3.	**Orthostatic hypotension:** Quantified as the orthostatic change in systolic blood pressure (ΔSBP, supine SBP minus standing SBP upon standing). A ΔSBP ≥20 mmHg within 3 min of standing was considered indicative of clinically significant orthostatic hypotension [@freeman2011consensus].

4.	**Motor severity:** Evaluated using the Movement Disorder Society – Unified Parkinson's Disease Rating Scale (MDS-UPDRS) Part III. A score between 33 to 58 was considered moderate motor impairment [@martinezmartin2015severity].


(supp-baseline)=
### Baseline Characteristics
Baseline characteristics across the three classes were compared using the Kruskal-Wallis test for continuous variables and the chi-square test for categorical variables. Pairwise comparisons were conducted using Dunn's test for continuous variables and chi-square tests for categorical variables, with Benjamini-Hochberg false discovery rate (FDR) correction applied to all pairwise comparisons. Continuous variables were expressed as mean ± standard deviation (SD), categorical variables were presented as number and percentage. 

Baseline clinical characteristics across the three classes are summarized in (). Classes did not differ significantly in age at diagnosis, disease duration, years of education, Hoehn-Yahr stage, dominant side of symptom onset, or cognitive status at enrollment. Class 1 was distinguished by significantly higher RBDSQ scores, greater autonomic dysfunction (SCOPA-AUT, ΔSBP), worse olfactory function (UPSIT), higher anxiety (STAI), depressive symptoms (GDS), daytime sleepiness (ESS), and greater functional impairment (UPDRS-I, UPDRS-II, PIGD, ADL) compared to Class 2 (all p < 0.05). Class 3 showed significantly worse olfactory function than Class 2 (UPSIT p < 0.001) and greater autonomic dysfunction (SCOPA-AUT p = 0.002), but did not differ significantly from Class 2 on most other clinical scales at baseline. Class 1 had the highest proportion of male participants (80.9%), significantly exceeding both Class 2 (61.4%, p < 0.0001) and Class 3 (74.6%, p = 0.016)

Baseline biomarker and neuroimaging characteristics are presented in (). CSF biomarkers (Aβ, α-synuclein, p-tau, tau), serum NfL, urate, and APOE ε4 status did not differ significantly between classes. CSF α-synuclein seed amplification assay (SAA) positivity rates showed a nominally significant overall difference (p = 0.014), driven by a higher proportion of SAA-negative cases in Class 2 (11.7%) compared to Class 1 (5.0%) and Class 3 (4.6%), though pairwise comparisons did not survive FDR correction. Striatal DAT binding in the putamen was severely reduced across all three classes with no significant between-group differences, consistent with the shared nigrostriatal pathology of early-stage PD. On cross-sectional MRI, subcortical gray matter volume showed a nominally significant overall difference (p = 0.022), with Class 2 showing numerically larger volumes; thalamic volume also differed nominally across groups (p = 0.005), with Class 2 showing the largest values.


### MRI processing

Baseline morphological and quality control data were obtained directly from the PPMI repository, derived from the FreeSurfer (v7.3.2) and MRIQC (v23.1.0) pipelines within the nipoppy framework [@bhagwatProcessingAnalysisreadyImagederived2023]. To extend this to a longitudinal framework while maintaining computational efficiency, we independently processed all participants with available structural MRI at two or more visits (n = 382 of the total N = 855 inclusion cohort) using FastSurfer (v2.4.2) [@henschelFastSurferFastAccurate2020]. A total of 1036 scans were segmented, with volume statistics collated for regions defined by the Desikan-Killiany Atlas [@desikanAutomatedLabelingSystem2006]. One participant was subsequently excluded due to technical issues involving missing entries and extreme hemispheric asymmetry. The specific processing parameters and code for this pipeline are documented in the Colab notebooks within our GitHub repository.

Quality control for the Freesurfer data involved a rigorous outlier detection process using the Gap Statistic algorithm [@tibshiraniEstimatingNumberClusters2001] via the GapStatistics Python package [@loehrGapStatistics2025]. We focused on three key MRIQC metrics: the coefficient of joint variation (CJV), contrast-to-noise ratio (CNR), and entropy focus criterion.

### Secondary Analysis

Relating latent class models to external variables requires careful handling of estimation bias. The traditional "one-step" method where covariates and the latent class model are estimated simultaneously often suffers from model instability, as the inclusion of predictors can shift the latent structure itself. To avoid this, many studies fall into the trap of the "naive" three-step method (assigning participants to classes before regression), which produces biased parameter estimates by ignoring classification uncertainty. We instead employed the improved three-step and two-step frameworks developed to account for this uncertainty [@bolckEstimatingLatentStructure2004; @vermuntLatentClassModeling2010; @bakkTwoStepEstimationModels2018; @nylund-gibsonCovariatesMixtureModeling2016]. Specifically, we utilized the `externVar` function in the lcmm package [@proust-limaAccountingLatentClassn.d.], opting for the two-step method over the three-step bootstrap to maintain computational efficiency while achieving comparable bias reduction.

Predictors were selected based on their importance to PD pathogenesis according to prior literature. Multicollinearity was assessed using Variance Inflation Factors (VIF) via the car library [@johnfoxCompanionAppliedRegression2019], with all predictors yielding acceptable values (VIF < 5).

Red blood cells represent a significant source of interference in α-synuclein assays [@barbourRedBloodCells2008]. To account for this, we leveraged the PPMI hemoglobin (Hb) threshold indicators. Comparative analysis confirmed that α-synuclein levels did not differ significantly in median (Mann-Whitney U, p = .627) or distribution (Kolmogorov-Smirnov, p = .495) between samples with detectable Hb (n = 60) and those without (n = 265); consequently, the full sample was retained to maximize statistical power. Associations between monogenic PD variants and class membership were not evaluated due to the high prevalence of sporadic cases (N = 808, 94.5%). Furthermore, APOE ε4 status was binarized (carrier vs. non-carrier) because homozygous cases were too infrequent for independent analysis.

The relationship between class membership and longitudinal atrophy (LMM) was implemented using the hlme function. We acknowledge that this specific analysis utilized a modal (naive) class assignment, as a corrected bias-adjustment method for LMMs was not available in the current lcmm implementation. 

For the cross-sectional multinomial logistic regression, we used Freesurfer outputs, normalized by estimated Total Intracranial Volume (eTIV) to account for head size [@voevodskayaEffectsIntracranialVolume2014]. For the longitudinal Linear Mixed Models (LMM), which investigated atrophy and ventricular expansion rates, we used Fastsurfer outputs. Because Fastsurfer does not provide an eTIV estimate, these volumes were normalized using MaskVol; this shift in normalization was a necessary adaptation to the respective software pipelines rather than a change in statistical strategy.


### XGBoost

We employed XGBoost, a gradient boosting framework optimised for tabular data to predict the latent classes from baseline features, with the of developing a lightweight model. The dataset contains PATNO, their respective class assignment , age, sex, race, baseline clinical scales, DaTScan features, genetics and biofluid markers. The dataset was split into (70:15:15) train, validation, test set. Hyperparameters were optimised using Random search and 3 fold cross validation. We also used sample weights and balanced accuracy to tackle the problem of imbalanced classes. Model performance was evaluated using AUC. SHAP was employed to explain the results of XGBoost.



### Table S1
RBDSQ LCMM model selection and classification metrics

```{csv-table} 
:header-rows: 1
:name: supp-rbd-model-selection-2dp
:align: center
:widths: 8, 16, 16, 12, 12, 22, 22, 12

"K","Log-likelihood","Relative entropy","AIC","BIC","Proportion per class (%)","Average posterior probability","OCC"
"1","-7504.38","1.00","15016.75","15035.76","100.00","-","-"
"2","-7403.28","0.80","14820.56","14853.82","27.37<br>72.63","0.90<br>0.96","-"
"**3**","**-7326.08**","**0.76**","**14672.16**","**14719.67**","**19.30<br>66.43<br>14.27**","**0.87<br>0.92<br>0.79**","**27.90<br>6.11<br>23.10**"
"4","-7326.08","0.54","14678.16","14739.92","15.32<br>19.42<br>65.26<br>0.00","0.77<br>0.87<br>0.68<br>NaN","-"
```
*Note. The 4-class model yielded an empty class (0.00%) and undefined posterior probability (NaN), indicating a degenerate solution.


### Table S2
Comparison of class assignments between the z-score multivariate LCMM model (A) and the RBD-only LCMM model (C)
```{csv-table} 
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



### Figure S1

RBDSQ Estimated Mean Trajectories with 95% CIs and Raw Individual Trajectories in the MultLCMM (z-score model)

```{raw} latex
\begin{figure}[h]
\centering
\includegraphics[width=\textheight, angle=90]{./s2.png}
\end{figure}
```


### Figure S2
LMM Predicted Trajectories, for regions where nominal differences were found between Class 2 and Class 3
```{image} ./s4.png
:name: lmm-predicty
:align: center
:width: 100%
```


### Figure S5
SHAP beeswarm plot for Class 1
```{image} ./s5.png
:name: supp-shap
:align: center
:width: 80%

```
(supp-roc)=
### Figure S6
ROC curves for one-vs-rest on the test set
```{image} ./s6.png
:name: supp-roc
:align: center
:width: 80%

```


## Limitations, Strengths, and Future Directions

### Cohort and Clinical Measurement Constraints
Several limitations should be considered when interpreting these findings. First, while the PPMI dataset provides an unprecedented de novo PD cohort, it represents a highly educated, predominantly white demographic that excludes atypical parkinsonism or early dementia, limiting immediate generalizability to broader clinical populations. Clinically, REM sleep behavior disorder was assessed via the RBDSQ rather than polysomnography, reflecting probable symptom trajectories (pRBD) rather than confirmed diagnoses. Additionally, simplifying the multisystem complexity of PD by representing each clinical domain with a single scale, alongside collecting data post-diagnosis, prevents us from inferring the exact temporal order of early pathological events or $\alpha$-synuclein propagation.

### Statistical Modeling, Missing Data, and Distal Outcomes
Second, the use of Latent Class Mixed Models (LCMM) inherently assumes discrete categorical subpopulations within a continuous neurodegenerative spectrum. While LCMM natively handles missing longitudinal data, our secondary covariate analysis evaluates baseline variables as class predictors using a bias-adjusted 3-step method (`externVar()`). This framework highlights associations rather than strict causality and is currently restricted to a complete-case subset with overlapping biomarker data. To eliminate missing variable bias and leverage the full $N = 855$ cohort for secondary inference, future work will implement multiple imputation for these baseline biomarkers. Furthermore, while `externVar()` was deployed here exclusively for baseline predictors, it can also be used in future iterations of this work to relate trajectory classes directly to distal clinical outcomes, such as reaching Hoehn & Yahr Stage 3, mild cognitive impairment (MCI), and dementia.

### Neuroimaging Feature Selection and Pipeline Consistency
Third, our structural MRI analysis was restricted to a targeted subset of mostly subcortical regional volumes. This restricted feature selection was a strict statistical necessity: the parameter-heavy, bias-adjusted 3-step method introduces severe convergence issues if overloaded with variables, constraining our initial model and leaving broader cortical alterations unexplored. To resolve this and expand our feature space into cortical thickness and broader regional volumes, future work will integrate a wider array of cortical metrics. To ensure strict within-subject consistency across these expanded longitudinal metrics, future iterations will transition from standard automated segmentation to a dedicated longitudinal pipeline utilizing FastSurfer with Surf-Recon, contingent on sufficient computational resources.

### Study Strengths
Despite these limitations, our longitudinal multidomain approach successfully identifies progression phenotypes based on within-person change rather than static baseline severity alone. The robust associations demonstrating clear alignment between these latent trajectory classes and underlying clinical, biomarker, and MRI features strongly support their physiological relevance to dissecting PD heterogeneity.


### Table S3: Baseline Characteristics

```{figure} ./bl1.png
:name: baseline-1
:align: center
:width: 100%

Baseline characteristics (Part 1): Model indicators, demographics, and non-motor scales.
```

```{figure} ./bl2.png
:name: baseline-2
:align: center
:width: 100%

Baseline characteristics (Part 2): Cognitive tests, motor and functional scales.
```

```{figure} ./bl3.png
:name: baseline-3
:align: center
:width: 100%

Baseline characteristics (Part 3): Biomarkers and subcortical volumes.
```

```{figure} ./bl4.png
:name: baseline-4
:align: center
:width: 100%

Baseline characteristics (Part 4): Ventricular, cortical, white matter, and corpus callosum volumes.
```

```{figure} ./bl5.png
:name: baseline-5
:align: center
:width: 100%

Baseline characteristics (Part 5): Cortical thickness, Part 1 (Desikan-Killiany Atlas).
```


```{figure} ./bl6.png
:name: baseline-6
:align: center
:width: 100%

Baseline characteristics (Part 6): Cortical thickness, Part 2 (Desikan-Killiany Atlas).
```

