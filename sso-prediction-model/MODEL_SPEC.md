# SSO Pipe Failure Prediction Model - Implementation Spec

## Overview

Build a logistic regression model to predict sewer pipe failure likelihood based on pipe age and material. The model uses historical SSO (Sanitary Sewer Overflow) data from LA County.

---

## Project Structure

```
sso-prediction-model/
├── data/
│   └── sso_la_county_analyzed.csv    # Input data (user provides)
├── src/
│   ├── preprocess.py                 # Data cleaning and feature engineering
│   ├── model.py                      # Model training and evaluation
│   └── predict.py                    # Generate predictions for all records
├── outputs/
│   ├── model_results.csv             # Predictions with risk scores
│   ├── model_metrics.json            # Accuracy, precision, recall, etc.
│   └── feature_importance.csv        # Model coefficients
├── requirements.txt
└── README.md
```

---

## Step 1: Data Preprocessing (`preprocess.py`)

### Input
- `sso_la_county_analyzed.csv` — SSO incident data with columns including:
  - `pipe_age_years` (numeric, may have nulls)
  - `pipe_material` (string, may have nulls)
  - Other columns we won't use for the model

### Filtering
1. Keep only records where `pipe_age_years` is not null
2. Keep only records where `pipe_material` is not null
3. Log how many records remain after filtering

### Feature Engineering

**Age Score (0-100 scale, 80% weight):**

Use Oakland's age bands as reference, scaled to 0-100:

```python
def calculate_age_score(age):
    if age <= 30:
        return 20      # Low risk
    elif age <= 50:
        return 40      # Moderate risk
    elif age <= 70:
        return 60      # Elevated risk
    elif age <= 90:
        return 80      # High risk
    else:
        return 100     # Critical risk
```

**Material Score (0-100 scale, 20% weight):**

Based on known failure rates by material type:

```python
def calculate_material_score(material):
    material = str(material).upper().strip()
    
    # High risk materials
    if any(x in material for x in ['VCP', 'VITRIFIED', 'CLAY']):
        return 80
    if any(x in material for x in ['CONCRETE', 'CMP', 'RCP']):
        return 70
    
    # Medium risk
    if any(x in material for x in ['CAST IRON', 'CI', 'IRON']):
        return 50
    if any(x in material for x in ['STEEL']):
        return 40
    
    # Lower risk (modern materials)
    if any(x in material for x in ['PVC', 'PLASTIC', 'POLY', 'HDPE', 'PE']):
        return 20
    if any(x in material for x in ['DUCTILE', 'DIP']):
        return 30
    
    # Unknown - assign moderate risk
    return 50
```

**Combined Risk Score:**

```python
risk_score = (age_score * 0.80) + (material_score * 0.20)
```

### Output
Save preprocessed data with new columns:
- `age_score`
- `material_score`
- `risk_score`
- `risk_category` (Low/Medium/High/Critical based on risk_score thresholds)

Risk categories:
- 0-40: Low
- 41-60: Medium
- 61-80: High
- 81-100: Critical

---

## Step 2: Model Training (`model.py`)

### Approach
Since we're working with SSO incident data (all records are failures), we need to reframe this as a risk scoring model rather than traditional classification. The logistic regression will validate our scoring approach.

### Option A: Validate Scoring Approach
1. Use the calculated `risk_score` as the primary output
2. Validate by checking correlation between risk_score and:
   - Spill volume (`spill_volume_gal`)
   - Whether spill reached water (`spill_reached_water`)
3. Report correlation coefficients

### Option B: If We Had Non-Failure Data
If we want to demonstrate classification capability, we could:
1. Create synthetic "non-failure" baseline using inverse characteristics
2. Train logistic regression on binary outcome
3. Report accuracy metrics

**Implement Option A** — it's more honest given our data limitations.

### Validation Analysis
```python
# Correlate risk score with severity indicators
correlations = {
    'risk_score_vs_volume': df['risk_score'].corr(df['spill_volume_gal']),
    'risk_score_vs_reached_water': df['risk_score'].corr(df['spill_reached_water'].astype(int))
}
```

### Additional Analysis
- Distribution of risk scores by material type
- Distribution of risk scores by age band
- Average risk score by `spill_cause` (validate that structural causes have higher scores)

---

## Step 3: Generate Predictions (`predict.py`)

### Output File: `model_results.csv`

Include all original columns plus:
- `age_score`
- `material_score`
- `risk_score`
- `risk_category`
- `risk_rank` (1 = highest risk, descending)

### Summary Statistics
Print/log:
- Total records scored
- Distribution by risk category
- Top 10 highest risk locations (if lat/long available)
- Average risk score by material type
- Average risk score by age band

---

## Step 4: Output for Power BI

### `model_results.csv` should be Power BI ready:
- Clean column names (no spaces, lowercase with underscores)
- Risk category as string for filtering
- Lat/long preserved for mapping
- Date fields preserved for time analysis

### `model_metrics.json` structure:
```json
{
    "total_records": 7020,
    "records_scored": 3408,
    "records_missing_age": 3612,
    "risk_distribution": {
        "Critical": 245,
        "High": 892,
        "Medium": 1456,
        "Low": 815
    },
    "avg_risk_by_material": {
        "VCP": 78.4,
        "Concrete": 72.1,
        ...
    },
    "correlation_risk_vs_volume": 0.23,
    "methodology": "80% Age / 20% Material weighted scoring"
}
```

---

## Requirements

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.1.0
```

---

## Key Methodology Notes (For README)

1. **Weighting Rationale:** 80% Age / 20% Material based on Dallas empirical study showing 4:1 importance ratio

2. **Age Bands:** Adapted from Oakland's Info360 Asset scoring system (under EPA Consent Decree)

3. **Data Limitation:** All records are SSO incidents (failures). Model produces risk scores rather than binary predictions. Validation via correlation with severity indicators.

4. **Alignment:** Methodology matches LASAN's RAMS algorithm approach — using age and material to predict condition when CCTV data unavailable

---

## Execution Order

1. Run `preprocess.py` — creates cleaned dataset with scores
2. Run `model.py` — validates scoring, generates metrics
3. Run `predict.py` — creates final output for Power BI

Or create a `main.py` that runs all three in sequence.
