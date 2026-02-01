# LA County Sewer Pipe Risk Assessment Dashboard

Interactive dashboard for identifying highest-risk sewer infrastructure in Los Angeles County to support maintenance prioritization.

**[View Live Dashboard](https://jeanjyi.github.io/la-county-sewer-risk-dashboard/dashboard.html)**

## Overview

This project analyzes sanitary sewer overflow (SSO) incidents from 2007-2025 to build a predictive risk model for LA County's sewer pipe infrastructure. The model scores 3,512 pipes based on age and material factors to help prioritize maintenance efforts.

## Key Findings

| Metric | Value |
|--------|-------|
| Total Pipes Scored | 3,512 |
| High/Critical Risk | 48% |
| Average Risk Score | 60.3 |
| Pipes 70+ Years Old | 49% |

### Risk Distribution
- **Critical**: 20.8%
- **High**: 27.6%
- **Medium**: 36.2%
- **Low**: 15.4%

## Methodology

### Risk Score Formula
```
risk_score = (age_score × 0.80) + (material_score × 0.20)
```

**Age Scoring (80% weight)**
- Based on exponential curve from Isfahan sewer failure study
- New pipes start at baseline score of 20
- Score accelerates exponentially after 50 years

**Material Scoring (20% weight)**
- 6-factor assessment: H₂S Corrosion, Root Intrusion, Structural Integrity, Joint Degradation, Surface Roughness, Longevity
- 147 material name variants standardized to 12 canonical types

### Data Sources
- California State Water Board SSO database (2007-2025)
- 7,020 SSO incidents in LA County
- Pipe age and material data from incident reports

## Dashboard Features

- **Executive Overview**: KPIs, risk distribution charts, age vs risk analysis
- **Geographic Analysis**: Interactive map with filterable risk markers
- **Top Risks**: Sortable table of highest-risk locations with city geocoding
- **Methodology**: Detailed explanation of scoring approach

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Plotly.js, Leaflet.js
- **Data Processing**: Python, Pandas
- **Geocoding**: OpenStreetMap Nominatim API

## Local Development

```bash
# Clone the repository
git clone https://github.com/jeanjyi/la-county-sewer-risk-dashboard.git
cd la-county-sewer-risk-dashboard

# Start local server
python3 -m http.server 8000

# Open in browser
open http://localhost:8000/dashboard.html
```

## Project Structure

```
├── dashboard.html              # Main interactive dashboard
├── sso-prediction-model/
│   ├── main.py                 # Model entry point
│   ├── src/
│   │   ├── preprocess.py       # Data cleaning & standardization
│   │   ├── model.py            # Risk scoring logic
│   │   └── predict.py          # Prediction pipeline
│   └── outputs/
│       └── model_results.csv   # Scored pipe data
├── Research Papers/            # Academic sources
└── *.md                        # Documentation
```

## References

- Goodarzi et al. (2024) - Isfahan sewer failure study (age curve)
- Dallas Water Utilities - Age/material weighting research
- ASCE 2025 Wastewater Infrastructure Report Card

## Author

Jean Yi

---

*Built with assistance from Claude (Anthropic)*
