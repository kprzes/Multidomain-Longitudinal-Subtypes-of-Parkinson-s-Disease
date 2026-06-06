---
title: REM Sleep Behaviour Disorder Dominates Heterogeneity in Longitudinal Analysis of Parkinson's Disease
abstract: |
    Parkinson’s disease (PD) exhibits significant clinical heterogeneity, yet the longitudinal interplay between multidomain symptoms and structural biomarkers remains underexplored. We analyzed 5-year data from the PPMI cohort (N=855) using multivariate latent class mixed modeling (multlcmm) to identify distinct progression phenotypes. A two-step externVar approach assessed class predictors, while Linear Mixed Models and XGBoost characterized longitudinal atrophy and early-stage subtype prediction. Three classes emerged: Stable High-Burden (Class 1, n=173), Low-Burden (Class 2, n=568), and Increasing-Burden (Class 3, n=114). Model assignment was primarily driven by RBDSQ trajectories (ARI = 0.96) and validated by significantly lower baseline UPSIT scores in Classes 1 and 3 ($p$ < .01). Class 1 exhibited pronounced baseline atrophy, whereas Class 3 demonstrated accelerated longitudinal structural change. SHAP analysis identified baseline RBDSQ as the most critical predictor of class membership.
acknowledgments: |
    This work was supported by the Impact Scholars Program. We thank the PPMI participants and staff.
---

# Introduction

Translational research mandates from the National Institutes of Health emphasize the urgent need to characterize the natural history of Parkinson’s disease (PD) and develop objective stratification tools [@sieberPrioritizedResearchRecommendations2014]. Large-scale cohort studies, such as the Parkinson’s Precision Medicine Initiative (PPMI), now provide the infrastructure to discover data-driven progression subtypes and accelerate targeted therapeutic trials [@marekParkinsonsProgressionMarkers2018]. Historically, stratification relied on baseline motor features such as tremor-dominant and PIGD phenotypes [@jankovicVariableExpressionParkinsons1990]. However, both clinical and data-driven subtypes are predominantly early-stage phenomena, often coalescing into a more uniform clinical presentation as the disease advances [@sauerbierNonMotorSubtypes2016].

Comprehensive multidomain clustering studies have significantly advanced our understanding of PD heterogeneity. By defining phenotypic profiles at a static baseline, standard distance-based clustering approaches have successfully identified subgroups with distinctly divergent clinical outcomes, such as the fast-progressing "diffuse malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015; @fereshtehnejadClinicalCriteriaSubtyping2017; @velucci2025nonmotor]. Notably, this same temporal approach is frequently mirrored even in studies utilizing advanced machine learning frameworks [@markelloMultimodalPhenotypicAxes2021]: phenotypic classes are established cross-sectionally, and longitudinal follow-up is only used post hoc to observe the progression of these fixed groups. Conversely, approaches that explicitly subtype patients based on progression rates have demonstrated the immense prognostic value of temporal data [@faghriPredictingOnsetProgression2018]. Yet, these machine learning methods often compress longitudinal follow-up into static summary vectors, obscuring the dynamic shape of the disease course. 

To capture actual symptom evolution, univariate latent class models have mapped individual domains over time, such as cognition [@pourzinal2024profiling], autonomic function [@chen2021orthostatic], and motor severity [@he2023motor]. Evaluating these axes in isolation limits our understanding of PD as a multi-system disorder. To bridge this gap, our research undertakes an exploratory investigation using a multivariate longitudinal Latent Class Mixed Model (LCMM). Rather than assuming equal contribution across all symptom domains, this multi-dimensional approach allows the natural variance of the cohort to dictate the clustering, revealing which clinical scales predominantly drive longitudinal heterogeneity. 

Finally, we relate these emergent clinical phenotypes to targeted biological metrics. Specifically, further relate these phenotypes to structural MRI, as atrophy patterns track both clinical severity and trans-neuronal spread of PD pathology [@zeighamiNetworkStructureBrain2015]. As highlighted in a recent review [@filideiParkinsonsDiseaseClinical2025], bridging data-driven subtypes and biological correlates is a critical priority to ensure clinical classifications reflect true pathophysiological differences

<br/><br/>

# Results

<br/><br/>

```{figure} figure.png
:name: figure-main
:alt: Multi-panel figure supporting the main findings

\
**A–D:** Observed mean trajectories of the 4 class indicator variables that defined the `multlcmm` model - Class 1 is the stable high burden group, Class 2 is stable low burden group and Class 3 is the increasing burden group.
\
**E:** Boxplots of subject-specific annual change rates (random slopes from LMM) for regions showing nominal differences between Class 2 (stable reference, green) and Class 3 (orange). Positive slopes = expansion, negative slopes = atrophy.  Red dashed line = no change. Only the inferior lateral ventricle difference survived false discovery rate correction (q<0.10).
\
**F:** Class-specific SHAP feature importance profiles. Bars indicate the mean absolute SHAP values, representing the global contribution of baseline features to XGBoost class assignment.
```

<br/><br/>

## Latent Class Identification and Trajectories
Multivariate LCMM identified a three-class solution as optimal based on the lowest BIC, mean posterior probabilities, class size, and relative entropy criteria [Table 1](#main-model-selection), full methodological details are provided in [Supp.Methodology](#supp-methodology) : a Stable High-Burden class (Class 1, n = 173, 20.2%), a Low-Burden class (Class 2, n = 568, 66.4%), and an Increasing-Burden class (Class 3, n = 114, 13.3%). Observed mean trajectories are shown in [Figure 1 (A-D)](#figure-main). Class 1 maintained stably elevated REM Sleep Behavior Disorder Screening Questionnaire (RBDSQ) scores above the diagnostic cutoff (≥5) throughout follow-up; Class 2 remained consistently below the cutoff; Class 3 crossed the threshold at approximately Year 2 and approached Class 1 levels by Year 5. Montreal Cognitive Assessment (MoCA) declined in Class 3 from Year 3–4 onward while remaining stable in Classes 1 and 2; orthostatic systolic blood pressure drop (ΔSBP) and Movement Disorder Society Unified Parkinson's Disease Rating Scale Part III (UPDRS Part III) increased progressively across all classes, most prominently in Class 1. RBDSQ accounted for the largest proportion of between-class variance (39.1%), substantially exceeding ΔSBP (0.74%), MoCA (0.50%), and UPDRS-III (0.20%); the multivariate class structure showed strong agreement with the RBDSQ-only solution (ARI = 0.96; Cramér's V = 0.95) [Table S1](#supp-rbd-model-selection-2dp) [Table S2](#supp-rbd-class-comparison). Baseline characteristics are descriped in [Supp.Baseline](#supp-baseline).


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
To ensure computation stability and numerical convergence, predictors were structured into MRI regional volumes (N = 474) and biofluid/clinical biomarkers (N = 240), with age, sex, and education as covariates. ORs for MRI metrics were standardized per standard deviation, as raw normalized brain volumes (often <0.1% of eTIV) produce ORs that are either extreme or indistinguishable from 1.0; clinical and biofluid markers remain on their raw scales. UPSIT, Specific Binding Ratios (SBR), and APOE were evaluated at their maximum available sample sizes, with the restricted combined model (N = 240) as a sensitivity analysis.

To validate the clinical relevance, we compared baseline UPSIT scores as an external benchmark. Olfactory function was significantly lower in both the high-burden ($p$ = .005) and increasing-burden ($p$ = .002) groups [Table 2](#multinomial-reg-table). Aligning with the "Diffuse Malignant" phenotype [@fereshtehnejadNewClinicalSubtypes2015] and confirming the model's capacity to capture established biological patterns of PD heterogeneity.


## Longitudinal Structural Change
Longitudinal analysis revealed divergent temporal dynamics: while the high-burden class exhibited pronounced volumetric differences at baseline, the increasing-burden group was characterized by accelerated rates of structural change [Figure 1 (E)](#figure-main). We observed broad trends of accelerated ventricular and choroid plexus expansion in the latter; however, under rigorous False Discovery Rate correction (n = 382), only the inferior lateral ventricle slope survived the significance threshold ($q$ < .10) [Table 3](#lmm-slope-table).

<br/><br/>


```{csv-table} Multinomial Logistic Regression on Baseline Biomarkers (Reference: Class 2). **Bolded** values indicate $p < 0.05$. ORs for MRI-derived features are standardized, other ORs are given in terms of raw units. Age and Sex were included as controls in all regressions, Education was additionally controlled for in all regressions except for the one carried out on the MRI-derived features.
:header-rows: 1
:name: multinomial-reg-table
:align: center

"Predictor","N","Odds Ratio<br>(Class 1)","p-value<br>(Class 1)","Odds Ratio<br>(Class 3)","p-value<br>(Class 3)"
"Sex (Male=1)","855","**3.278**","**<.001**","1.633","0.093"
"Education (Years)","855","0.975","0.471","0.984","0.718"
"Age","855","1.011","0.432","1.005","0.775"
"Striatal SBR Caudate (full)","846","0.436","0.075","0.550","0.323"
"Striatal SBR Putamen (full)","846","0.767","0.579","0.249","0.054"
"UPSIT (full)","834","**0.963**","**0.005**","**0.948**","**0.002**"
"CSF-SAA (Positive=1) (full)","796","1.535","0.208","5.983","0.109"
"CSF $\alpha$-synuclein","240","0.999","0.130","1.000","0.490"
"CSF phosphorylated-$\tau$","240","1.117","0.203","1.062","0.345"
"CSF amyloid-$\beta$","240","0.999","0.630","0.999","0.248"
"UPSIT (overlap)","240","0.966","0.233","0.954","0.076"
"Serum NfL Chain","240","1.043","0.167","0.978","0.560"
"Striatal SBR Caudate (overlap)","240","0.375","0.425","1.089","0.941"
"Striatal SBR Putamen (overlap)","240","0.163","0.222","0.098","0.092"
"APOE $\epsilon$4 (Carrier=1)","240","0.911","0.875","0.744","0.575"
"Thalamus","474","**0.596**","**0.026**","0.868","0.527"
"Putamen","474","**0.613**","**0.023**","0.899","0.630"
"Caudate","474","1.348","0.133","0.845","0.393"
"Pallidum","474","1.147","0.478","**1.511**","**0.033**"
"Insula","474","1.361","0.196","0.911","0.654"
"Amygdala","474","1.000","0.974","0.924","0.732"
"Hippocampus","474","1.537","0.058","1.036","0.903"
"Inferior Temporal","474","0.954","0.807","1.057","0.776"
"Para-Hippocampal","474","0.737","0.090","1.015","0.933"
"Posterior Cingulate","474","1.048","0.825","0.863","0.494"
"Superior Parietal","474","1.150","0.507","0.903","0.669"
"Middle Frontal","474","0.863","0.386","1.024","0.903"
"Anterior Cingulate","474","1.443","0.135","1.215","0.404"
```

<br/><br/>

```{csv-table} Linear Mixed Models on MRI Volume and Cortical Thickness Trajectories (Reference: Class 2). P-values are shown for the differences in atrophy/expansion between classes. Unadjusted $p < 0.05$ results are indicated in **bold**. None of the results survived FDR correction. Age and sex were controlled for in all models.
:header-rows: 1
:name: lmm-slope-table
:align: center

"Region","p-value<br>(Class 1)","FDR q<0.10<br>(Class 1)","p-value<br>(Class 3)","FDR q<0.10<br>(Class 3)"
"Thalamus","0.950","0.990","0.835","0.879"
"Caudate","0.684","0.808","**0.036**","0.204"
"Putamen","0.433","0.618","0.306","0.680"
"Hippocampus","0.561","0.748","0.090","0.258"
"Choroid Plexus","0.990","0.990","**0.044**","0.204"
"Pallidum","0.271","0.542","0.990","0.990"
"Lateral Ventricle","0.393","0.618","**0.020**","0.202"
"Inf. Lat. Ventricle","0.054","0.180","**0.009**","0.177"
"Cerebral White Matter","0.799","0.888","0.430","0.782"
"WM Hypointensities","0.067","0.192","0.378","0.756"
"Amygdala","**0.010**","0.120","0.768","0.853"
"Insula","0.414","0.618","0.757","0.853"
"Inferior Temporal","**0.012**","0.120","0.470","0.783"
"Para-Hippocampal","**0.028**","0.180","0.651","0.853"
"Posterior Cingulate","0.148","0.330","0.069","0.231"
"Superior Parietal","**0.047**","0.180","0.145","0.363"
"Rostral Middle Frontal","0.686","0.808","0.701","0.853"
"Caudal Middle Frontal","**0.049**","0.180","0.512","0.788"
"Rostral Anterior Cingulate","0.340","0.618","0.751","0.853"
"Caudal Anterior Cingulate","0.116","0.291","0.051","0.204"
```

<br/><br/>

## Early-Stage Subtype Prediction
The XGBoost model achieved an AUC of 0.88 and cross-validated balanced accuracy of 0.73. Baseline RBDSQ was the single most discriminative predictor of class membership by both split frequency and information gain, tripling the next-ranked feature. Class-specific SHAP analysis [Figure 1 (F)](#figure-main) revealed that Class 1 was overwhelmingly driven by RBD severity; Class 2 showed a more distributed profile led by RBD, olfactory function, autonomic dysfunction, and anxiety; and Class 3 had the broadest SHAP profile with postural instability and dopaminergic imaging as notable contributors, consistent with its lower classification accuracy (F1 = 0.36). CSF α-synuclein SAA ranked prominently in native tree metrics but not in SHAP values, reflecting population-level rather than patient-level discriminative utility. 

<br/><br/>

# Discussion
While RBD is a well-established prognostic marker, it is typically deployed as a static or binary baseline feature [@velucci2025nonmotor; @liuLongitudinalChangesParkinsons2021]. Our findings highlight its dynamic evolution: longitudinal RBDSQ trajectories contributed the majority of variance, driving the latent class structure and demonstrating that RBD-related heterogeneity persists well beyond the prodromal stage.

This longitudinal approach yields markedly different prognostic insights compared to baseline clustering. For instance, the highly cited diffuse/malignant phenotype [@fereshtehnejadNewClinicalSubtypes2015] couples a wide breadth of severe baseline symptoms with rapid global progression. While our Class 1 shares this severe baseline multi-domain profile [Supp.Baseline](#supp-baseline) and resembles the RBD+ cluster [@velucci2025nonmotor], its symptom progression was not exclusively the most rapid. Instead, Class 3 demonstrated the steepest multi-domain deterioration despite much milder baseline symptoms. Because our multivariate LCMM models domain-specific trajectories rather than collapsing metrics into a single composite score, these results suggests that initial symptom burden and progression rate represent distinct, decoupled dimensions of PD heterogeneity.

Our trajectory-derived subtypes align more closely with longitudinal RBD progression studies than with traditional baseline clustering. Our data-driven classes mirror the a priori groups defined by @Ye2022RBDProgressionPD. Their largest group, the non-RBD-stable phenotype, matches our low-burden stable class (Class 2). Our Class 3 strongly aligns with their "late-RBD" group (12.1% of their cohort), showing a late-emerging probable RBD trajectory that crosses the clinical threshold around Year 2. This transitional, high-risk phenotype exhibits baseline olfactory impairment and orthostatic hypotension [@y.saitohImpactLateonsetREM]. Our high-burden Class 1 likely represents a combination of their pRBD-stable and pRBD-reversion phenotypes—supported by a slight reversion in Class 1's RBDSQ  during Years 4 and 5.

Finally, while we did not directly measure α-synuclein pathology, these distinct trajectories tentatively align with proposed models of Lewy body spatial progression. Class 1's early concurrent triad of RBD, autonomic, and olfactory dysfunction resembles a "body-first" or brainstem-early trajectory [@borghammerBrainFirstGutFirstParkinsons2019; @mastenbroekDiseaseProgressionModelling2024]. Conversely, Class 3's post-motor RBD onset and rapid cognitive decline suggests a "brain-first" origin with delayed, steep brainstem involvement. Class 2, persistently lacking RBD, may represent a phenotype where pathology remains temporarily confined to olfactory regions. Ultimately, the longitudinal timing of RBD expression appears to carry critical, albeit interpretive, pathophysiological weight.

Smaller baseline thalamus and putamen volumes predict membership in the high-burden class relative to the low-burden stable class, matching literature identifying these regions as structural markers for pRBD and aggressive PD [@boucettaStructuralBrainAlterations2016; @ellmoreReducedVolumePutamen2010; @rahayelBrainAtrophyParkinsons2019; @salsoneReducedThalamicVolume2014]. Conversely, the high-burden and increasing-burden classes predicted larger baseline volumes in the hippocampus and pallidum, respectively. While pRBD is sometimes associated with volume loss in these structures [@limNeuralSubstratesRapid2016], morphometric analysis demonstrates that PD patients without RBD exhibit significant localized surface shape contraction in both the hippocampus and pallidum [@rahayelBrainAtrophyParkinsons2019]. Because this low-burden stable population serves as our statistical reference group, we hypothesize that their localized shape deformations distort automated boundary detection, artificially manifesting as relative hypertrophy in our tracking classes.

Longitudinally, neurodegeneration tracks clinical evolution; the increasing-burden class displays accelerated ventricular and choroid plexus expansion — a marker of progressive central atrophy and altered cerebrospinal fluid dynamics linked to impaired glymphatic clearance [@he2023motor]—alongside slower caudate atrophy relative to the low-burden stable class, highlighting distinct subcortical phenotypes requiring future whole-brain context.

<br/><br/>

$^\dagger$ These authors contributed equally to this work.

<br/><br/>







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
Analyses were performed in R (v4.5.3) and Python (v3.12.13). `multlcmm` function in the R package `lcmm` [@proustlima2017lcmm] was applied for trajectory analysis. This approach follows the rationale of group-based trajectory modeling [@naginGroupBasedTrajectory2010], allowing several longitudinal markers measured on different clinical scales, to inform a common underlying latent disease process while accounting for marker-specific measurement relationships. Latent classes and individual membership probabilities were estimated within a maximum-likelihood framework, providing asymptotically unbiased parameter estimates under a missing-at-random assumption. Follow-up time since baseline, measured in years, was used as the time indicator. The following steps were performed to optimize the analysis:

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


## Limitations, Strengths, and Future Directions

### Cohort and Clinical Measurement Constraints
Several limitations should be considered when interpreting these findings. First, while the PPMI dataset provides an unprecedented de novo PD cohort, it represents a highly educated, predominantly white demographic that excludes atypical parkinsonism or early dementia, limiting immediate generalizability to broader clinical populations. Clinically, REM sleep behavior disorder was assessed via the RBDSQ rather than polysomnography, reflecting probable symptom trajectories (pRBD) rather than confirmed diagnoses. Additionally, simplifying the multisystem complexity of PD by representing each clinical domain with a single scale, alongside collecting data post-diagnosis, prevents us from inferring the exact temporal order of early pathological events or $\alpha$-synuclein propagation.

### Statistical Modeling, Missing Data, and Distal Outcomes
Second, the use of Latent Class Mixed Models (LCMM) inherently assumes discrete categorical subpopulations within a continuous neurodegenerative spectrum. While LCMM natively handles missing longitudinal data, our secondary covariate analysis evaluates baseline variables as class predictors using a bias-adjusted 3-step method (`externVar()`). This framework highlights associations rather than strict causality and is currently restricted to a complete-case subset with overlapping biomarker data. To eliminate missing variable bias and leverage the full $N = 855$ cohort for secondary inference, future work will implement multiple imputation for these baseline biomarkers. Furthermore, while `externVar()` was deployed here exclusively for baseline predictors, it can also be used in future iterations of this work to relate trajectory classes directly to distal clinical outcomes, such as reaching Hoehn & Yahr Stage 3, mild cognitive impairment (MCI), and dementia.

### Neuroimaging Feature Selection and Pipeline Consistency
Third, our structural MRI analysis was restricted to a targeted subset of mostly subcortical regional volumes. This restricted feature selection was a strict statistical necessity: the parameter-heavy, bias-adjusted 3-step method introduces severe convergence issues if overloaded with variables, constraining our initial model and leaving broader cortical alterations unexplored. To resolve this and expand our feature space into cortical thickness and broader regional volumes, future work will integrate a wider array of cortical metrics. To ensure strict within-subject consistency across these expanded longitudinal metrics, future iterations will transition from standard automated segmentation to a dedicated longitudinal pipeline utilizing FastSurfer with Surf-Recon, contingent on sufficient computational resources.

### Study Strengths
Despite these limitations, our longitudinal multidomain approach successfully identifies progression phenotypes based on within-person change rather than static baseline severity alone. The robust associations demonstrating clear alignment between these latent trajectory classes and underlying clinical, biomarker, and MRI features strongly support their physiological relevance to dissecting PD heterogeneity.


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
LMM Predicted Trajectories, for regions where nominal differences were found between Class 2 and Class 3
```{image} ./s4.png
:name: lmm-predicty
:align: center
:width: 100%
```

(supp-roc)=
### Figure S2
ROC curves for one-vs-rest on the test set
```{image} ./s6.png
:name: supp-roc
:align: center
:width: 80%

```


(supp-baseline)=
### Baseline Characteristics
Baseline characteristics across the three classes were compared using the Kruskal–Wallis test for continuous variables. For categorical variables, the chi-square test was used by default; when expected cell frequencies were small (any expected count < 1, or more than 20% of cells with an expected count < 5), an exact test was applied instead. Specifically, Fisher's exact test was used for 2×2 tables and a Monte Carlo–based Fisher's exact test for larger R×C tables. Pairwise comparisons between classes were performed using Dunn's test for continuous variables and the same chi-square/exact-test procedure for categorical variables, with Benjamini–Hochberg false discovery rate (FDR) correction applied across the pairwise comparisons within each variable. Continuous variables are expressed as mean ± standard deviation (SD), and categorical variables as number (percentage).

Baseline clinical characteristics showed that the three classes did not differ significantly in age at diagnosis or symptom onset, disease duration, education, Hoehn-Yahr stage, dominant side of symptom onset, motor severity (UPDRS Part III), global cognition (MoCA), or the battery of neuropsychological tests. Class 1 carried the heaviest overall disease burden, with the highest RBDSQ (8.65±1.83), SCOPA-AUT (14.33±7.49), STAI (66.69±18.46), GDS (2.78±2.58), ESS (6.42±3.83), QUIP (0.37±0.80), and MDS-UPDRS Part I (8.28±5.12), all significantly exceeding Class 2 (p < 0.05). Olfaction was impaired (UPSIT 20.33±7.76, p < 0.001 vs Class 2), and orthostatic blood pressure drop was elevated (ΔSBP 6.61±13.64, p < 0.05 vs Class 2), however these two features were most severe in Class 3. This group also had the greatest motor and functional impact, with the highest MDS-UPDRS Part II, PIGD score, lowest ADL score, and a marked male predominance (80.9% vs 61.4% in Class 2, p < 0.0001). Class 2 repesented the low-burden group, with mildest non-motor, motor and functional symptoms, serving as the reference against which the other two groups were defined. Class 3 occupied an intermediate position overall but carried a distinctive early signature. It showed the worst olfactory function (UPSIT 19.85±6.24, p < 0.001 vs Class 2), greater orthostatic blood pressure drop (ΔSBP 6.82±15.07), higher SCOPA-AUT (11.43±6.43, p = 0.002 vs Class 2), and elevated MDS-UPDRS Part I (6.29±4.04) and Part II (6.16±3.72) compared to Class 2, yet without prominent anxiety, depression, or sleepiness. This combination of hyposmia and emerging autonomic dysfunction distinguished Class 3 from the otherwise similar low-burden Class 2 at baseline.

Baseline biomarker and neuroimaging profiles were largely comparable across classes. CSF Aβ, total α-synuclein, phosphorylated tau, total tau, serum NfL, and APOE ε4 burden showed no significant differences. Serum urate differed modestly overall (p = 0.034), but pairwise comparisons were not significant. CSF α-synuclein seed amplification assay (SAA) status differed among classes, with Class 2 showing a higher proportion of SAA-negative cases and Classes 1 and 3 exhibiting higher SAA-positive rates (11.7% vs 5.0% and 4.6%). DATSCAN age-/sex-expected lowest putamen ratio was similar across groups, indicating comparable baseline nigrostriatal dopaminergic deficits. MRI volumetric analyses revealed several nominal overall differences, including thalamus (p = 0.005), putamen (p = 0.036), nucleus accumbens (p = 0.009), third ventricle (p = 0.024), total gray matter (p = 0.008), subcortical gray matter (p = 0.022), and cortex volume (p = 0.009), though pairwise comparisons did not survive FDR correction. Class 2 generally showed numerically larger brain volumes. Cortical thickness measures did not differ significantly across classes.

Detailed values for each variable are provided in the table below.


```{figure} ./bl1.png
:name: baseline-1
:align: center
:width: 100%
```


```{figure} ./bl2.png
:name: baseline-2
:align: center
:width: 100%
```

```{figure} ./bl3.png
:name: baseline-3
:align: center
:width: 100%
```

```{figure} ./bl4.png
:name: baseline-4
:align: center
:width: 100%
```

```{figure} ./bl5.png
:name: baseline-5
:align: center
:width: 100%
```


```{figure} ./bl6.png
:name: baseline-6
:align: center
:width: 100%
```

