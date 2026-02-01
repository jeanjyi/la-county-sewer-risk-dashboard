#!/usr/bin/env python3
"""
Model Validation: Analyze risk scores at time of pipe failure

This script validates the risk model by examining the distribution of
risk scores when pipes actually failed. If the model works well, most
failures should occur in High/Critical risk categories.
"""

import pandas as pd

def main():
    # Load model results
    df = pd.read_csv('outputs/model_results.csv')

    print("="*60)
    print("MODEL VALIDATION: Risk Scores at Time of Failure")
    print("="*60)
    print(f"\nTotal incidents analyzed: {len(df):,}")

    # Analysis 1: Risk Score Statistics at Failure
    print("\n" + "="*60)
    print("1. RISK SCORE DISTRIBUTION AT FAILURE")
    print("="*60)
    print(f"  Mean Risk Score:   {df['risk_score'].mean():.1f}")
    print(f"  Median Risk Score: {df['risk_score'].median():.1f}")
    print(f"  Min Risk Score:    {df['risk_score'].min():.1f}")
    print(f"  Max Risk Score:    {df['risk_score'].max():.1f}")
    print(f"  Std Deviation:     {df['risk_score'].std():.1f}")

    # Analysis 2: Distribution by Risk Category
    print("\n" + "="*60)
    print("2. FAILURE DISTRIBUTION BY RISK CATEGORY")
    print("="*60)

    category_counts = df['risk_category'].value_counts()
    category_pct = (category_counts / len(df) * 100)

    print("\n  Category    Count    Percentage")
    print("  " + "-"*38)
    for cat in ['Critical', 'High', 'Medium', 'Low']:
        count = category_counts.get(cat, 0)
        pct = category_pct.get(cat, 0)
        print(f"  {cat:10}  {count:5}    {pct:5.1f}%")

    # Validation: Are most failures in High/Critical?
    high_critical_pct = category_pct.get('Critical', 0) + category_pct.get('High', 0)
    print(f"\n  → {high_critical_pct:.1f}% of failures occurred in High/Critical risk pipes")
    print(f"  → {category_pct.get('Critical', 0):.1f}% of failures occurred in Critical risk pipes alone")

    # Analysis 3: Age Statistics at Failure
    print("\n" + "="*60)
    print("3. PIPE AGE AT FAILURE")
    print("="*60)
    print(f"  Mean Age:   {df['pipe_age_years'].mean():.1f} years")
    print(f"  Median Age: {df['pipe_age_years'].median():.1f} years")
    print(f"  Min Age:    {df['pipe_age_years'].min():.1f} years")
    print(f"  Max Age:    {df['pipe_age_years'].max():.1f} years")

    # Analysis 4: Material-Specific Breakdown
    print("\n" + "="*60)
    print("4. FAILURES BY MATERIAL TYPE")
    print("="*60)

    material_stats = df.groupby('pipe_material_standardized').agg({
        'risk_score': ['mean', 'count'],
        'pipe_age_years': 'mean'
    }).round(1)

    material_stats.columns = ['Avg Risk Score', 'Count', 'Avg Age']
    material_stats = material_stats[material_stats['Count'] >= 10].sort_values('Avg Risk Score', ascending=False)

    print("\n  Material                     Count  Avg Risk  Avg Age")
    print("  " + "-"*60)
    for material, row in material_stats.iterrows():
        print(f"  {material:25}  {int(row['Count']):5}    {row['Avg Risk Score']:5.1f}   {row['Avg Age']:5.1f}")

    # Analysis 5: Model Performance Assessment
    print("\n" + "="*60)
    print("5. MODEL PERFORMANCE ASSESSMENT")
    print("="*60)

    print(f"\n  Average risk score at failure: {df['risk_score'].mean():.1f}")
    print(f"  (Scale: 18-100, where 18 = lowest risk, 100 = highest risk)")

    if high_critical_pct >= 60:
        assessment = "STRONG - Majority of failures in High/Critical categories"
    elif high_critical_pct >= 40:
        assessment = "MODERATE - Significant failures in High/Critical categories"
    else:
        assessment = "WEAK - Too many failures in Low/Medium categories"

    print(f"\n  Model Performance: {assessment}")
    print(f"  → The model successfully identifies {high_critical_pct:.0f}% of failures")
    print(f"     as High or Critical risk pipes")

    # Key Insights
    print("\n" + "="*60)
    print("KEY INSIGHTS")
    print("="*60)

    print("\n  ✓ Pipes failed at an average risk score of {:.1f}".format(df['risk_score'].mean()))
    print(f"  ✓ {category_pct.get('Critical', 0):.0f}% of failures were Critical risk (score > 80)")
    print(f"  ✓ {high_critical_pct:.0f}% of failures were High or Critical risk (score > 60)")
    print(f"  ✓ Average age at failure: {df['pipe_age_years'].mean():.0f} years")

    top_material = material_stats.index[0] if len(material_stats) > 0 else "N/A"
    print(f"  ✓ Highest-risk material failures: {top_material}")

    print("\n" + "="*60)

if __name__ == '__main__':
    main()
