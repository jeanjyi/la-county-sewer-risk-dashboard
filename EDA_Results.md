# Exploratory Data Analysis: LA County SSO Data

## Executive Summary

This EDA analyzed **7,020 sanitary sewer overflow (SSO) incidents** in LA County from 2007-2025. Key findings that inform our predictive model:

- **Pipe age data is available for 48.5%** of records, with a median failure age of **69 years**
- **Vitrified Clay Pipe (VCP)** accounts for 45% of incidents with known material
- **Root intrusion** is the leading cause (39% of incidents)
- Age distribution shows failures concentrated in **41-100 year old pipes** (78% of incidents with age data)

These findings support using **age as the primary predictor**, consistent with the academic literature review (see Research_Findings.md).

---

## 1. Data Integration

### Sources Combined
| Dataset | Period | Records |
|---------|--------|---------|
| SSO.txt | 2007-2023 | Historical data |
| Cat1-2-3-Spills.txt | 2023-present | Recent data |
| **Combined (LA County)** | **2007-2025** | **7,020** |

### Column Standardization
The two datasets used different column names. These were mapped to a unified schema:

| Unified Name | Purpose |
|--------------|---------|
| `pipe_material` | Material type (VCP, PVC, Cast Iron, etc.) |
| `pipe_age_years` | Age of pipe at time of failure |
| `spill_cause` | Cause of the SSO event |
| `spill_volume_gal` | Volume spilled in gallons |
| `latitude` / `longitude` | Geographic coordinates |

### Geographic Filtering
LA County was identified by:
1. `county == 'Los Angeles'` (from older dataset)
2. Lat/long bounding box: 33.7-34.8°N, 118.9-117.6°W (for newer dataset lacking county field)

---

## 2. Data Quality Assessment

| Variable | Records with Data | Coverage |
|----------|-------------------|----------|
| pipe_age_years | 3,408 | 48.5% |
| pipe_material | 4,030 | 57.4% |
| spill_cause | 7,020 | 100% |
| spill_volume_gal | ~7,000 | ~99% |
| lat/long | ~6,800 | ~97% |

**Implication**: Nearly half of records lack pipe age data. For predictive modeling, we can either:
1. Use only complete cases (3,408 records)
2. Impute missing ages based on material or location
3. Build separate models for records with/without age data

---

## 3. Pipe Material Analysis

### Methodology
- Cleaned text values (uppercase, strip whitespace)
- Mapped variations to standard names (e.g., "vcp", "VCP", "Vitrified Clay" → "Vitrified Clay (VCP)")

### Results

| Material | Incidents | % of Known |
|----------|-----------|------------|
| Vitrified Clay (VCP) | 3,156 | 78.3% |
| Unknown | 2,990 | — |
| Concrete | 176 | 4.4% |
| Clay (unspecified) | 140 | 3.5% |
| Cast Iron | 49 | 1.2% |
| PVC | 39 | 1.0% |
| Other materials | <200 combined | <5% |

**Key Insight**: VCP dominates the failure data. This is expected because:
1. VCP was the standard material from ~1900-1980
2. These pipes are now 45-125 years old (peak failure age range)
3. VCP is susceptible to root intrusion and joint failures

---

## 4. Pipe Age Analysis

### Methodology
- Converted age field to numeric, filtering out invalid values (kept 0-150 years)
- Calculated descriptive statistics
- Binned ages into 20-year groups for distribution analysis

### Descriptive Statistics

| Statistic | Value |
|-----------|-------|
| **Mean** | 67.6 years |
| **Median** | 69.0 years |
| **Std Dev** | 25.9 years |
| **Min** | 0 years |
| **Max** | 138 years |

### Age Distribution at Failure

| Age Group | Incidents | % of Total |
|-----------|-----------|------------|
| 0-20 years | 206 | 6.0% |
| 21-40 years | 284 | 8.3% |
| 41-60 years | 865 | 25.4% |
| 61-80 years | 753 | 22.1% |
| 81-100 years | 1,058 | 31.0% |
| 100+ years | 234 | 6.9% |

**Key Insight**: 78% of failures occur in pipes aged 41-100 years. The distribution peaks at 81-100 years, supporting the research finding that failure risk increases dramatically after ~40 years.

---

## 5. Spill Cause Analysis

### Methodology
- Simplified cause categories using keyword matching
- Causes often contain multiple factors; assigned to primary category

### Results

| Cause Category | Incidents | % of Total |
|----------------|-----------|------------|
| Root Intrusion | 2,755 | 39.2% |
| Other/Unknown | 1,512 | 21.5% |
| FOG (Fats, Oils, Grease) | 1,419 | 20.2% |
| Debris/Rags | 854 | 12.2% |
| Pipe Structural Failure | 329 | 4.7% |
| Vandalism | 82 | 1.2% |
| Capacity/Flow Issues | 37 | 0.5% |
| Operator Error | 32 | 0.5% |

**Key Insight**: Root intrusion (39%) and FOG (20%) are the top causes. These are both influenced by pipe age and material:
- Older pipes have more joint deterioration where roots enter
- VCP joints are particularly susceptible to root intrusion

---

## 6. Spill Volume Analysis

### Descriptive Statistics

| Statistic | Value (gallons) |
|-----------|-----------------|
| **Mean** | 8,179 |
| **Median** | 200 |
| **90th Percentile** | 2,490 |
| **99th Percentile** | 34,928 |
| **Maximum** | 11,536,234 |

**Key Insight**: The distribution is heavily right-skewed. Most spills are small (median = 200 gal), but a few extreme events pull the mean up. The max of 11.5M gallons represents a catastrophic failure. For modeling severity, consider:
- Log-transforming volume
- Using percentile-based categories (small/medium/large)
- Focusing on binary failure prediction rather than volume

---

## 7. Cross-Tabulation: Age by Material

### Average Age at Failure by Material
(Minimum 50 incidents for statistical reliability)

| Material | Mean Age | Median Age | Count |
|----------|----------|------------|-------|
| Clay (unspecified) | 106.5 | 50.0 | 90 |
| Vitrified Clay (VCP) | 101.2 | 71.0 | 2,742 |
| Concrete | 84.4 | 86.0 | 173 |

**Key Insight**: VCP and Clay pipes have the highest average failure ages, reflecting that these are the oldest materials still in service. This doesn't mean they're more durable—it means they were installed earlier.

---

## 8. LAX Area Analysis

### Geographic Filter
LAX area defined as: 33.91-33.97°N, 118.45-118.37°W

### Results
- **Total LAX-area incidents**: 55
- **Dominant material**: VCP (91% of incidents)
- **Average pipe age**: 78.4 years (vs. 67.6 county-wide)
- **Top cause**: Root intrusion (51%)

**Key Insight**: The LAX area has older infrastructure than the county average. This suggests targeting older VCP pipes for inspection/replacement priority.

---

## Statistical Concepts Used

### Descriptive Statistics
- **Mean**: Average value. Calculated as sum ÷ count. Sensitive to outliers (see spill volume mean vs. median).
- **Median**: Middle value when sorted. More robust to extreme values.
- **Standard Deviation**: Measures spread around the mean. ~68% of data falls within ±1 std dev of mean.

### Percentiles
- The Nth percentile is the value below which N% of data falls.
- Example: 90th percentile spill volume = 2,490 gal means 90% of spills are ≤2,490 gal.

### Frequency Distribution
- Counts of each category in a categorical variable.
- Reveals dominant values (VCP is 78% of known materials).

### Data Cleaning
- Standardizing text (uppercase, strip whitespace)
- Mapping variations to canonical values
- Handling missing values (Unknown category vs. exclusion)

### Binning (Discretization)
- Converting continuous variables to categories.
- Example: Age 67.3 years → "61-80" age group.
- Useful for seeing patterns in distributions.

### Cross-Tabulation
- Analyzing one variable grouped by another.
- Example: Average age at failure, grouped by material type.
- Reveals interaction effects between variables.

---

## Implications for Predictive Model

Based on this EDA:

1. **Age should be the primary predictor** — 78% of failures are in pipes 41-100 years old, and age data is available for 48.5% of records.

2. **Material is secondary but useful** — VCP dominates failures, but this reflects its prevalence in older infrastructure rather than inherent fragility.

3. **Consider cause as a confounding variable** — Root intrusion (39%) and grease (20%) are top causes. These may correlate with both age and material.

4. **Binary classification is appropriate** — Rather than predicting volume, predict failure/no-failure. Volume distribution is too skewed for reliable regression.

5. **Data quality considerations** — 51% missing age data is significant. Consider imputation or separate models for complete vs. incomplete records.

---

*Last updated: February 2026*
*Data source: California State Water Resources Control Board CIWQS database*
