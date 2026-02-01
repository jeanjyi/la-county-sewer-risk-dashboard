# Sewer Pipe Failure Prediction - Research Findings

This document compiles research findings specifically about **sewer/wastewater pipe** condition prediction to support methodology decisions for the SSO (Sanitary Sewer Overflow) predictive model.

---

## Executive Summary

### Recommended Approach

**Model:** Binary logistic regression (Fail/No-Fail) using pipe age as primary predictor

**Weighting:** 80% Age / 20% Material

**Expected Accuracy:** 65-75%

### Evidence Supporting This Approach

**Age as dominant predictor:**
- Dallas empirical study: Age scored 100% importance vs. Material at 25% (4:1 ratio)
- Isfahan study: Age ranked #1 at 38% importance
- Review of 16 studies: Age consistently the most significant variable
- LASAN explicitly lists "pipe age and material" as primary prioritization factors

**Age-based prediction when CCTV unavailable:**
- LASAN's RAMS algorithm "predicts system condition when condition data is not available" using "age, material type, and other attribute information"
- Oakland's Info360 methodology: "Defect Rating is primary (if no CCTV use Age)"

**Logistic regression validity:**
- Published accuracy: 65-81% across multiple studies
- Most commonly used method in sewer condition prediction literature
- Appropriate for available data quality; more complex methods (ANN, SVM) require larger datasets

**Real-world alignment:**
- Methodology matches actual municipal practice in Los Angeles and Oakland
- Both cities under regulatory oversight (State Water Board, EPA Consent Decree)

---

## Paper 1: Malek Mohammadi et al. (2019)
**Title:** Sewer Pipes Condition Prediction Models: A State-of-the-Art Review
**Journal:** Infrastructures (MDPI)
**File:** `Malek_Mohammadi_2019_Sewer_Condition_Review.pdf`

### Overview
Comprehensive review of 16 sewer condition prediction models from 2001-2019. This is a foundational reference for understanding the state of sewer pipe failure prediction research.

### Key Factors Affecting Sewer Deterioration

| Category | Factors |
|----------|---------|
| **Physical** | Age, Material, Diameter, Length, Slope, Depth |
| **Environmental** | Soil Type, Groundwater Level, Location (traffic load) |
| **Operational** | Previous failures, Flow characteristics, Maintenance history |

### Sewer Failure Modes
1. **Structural Defects:** Cracks, fractures, deformation, corrosion, joint displacement
2. **Operational Defects:** Root intrusion, deposits (grease, debris), infiltration
3. **Hydraulic Capacity:** Related to pipe sizing and flow demands

### Model Types Reviewed
- **Logistic Regression** - Most commonly used; rated "Good" for individual pipe analysis
- **Markov Chain** - Better for network-level deterioration over time
- **Linear Regression** - Used in some studies but less common
- **Machine Learning** - Neural networks, random forests emerging

### Significant Variables Across Studies

Based on the review of 16 studies, these variables consistently appeared as significant predictors:

| Variable | Frequency of Significance |
|----------|---------------------------|
| **Age** | Most studies (consistently significant) |
| **Material** | Most studies |
| **Diameter** | Common |
| **Length** | Common |
| **Slope** | Several studies |
| **Depth** | Several studies |
| **Soil Type** | Where data available |

### Model Performance Benchmarks

| Study | Model Type | Accuracy |
|-------|------------|----------|
| Ariaratnam et al. (2001) | Logistic Regression | 65% |
| Chughtai & Zayed (2008) | Logistic Regression | 72% |
| Malek Mohammadi et al. (2019) | Binary Logistic Regression | **81%** |

### Key Insights for Our Model

1. **Age is consistently the strongest predictor** - Appears significant in virtually all studies
2. **Material matters significantly** - Different materials have different deterioration patterns
3. **Logistic regression is appropriate** - Well-validated for sewer condition prediction
4. **65-81% accuracy is realistic** - Our model should target this range
5. **Binary classification works well** - Fail/No-Fail prediction is common approach

### Limitations Noted
- Data availability varies significantly
- Many studies are location-specific (may not generalize)
- Condition assessment standards differ between studies
- Some factors (soil type, groundwater) often unavailable

---

## Summary Table: Factor Importance for Sewer Pipes

| Factor | Evidence Level | Notes |
|--------|---------------|-------|
| Age | **Strong** | Consistently significant across all studies |
| Material | **Strong** | Significant in most studies |
| Diameter | Moderate | Significant in several studies |
| Length | Moderate | Significant in several studies |
| Slope | Moderate | Where available, often significant |
| Depth | Moderate | Environmental exposure factor |
| Soil Type | Variable | Significant when data available |
| Previous Failures | Variable | Strong predictor when historical data exists |

---

## Paper 2: Atambo, Najafi & Kaushal (2022)
**Title:** Development and Comparison of Prediction Models for Sanitary Sewer Pipes Condition Assessment Using Multinomial Logistic Regression and Artificial Neural Network
**Journal:** Sustainability (MDPI)
**File:** `Atambo_2022_Sewer_MLR_ANN.pdf`

### Overview
Empirical study using **real inspection data from City of Dallas Water Utilities**. Developed and compared MLR and ANN models for sewer pipe condition prediction. This is highly valuable because it provides actual quantitative importance rankings.

### Data Source
- City of Dallas Water Utilities GIS database
- CCTV inspection records
- PACP (Pipeline Assessment Certification Program) condition ratings
- 80/20 train/validation split

### Model Accuracy Results

| Model | Accuracy |
|-------|----------|
| Multinomial Logistic Regression (MLR) | **75%** |
| Artificial Neural Network (ANN) | **85%** |

### **CRITICAL: Variable Importance Rankings (Normalized)**

| Variable | Importance | Normalized |
|----------|------------|------------|
| **Age** | Highest | **100%** |
| **Diameter** | Very High | **80%** |
| **Slope** | High | 62% |
| **Length** | High | 62% |
| Flow | Moderate | 60% |
| pH | Moderate | 40% |
| Corrosivity Steel | Moderate | 38% |
| Soil Type | Moderate | 36% |
| Depth | Moderate | 35% |
| **Pipe Material** | Lower | **25%** |
| Surface Condition | Lower | 22% |
| Corrosivity Concrete | Lower | 20% |

### Statistical Significance (p-values < 0.05)

| Factor | Condition 1 | Condition 2 | Condition 3 | Condition 4 |
|--------|-------------|-------------|-------------|-------------|
| Diameter | **0.001** | **0.000** | 0.199 | **0.008** |
| Age | **0.000** | **0.001** | **0.000** | 0.807 |
| Length | **0.000** | 0.228 | 0.113 | 0.980 |
| Material | 0.503 | **0.025** | **0.001** | 0.280 |

### Key Insights for Our Model

1. **Age is THE dominant factor (100%)** - Not just "important" but the single most important predictor
2. **Material is only 25% importance** - Much lower than Age
3. **Diameter (80%) is more important than Material (25%)**
4. **75-85% accuracy is achievable** with proper modeling
5. Physical factors (Age, Diameter, Slope, Length) outweigh environmental factors

### Implications for Weighting

Based on this study's normalized importance:
- If using just Age + Material: **Age should be ~80%, Material ~20%** (ratio of 100:25 = 4:1)
- Original 60/40 split **underweighted Age** relative to this research

---

## Paper 3: Goodarzi & Vazirian (2024)
**Title:** A machine learning approach for predicting and localizing the failure and damage point in sewer networks due to pipe properties
**Journal:** Journal of Water and Health (IWA Publishing)
**File:** `Goodarzi_2024_SVM_Sewer_Isfahan.pdf`

### Overview
Machine learning study using **Support Vector Machine (SVM)** to predict sewer pipe failures in Isfahan, Iran. The network is 50 years old with 3,500 km of pipes. Unique focus on manhole proximity effects.

### Data Source
- Isfahan, Iran sewer network
- SCADA system failure reports (2014-2015)
- 851 failure incidents analyzed
- Pipe types: Concrete, diameter 250mm
- Pipe ages: 40-55 years

### Model Accuracy Results

| Metric | Value |
|--------|-------|
| SVM Accuracy | **84-86%** |
| AUC (Area Under ROC Curve) | **0.905** |
| Sensitivity | 88% |
| Specificity | 80% |

### **Variable Importance Rankings (Figure 14)**

| Variable | Importance |
|----------|------------|
| **Age** | **38%** |
| **Depth** | 25% |
| **Length** | 20% |
| **Diameter** | 10% |
| Slope | 7% |

### Key Findings from Literature Review

The paper cites an **Edmonton logistic regression study** (referenced as Guo et al. 2022):
- Age, diameter, and type of sewage systems = **significant impact** on failure
- Depth of burial = **NOT significant**
- Pipe material type = **NOT significant**

Also cites Gedam et al. (2016):
- "Pipe age is very significant to the model but the depth is not of significant impact"

### Failure Distribution by Age (Figure 11)

| Pipe Age | Number of Failures |
|----------|-------------------|
| 0-10 years | 9 |
| 10-20 years | 21 |
| 20-30 years | 27 |
| 30-40 years | 56 |
| **40-50 years** | **393** |
| **50-60 years** | **345** |

This shows exponential increase in failures after 40 years.

### Key Insights for Our Model

1. **Age again confirmed as most important factor (38%)** - consistent across studies
2. **Material was NOT a variable** - all pipes were concrete in this study
3. **Depth was NOT significant** in referenced Edmonton study
4. **84-86% accuracy** achievable with SVM
5. **Failure rate increases dramatically after 40 years**

### Implications

- Further confirms Age as the dominant predictor
- Suggests depth and material may be less important than previously thought
- Provides international validation (Iran) beyond US studies

---

## Updated Summary: Factor Importance for Sewer Pipes

| Factor | Evidence Level | Atambo Dallas (2022) | Goodarzi Isfahan (2024) | Notes |
|--------|---------------|----------------------|-------------------------|-------|
| **Age** | **Very Strong** | **100%** | **38%** | #1 in both studies |
| Diameter | Strong | 80% | 10% | Varies by study |
| Length | Strong | 62% | 20% | Consistent |
| Depth | Mixed | 35% | 25% | Edmonton study: NOT significant |
| Slope | Moderate | 62% | 7% | Varies by study |
| **Material** | **Mixed** | **25%** | N/A (constant) | Edmonton: NOT significant |
| Soil Type | Moderate | 36% | N/A | When data available |

---

## Paper 4: Latifi et al. (2024)
**Title:** Efficacy of Tree-Based Models for Pipe Failure Prediction and Condition Assessment: A Comprehensive Review
**Journal:** ASCE Journal of Water Resources Planning and Management
**File:** `Latifi_2024_TreeBased_Models_Review.pdf`

### Overview
Comprehensive review from University of Exeter covering tree-based machine learning models (Decision Trees, Random Forest, Gradient Boosting) for **both water AND sewer** pipe failure prediction. Reviews studies from North America and Europe.

### Key Findings

**Model Performance:**
- "Tree-based algorithms outperformed other prevalent models" (ANN, SVM, Bayesian)
- **Random Forest** = most frequently used approach
- Tree-based models achieve comparable or better performance than traditional statistical methods

**Most Important Variables (from reviewed studies):**
- **Pipe material**
- **Number of previous bursts/failures**
- **Age**

Quote: "Pipe material, number of previous bursts and age were shown to be the most important attributes."

**Sewer-Specific Findings:**
- For sewer condition prediction using static data: "the main predictive variables of the model were **age, length, and diameter**"
- CCTV-based models can achieve high accuracy for condition classification

### Model Comparison Summary

| Model Type | Strengths | Best For |
|------------|-----------|----------|
| Random Forest | Robust, handles imbalanced data | General failure prediction |
| Gradient Boosting (XGB) | High accuracy, handles complex patterns | When accuracy is priority |
| Logistic Regression | Simple, interpretable | When explainability needed |
| ANN | Captures nonlinear relationships | Large datasets |

### Implications for Our Model

1. **Age confirmed as key predictor** - across multiple tree-based model studies
2. **Previous failures** matter significantly - historical data is valuable
3. **Random Forest and XGBoost** outperform simpler models when data is available
4. For simpler approaches, **logistic regression remains valid** and interpretable

---

## FINAL CROSS-STUDY CONSENSUS

### Variable Importance Summary (4 Papers)

| Factor | Paper 1 (Review) | Paper 2 (Dallas) | Paper 3 (Isfahan) | Paper 4 (Review) | **Consensus** |
|--------|------------------|------------------|-------------------|------------------|---------------|
| **Age** | Most studies | **100%** | **38%** | Key variable | **#1 PREDICTOR** |
| Material | Most studies | 25% | N/A | Important | Moderate |
| Diameter | Common | 80% | 10% | Important | Moderate-High |
| Length | Common | 62% | 20% | Key (sewer) | Moderate |
| Previous Failures | Variable | N/A | N/A | Key variable | **HIGH when available** |
| Depth | Several | 35% | 25% | Variable | Mixed |

### Model Accuracy Benchmarks

| Method | Typical Accuracy | Source |
|--------|------------------|--------|
| Logistic Regression | 65-81% | Multiple studies |
| Neural Network (ANN) | 75-85% | Dallas study |
| Support Vector Machine | 84-86% | Isfahan study |
| Random Forest | 80%+ (AUC) | Multiple studies |

### Key Takeaways for SSO Model

1. **Age should be weighted heavily** - consistently #1 across all studies
2. **Material matters but less than Age** - ratio approximately 4:1 (Age:Material)
3. **75-85% accuracy is realistic and achievable**
4. **Simple logistic regression is valid** - don't need complex ML for good results
5. **Previous failure history** is valuable if available in SSO data

---

## Commercial Tool Case Study: City of Oakland & Autodesk Info360 Asset

**Source:** Autodesk University 2023 Presentation
**Presenters:** Wen Chen, PhD, PE (City of Oakland Public Works) & Martha Nunez (Autodesk)
**File:** `ClassPresentation-CI601629-Chen-AU2023_final.pdf`

### Overview

Real-world implementation case study showing how the City of Oakland operationalized sewer risk assessment using Autodesk Info360 Asset. Provides validated weighting schemes from an actual municipal utility under EPA Consent Decree.

### Oakland Sewer System Context

| Metric | Value |
|--------|-------|
| System Size | ~1,000 miles (934 miles gravity main) |
| Pump Stations | 11 |
| Sewer Connections | 100,000+ |
| Population Served | 430,000 |
| Oldest Pipe | **1852** (170+ years old) |
| Average Service Life | 50+ years |
| Annual SSOs | 100+ |
| Regulatory Status | EPA Consent Decree (2014-2035) |

### Consent Decree Requirements (Annual)

- Rehabilitate 13 miles of pipelines & maintenance holes
- Inspect/Assess 92 miles via CCTV
- Root control 50 miles via chemical treatment
- Manage sewer lateral connections

### Oakland's Risk Framework

**Risk = LOF × COF** (multiplicative, 50/50 weighting)

Risk grades: Negligible → Low → Medium → High → Extreme

---

### Likelihood of Failure (LOF) Weighting Scheme

| Category | Weight | Components | Rating Logic |
|----------|--------|------------|--------------|
| **Structural Failure** | **44.45%** | PACP Structural Peak Score, Installation Year/Rehab Year | Defect rating is primary; **if no CCTV, use Age** |
| **Maintenance Failure** | **33.33%** | PACP O&M Peak Score, Roots/Grease Observed During Cleaning, Debris Observed During Cleaning, SSO Occurrences at Pipe Locations, Cleaning Frequency | Maximum score used from all 4 factors |
| **Hydraulic Capacity Failure** | **22.22%** | Modeled Capacity - Identified Restrictions (d/D ratio) | Modeled capacity restrictions is primary factor |

### LOF Scoring Criteria Detail

**Installation Year (Age) Scoring:**

| Score | Installation Year | Interpretation |
|-------|-------------------|----------------|
| 1 | > 1990 | Newest (lowest risk) |
| 2 | 1971 - 1990 | Moderate age |
| 3 | 1951 - 1970; or **Unknown** | Older or unknown |
| 4 | ≤ 1950 | Oldest (highest risk) |
| 5 | Not Used | — |

**PACP Structural Score:**

| Score | Condition |
|-------|-----------|
| 0 | Peak Structure Score = 1; No Defects Noted |
| 2 | Peak Structure Score = 2 |
| 3 | Peak Structure Score = 3 |
| 4 | Peak Structure Score = 4 |
| 5 | Peak Structure Score = 5 |

**SSO Occurrences:**

| Score | SSO History |
|-------|-------------|
| 1 | No documented SSOs |
| 4 | 1 SSO |
| 5 | > 1 SSO |

**Cleaning Frequency:**

| Score | Frequency |
|-------|-----------|
| 1 | Not identified for frequent cleaning |
| 2 | 12-month cleaning frequency |
| 3 | 6-month cleaning frequency |
| 4 | 3-month cleaning frequency |
| 5 | Weekly cleaning frequency |

**Hydraulic Capacity (d/D ratio):**

| Score | Capacity |
|-------|----------|
| 1 | ≤ 0.5 (< 50% full) |
| 2 | 0.5 - 0.75 (50% - 75% full) |
| 3 | 0.75 - 1.0 (75% - 100% full) |
| 4 | Surcharge due to Backwater |
| 5 | Surcharge due to Capacity Exceedance |

---

### Consequence of Failure (COF) Weighting Scheme

| Category | Weight | Components | Rating Logic |
|----------|--------|------------|--------------|
| **Potential Spill Volume** | **20%** | Modeled Peak Wet Weather Flow, Estimated Spill Volume Based on Pipe Diameter | Modeled peak flow is primary; if not available, use diameter |
| **Environmental Impact** | **22%** | Proximity to Water Ways (Creeks, FEMA 100-yr Flood Zone, Lakes) | Single factor |
| **Public Exposure** | **23%** | Based on Pedestrian Traffic, Based on Facility (schools, hospitals, etc.) | Maximum score used between both factors |
| **Social Equity** | **23%** | Equity/Investment in Underserved Oakland Communities, Preservation/Enhancement of Existing Cultural/Historical/Natural Resources | Maximum score used between both factors |
| **Emergency Response & Construction Impact** | **12%** | Proximity to Road/Railroad and Easement Access, Difficulty of Repair/Potential Contaminated Soils, Difficulty of Repair/Depth of Pipe | Maximum score used from all 3 factors |

### COF Scoring Criteria Detail

**Potential Spill Volume (by pipe diameter when modeled data unavailable):**

| Score | Pipe Diameter |
|-------|---------------|
| 1 | ≤ 6 in |
| 2 | 7 in - 8 in; Unknown |
| 3 | 9 in - 10 in |
| 4 | 12 in |
| 5 | > 12 in |

**Proximity to Water Ways:**

| Score | Distance |
|-------|----------|
| 1 | Greater than 250 ft from water body or outside FEMA 100-yr Flood Zone |
| 2 | Within FEMA 100-year Flood Zone |
| 3 | Within 100 - 250 ft of water body |
| 4 | Within 50 - 100 ft of water body |
| 5 | Crosses or within 50 ft of water body |

**Pedestrian Traffic:**

| Score | Location |
|-------|----------|
| 1 | Not in proximity |
| 3 | Within 75 - 150 ft of high pedestrian traffic area |
| 4 | Within 25 - 75 ft of high pedestrian traffic area |
| 5 | Intersecting or within 25 ft high pedestrian traffic area |

High-use areas include: Downtown/urban areas, bicycle lanes/trails, Chinatown, East 14th Street Business, Fruitvale Station, BART Stations, Zoo, Lion Creek, Dimond Park, City Slicker Farms

**Facility Proximity:**

| Score | Facility Type |
|-------|---------------|
| 1 | Not in proximity |
| 3 | Within 150 ft of Commercial Area |
| 4 | Within 150 ft of Schools |
| 5 | Within 150 ft of Hospitals, Medical Facilities, Nursing Homes |

**Social Equity (Underserved Communities):**

| Score | Priority Level |
|-------|----------------|
| 1 | Lowest Priority Neighborhood; Area not included in priority neighborhood |
| 2 | Low Priority Neighborhood |
| 3 | Medium Priority Neighborhood |
| 4 | High Priority Neighborhood or Medium Priority Neighborhood and within 1/4 mile proximity to affordable housing |
| 5 | Highest Priority Neighborhood or High Priority Neighborhood and within 1/4 mile proximity to affordable housing |

**Pipe Depth (for emergency response difficulty):**

| Score | Depth |
|-------|-------|
| 1 | < 10 ft; Unknown |
| 3 | 10 ft - 12 ft |
| 4 | 12 ft - 18 ft |
| 5 | > 18 ft |

---

### Key Insight: Age as Fallback for CCTV

Oakland's approach explicitly states: **"Defect Rating is primary (if no CCTV use Age)"**

This validates our model approach:
- Commercial tools like Info360 Asset prioritize CCTV inspection data when available
- When CCTV is unavailable, **Age becomes the primary predictor**
- Our SSO-based model (which lacks CCTV data) correctly relies on Age

### Commercial vs. Our Model Comparison

| Aspect | Commercial Tools (Info360) | Our SSO Model |
|--------|---------------------------|---------------|
| **Primary Input** | CCTV inspection footage | SSO incident records |
| **Question Answered** | "Which pipes have visible defects now?" | "Which pipes likely to fail based on characteristics?" |
| **Data Required** | Physical inspection | Historical records + GIS |
| **Use Case** | Prioritize inspection findings | Predict where to inspect |
| **Age Role** | Fallback when no CCTV | Primary predictor |

**Complementary approaches:** Our model predicts which pipes to inspect; commercial tools interpret inspection results.

### Implementation Notes

**Info360 Asset Capabilities:**
- Cloud-based platform (AWS hosting)
- CCTV Management with NASSCO PACP scoring
- Risk Analysis with customizable LOF/COF components
- Rehab Decision Trees for maintenance prioritization
- ArcGIS Online integration for sharing results

**Oakland's Tech Stack:**
- ArcGIS Online & Apps (digital infrastructure)
- Granite XP/IT Pipes CCTV
- CityWorks platform (service requests, work orders)
- Info360 Asset (risk analysis, rehab planning)

---

## Other Research

### ASCE 2025 Infrastructure Report Card: Wastewater
**Source:** American Society of Civil Engineers
**File:** `ASCE_2025_Wastewater_Report_Card.pdf`

Provides national context for why sewer infrastructure prediction models are needed:

- **Grade: D+** (unchanged from 2021)
- **$69 billion annual funding gap** — only 30% of capital needs being met
- **Collection system failures increased** from 2 to 3.3 per 100 miles of pipe (indicating aging infrastructure impact)
- **SSO rate decreased** from 0.7 to 0.16 per 100 miles (2015→2021)
- **1.87 million miles** of sewer pipe nationally
- **54% of utilities** collecting data but not effectively leveraging it

ASCE recommends: "Asset management must include continuous assessment of the condition of assets and prioritize investment decisions based on a comprehensive suite of data."

### City of Los Angeles SSMP 2025
**Source:** LA Sanitation & Environment (LASAN)
**File:** `LASAN_SSMP_2025.pdf` (102 pages)

Official regulatory document submitted to State Water Resources Control Board. Directly validates our model approach.

#### System Overview
- **6,500 miles** of sewer pipelines
- 15-year CCTV inspection cycle (~500-600 miles/year)
- 220 secondary sewer basins
- 24 primary sewer basins
- ~10,000 Food Service Establishments monitored

#### Condition Assessment Prioritization (Section 8.1.3)

LASAN's methodology explicitly uses these **primary factors**:
- **Spill rate lineal density**
- **Groundwater inflow and infiltration**
- **Pipe age and material**

> *"The City's current condition assessment prioritization methodology considers spill rate lineal density, groundwater inflow and infiltration, pipe age and material as the primary factors for sewer basin condition assessment prioritization."*

#### RAMS Algorithm — Predictive Modeling Without CCTV (Section 8.1.5)

LASAN already uses predictive modeling when inspection data is unavailable:

> *"For purposes of basin planning, LASAN uses a Risk Assessment Management System (RAMS) algorithm to predict system condition when condition data is not available. This algorithm relies on available condition data for pipes in a similar location or with similar characteristics, hydrogen sulfide levels, and age, material type, and other attribute information to predict condition."*

**This is exactly what our model does** — predict failure risk using age and material when CCTV data isn't available.

#### Secondary Basin Prioritization (Section 8.3.2)

For the 220 secondary basins, LASAN uses weighted risk factors:
- **Number of spills per unit length of sewer**
- **Inflow and infiltration**
- **Percentage of known problem material**
- **Age categories**

#### Condition Rating System (A-E)

| Rating | Condition | Action |
|--------|-----------|--------|
| **E** | Emergency | Immediate — failure has occurred or full obstruction |
| **D** | Poor | Near-term rehabilitation, include in WCIP |
| **C** | Fair | Monitor, follow-up inspections |
| **B** | Good | Routine inspection schedule |
| **A** | Excellent | Routine inspection schedule |

#### FOG Program Results

Demonstrates impact of proactive management:
- **Baseline (FY2001):** 290+ FOG-related spills
- **Current:** ~20 FOG-related spills annually
- **Reduction:** >90%

#### Key Validation for Our Project

1. **Age and material are explicitly primary factors** in LASAN's actual methodology
2. **RAMS algorithm precedent** — LA already uses predictive modeling when CCTV unavailable
3. **Spill rate lineal density** — calculable from SSO data (potential enhancement)
4. **Official regulatory document** — submitted to State Water Board, defensible methodology

---

## Material-Specific Failure Mode Analysis

### Overview

During model development, additional research was conducted to understand material-specific failure mechanisms in sewer systems. This research informed the material scoring methodology, which considers multiple failure modes rather than relying solely on empirical failure rates.

**IMPORTANT NOTE:** The following research includes both academic sources and industry knowledge. Material scores in the model are informed estimates based on known failure mechanisms, not rigorous empirical calculations from failure rate data. This approach prioritizes defensibility and transparency for a non-technical audience.

---

### Failure Modes Analyzed

Six primary failure modes were considered for material risk scoring:

1. **H2S Corrosion** - Hydrogen sulfide (produced by anaerobic bacteria) converts to sulfuric acid, corroding pipe materials
2. **Root Intrusion** - Tree roots penetrate joints and cracks seeking water and nutrients
3. **Structural Integrity** - Inherent strength and brittleness of the material
4. **Joint Degradation** - Deterioration of pipe connections over time
5. **Surface Roughness** - Internal surface characteristics affecting flow and debris accumulation
6. **Longevity** - Expected service life under normal conditions

---

### H2S Corrosion in Sewer Systems

**Key Finding:** Concrete and cast iron are highly vulnerable to hydrogen sulfide corrosion; PVC and HDPE are immune.

**Corrosion Rates (cited in industry literature):**
- **Concrete pipes:** 1-10mm per year in high H2S environments
- **Cast iron pipes:** Severe corrosion, particularly in anaerobic conditions
- **Clay (VCP):** H2S resistant due to vitrification process
- **PVC/HDPE:** Chemically inert, no H2S corrosion

**Mechanism:**
1. Anaerobic bacteria in sewage produce H2S gas
2. H2S gas accumulates in crown of pipe
3. Aerobic bacteria (Thiobacillus) convert H2S to sulfuric acid
4. Sulfuric acid attacks concrete and iron surfaces

**Citations:**
- Multiple wastewater engineering references cite 1-10mm/year for concrete corrosion
- EPA guidance documents on sewer system management acknowledge H2S as primary deterioration mechanism

---

### Root Intrusion

**Key Finding:** Root intrusion accounts for >50% of sewer blockages and is particularly severe in VCP pipes with old joint systems.

**Material Vulnerability:**
- **VCP (High vulnerability):** Old bell-and-spigot joints with oakum/cement sealing fail after 25-30 years, creating entry points
- **Concrete (Moderate-High):** Joints and cracks provide entry points
- **Cast Iron (Moderate):** Old mechanical joints can separate
- **PVC/HDPE (Low):** Modern elastomeric gasket joints resist root penetration

**VCP Joint Paradox:**
- VCP pipe body extremely durable (50-200 year lifespan)
- BUT joint systems deteriorate much faster (25-30 years)
- Most VCP in LA County is 70-120 years old → joint failures widespread
- Root intrusion is leading cause in EDA results (39% of SSO incidents)

**Why Root Intrusion Matters:**
- Roots cause blockages leading to SSOs
- Roots accelerate structural deterioration
- Root clearing is temporary; roots regrow within months
- Represents ongoing operational failure mode

---

### Material Longevity & Service Life

**Expected Service Life (industry standards):**

| Material | Expected Life | Notes |
|----------|--------------|-------|
| **VCP** | 50-200 years | Pipe body very durable; joints fail at 25-30 years |
| **Concrete** | 50-100 years | H2S corrosion reduces lifespan significantly |
| **Cast Iron** | 75-100 years | Corrosion-dependent; can fail earlier in aggressive environments |
| **Ductile Iron** | 100+ years | Improved corrosion resistance vs. cast iron |
| **PVC** | 100+ years | Modern material with excellent longevity |
| **HDPE** | 50-100 years | Flexible, corrosion-resistant |
| **Asbestos Cement** | 50-75 years | Brittle, joint degradation issues |

---

### Material Risk Score Justification

Based on comprehensive vulnerability analysis across all six failure modes:

| Material | Score | Primary Risk Drivers |
|----------|-------|---------------------|
| **Cast Iron** | 100 | Severe H2S corrosion, old joint systems, brittleness |
| **Concrete** | 70 | H2S corrosion (1-10mm/yr), surface roughness, moderate structural issues |
| **Steel** | 60 | Corrosion susceptible but less used in sewers |
| **VCP** | 50 | Paradox: Long pipe lifespan BUT severe root intrusion due to failed joints |
| **Asbestos Cement** | 36 | Brittle, joint degradation, but H2S resistant |
| **Ductile Iron** | 18 | Better corrosion resistance than cast iron |
| **PVC/HDPE** | 10 | Low risk: H2S immune, good joints, flexible |
| **Unknown** | 50 | Conservative moderate assumption |

**Rationale for 50 score on VCP:**
- VCP appears high-risk in failure data (82.7% of LA County SSO incidents)
- BUT this is confounded by age (most VCP is 70-120 years old)
- Material itself is H2S-resistant and long-lasting
- Primary failure mode is root intrusion through deteriorated joints
- Scored at middle (50) reflecting mixed risk profile

---

### Why Water Main Data Was Excluded

**Initial Consideration:** Utah State University (USU) 2024 study on water main break rates showed:
- Cast Iron: 28.6 breaks per 100 miles
- PVC: 2.9 breaks per 100 miles
- Strong empirical data suggesting ~10x higher risk for cast iron

**Why We Rejected This Approach:**
1. **USU study explicitly excluded sewer pipes** - focused on pressurized water systems
2. **Different failure mechanisms:**
   - Water mains: Pressure cycling, external loads, soil movement
   - Sewer pipes: H2S corrosion, root intrusion, debris/FOG blockages
3. **Different operating environments:**
   - Water: Pressurized (50-100 PSI), clean water, external corrosion
   - Sewer: Gravity flow, corrosive atmosphere, internal degradation
4. **Inappropriate extrapolation** - would undermine model credibility

**Conclusion:** Material scoring must be based on sewer-specific failure modes, not water main data.

---

### Methodology Limitations & Transparency

**What We DON'T Have:**
- Empirical failure rate data by material type for LA County sewer system
- Total pipe inventory by material (denominator needed for true failure rates)
- Controlled studies comparing material performance under identical conditions

**What We DO Have:**
- Comprehensive understanding of failure mechanisms
- Industry knowledge of material vulnerabilities
- Qualitative rankings based on multiple risk factors
- 80/20 weighting that emphasizes age (well-validated) over material (informed estimate)

**Approach Justification:**
- Age accounts for 80% of risk score (research-backed)
- Material accounts for 20% of risk score (informed estimate)
- Even if material scores are ±20% uncertain, impact on final risk score is only ±4%
- Methodology prioritizes transparency: clearly stating limitations rather than claiming false precision

**Intended Audience:**
- Non-technical stakeholders requiring defensible prioritization
- Emphasis on clear explanations over academic rigor
- Honest acknowledgment of data limitations

---

*Last Updated: January 31, 2026*
