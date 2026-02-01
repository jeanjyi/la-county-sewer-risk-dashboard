# SSO Pipe Failure Prediction Model

A risk scoring model for predicting sewer pipe failure likelihood based on pipe age and material characteristics. Built using historical SSO (Sanitary Sewer Overflow) data from LA County.

## Overview

This model calculates risk scores for sewer pipes using a weighted combination of age-based and material-based risk factors. The outputs are designed for Power BI visualization and prioritization of infrastructure maintenance.

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running the Model

```bash
python main.py
```

This will run the complete pipeline:
1. Data preprocessing with filtering and scoring
2. Model validation with correlation analysis
3. Prediction generation for all records

### Running Individual Steps

```bash
# Step 1: Preprocess data
python src/preprocess.py

# Step 2: Validate model
python src/model.py

# Step 3: Generate predictions
python src/predict.py
```

## Methodology

### Scoring Approach

The model uses a **weighted risk scoring system** rather than binary classification:

- **Age Score (80% weight)**: 0-100 scale based on Oakland's Info360 Asset scoring bands
- **Material Score (20% weight)**: 0-100 scale based on known material failure rates
- **Combined Risk Score**: `(Age Score × 0.80) + (Material Score × 0.20)`

### Weighting Rationale

The 80/20 weighting is based on the **Dallas empirical study** showing a 4:1 importance ratio between age and material for predicting pipe condition.

### Age Bands (Oakland Info360 System)

Applied under EPA Consent Decree guidelines:

| Age Range | Risk Score | Risk Level |
|-----------|------------|------------|
| 0-30 years | 20 | Low |
| 31-50 years | 40 | Moderate |
| 51-70 years | 60 | Elevated |
| 71-90 years | 80 | High |
| 90+ years | 100 | Critical |

### Material Risk Scores

Based on known failure rates by material type:

| Material | Score | Examples |
|----------|-------|----------|
| High Risk | 70-80 | VCP (Vitrified Clay Pipe), Concrete, RCP |
| Medium Risk | 40-50 | Cast Iron, Steel |
| Lower Risk | 20-30 | PVC, HDPE, Ductile Iron |
| Unknown | 50 | Unclassified materials |

### Risk Categories

Final risk scores are binned into categories for filtering:

- **Low**: 0-40
- **Medium**: 41-60
- **High**: 61-80
- **Critical**: 81-100

## Data Limitations

**Important**: All input records are SSO incidents (failures). This is not a binary classification model but rather a **risk severity scoring system**.

The model:
- ✓ Produces relative risk scores for prioritization
- ✓ Validates scoring via correlation with severity indicators (spill volume)
- ✗ Does not predict failure vs. non-failure (no non-failure baseline data)

## Validation Approach

The model validates the scoring methodology by:

1. **Correlation with spill volume** - Higher risk scores should correlate with larger spills
2. **Age progression** - Risk scores should increase consistently with pipe age
3. **Material classification** - High-risk materials (VCP, Concrete) should have elevated scores
4. **Cause analysis** - Structural failure causes should align with higher risk scores

## Alignment with Industry Standards

This methodology matches:
- **LASAN's RAMS algorithm** - Uses age and material to predict pipe condition when CCTV data is unavailable
- **Oakland's Info360 Asset scoring** - Age band classification system
- **EPA Consent Decree requirements** - Risk-based prioritization for infrastructure management

## Project Structure

```
sso-prediction-model/
├── data/
│   ├── sso_la_county_analyzed.csv      # Input data
│   └── preprocessed_data.csv           # Intermediate output (generated)
├── src/
│   ├── preprocess.py                   # Data cleaning and scoring
│   ├── model.py                        # Validation analysis
│   └── predict.py                      # Final predictions
├── outputs/
│   ├── model_results.csv               # Power BI ready predictions
│   ├── model_metrics.json              # Validation statistics
│   └── feature_importance.csv          # Weight documentation
├── main.py                             # Orchestrator script
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Output Files

### model_results.csv
Complete dataset with all original columns plus:
- `age_score` - Age-based risk (0-100)
- `material_score` - Material-based risk (0-100)
- `risk_score` - Combined risk score (0-100)
- `risk_category` - Low/Medium/High/Critical
- `risk_rank` - Rank ordering (1 = highest risk)

**Power BI Ready Features:**
- Clean column names (lowercase with underscores)
- Preserved latitude/longitude for mapping
- Preserved date fields for time series analysis
- Risk categories as strings for filtering

### model_metrics.json
Validation statistics including:
- Total records processed
- Risk distribution by category
- Correlation coefficients
- Average risk by material type
- Average risk by age band
- Average risk by spill cause

### feature_importance.csv
Documents the 80/20 weighting scheme:
- Age: 80% weight
- Material: 20% weight

## Usage Example

```python
from src.preprocess import preprocess_data
from src.model import validate_risk_scoring
from src.predict import generate_predictions

# Load and score data
df = preprocess_data('data/sso_la_county_analyzed.csv')

# Validate scoring approach
metrics = validate_risk_scoring(df)

# Generate final predictions
results = generate_predictions(df)
```

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- numpy >= 1.23.0
- scikit-learn >= 1.1.0

## License

Model developed for LA County SSO analysis and infrastructure prioritization.

## References

- Dallas empirical study on pipe age vs. material importance (4:1 ratio)
- Oakland Info360 Asset scoring system (EPA Consent Decree)
- LASAN RAMS algorithm methodology
