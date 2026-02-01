# Sewer Pipe Failure Prediction - Project Tasks

## Deliverables
- HTML Dashboard
- GitHub Repository
- 1-Page Executive Summary

---

## Tasks

| # | Task | Status |
|---|------|--------|
| 1 | Data collection & integration (SSO.txt + Cat1-2-3-Spills.txt) | ✅ Complete |
| 2 | Data cleaning & standardization (column mapping, geographic filtering) | ✅ Complete |
| 3 | Exploratory Data Analysis (EDA) | ✅ Complete |
| 4 | Literature review & research findings (4 academic papers) | ✅ Complete |
| 5 | Commercial tool research (Oakland/Info360, LASAN RAMS) | ✅ Complete |
| 6 | Material failure mode research (H2S corrosion, root intrusion, etc.) | ✅ Complete |
| 7 | Build weighted risk scoring model (80% Age / 20% Material) | ✅ Complete |
| 8 | Implement exponential age scoring (Isfahan-based) | ✅ Complete |
| 9 | Implement material vulnerability scoring (6 failure modes) | ✅ Complete |
| 10 | Model validation & methodology documentation | ✅ Complete |
| 11 | Export model outputs (model_results.csv) | ✅ Complete |
| 12 | Create HTML dashboard | ✅ Complete |
| 13 | Set up GitHub repository | ⬜ Not started |
| 14 | Write 1-page executive summary | ⬜ Not started |

---

## Completed Model Details

**Approach:** Weighted risk scoring (not logistic regression - no non-failure data available)

**Scoring Methodology:**
- **Age (80%):** Exponential curve `score = 20 + ((age/100)^1.8) * 80`
- **Material (20%):** 6 failure modes → Cast Iron=100, Concrete=70, VCP=50, PVC=10

**Output:**
- 3,512 pipes scored (50% of 7,020 SSO incidents)
- Risk distribution: Critical 22%, High 27%, Medium 36%, Low 15%
- Files: [model_results.csv](sso-prediction-model/outputs/model_results.csv), [model_metrics.json](sso-prediction-model/outputs/model_metrics.json)

---

*Last updated: February 1, 2026*
