"""
Model validation for SSO pipe failure prediction.
Validates risk scoring approach using correlation analysis with severity indicators.
"""

import pandas as pd
import numpy as np
import json
import os
from preprocess import preprocess_data


def validate_risk_scoring(df):
    """
    Validate risk scores by correlating with severity indicators.

    Args:
        df: Preprocessed DataFrame with risk scores

    Returns:
        Dictionary of validation metrics
    """
    print("=" * 60)
    print("MODEL VALIDATION")
    print("=" * 60)

    metrics = {}

    # 1. Correlation with severity indicators
    print("\n1. CORRELATION ANALYSIS")
    print("-" * 60)

    # Check if volume data exists and is numeric
    if 'spill_volume_gal' in df.columns:
        # Filter out null/invalid volumes for correlation
        df_with_volume = df[df['spill_volume_gal'].notna() & (df['spill_volume_gal'] > 0)].copy()
        if len(df_with_volume) > 0:
            corr_volume = df_with_volume['risk_score'].corr(df_with_volume['spill_volume_gal'])
            metrics['risk_score_vs_volume'] = round(corr_volume, 4)
            print(f"   Risk Score vs Spill Volume: {corr_volume:.4f}")
            print(f"   (Based on {len(df_with_volume):,} records with valid volume data)")
        else:
            metrics['risk_score_vs_volume'] = None
            print("   Risk Score vs Spill Volume: No valid data")
    else:
        metrics['risk_score_vs_volume'] = None
        print("   Risk Score vs Spill Volume: Column not found")

    # Check for spill_reached_water or similar columns
    water_columns = [col for col in df.columns if 'water' in col.lower() or 'surface' in col.lower()]
    if water_columns:
        print(f"   Note: Found potential water-related columns: {', '.join(water_columns)}")
        # Try first water-related column
        water_col = water_columns[0]
        df_with_water = df[df[water_col].notna()].copy()
        if len(df_with_water) > 0:
            # Try to convert to numeric if it's Yes/No or similar
            try:
                if df_with_water[water_col].dtype == 'object':
                    water_numeric = df_with_water[water_col].map({'Yes': 1, 'No': 0, 'Y': 1, 'N': 0})
                    if water_numeric.notna().sum() > 0:
                        corr_water = df_with_water['risk_score'].corr(water_numeric)
                        metrics['risk_score_vs_water'] = round(corr_water, 4)
                        print(f"   Risk Score vs {water_col}: {corr_water:.4f}")
                else:
                    corr_water = df_with_water['risk_score'].corr(df_with_water[water_col])
                    metrics['risk_score_vs_water'] = round(corr_water, 4)
                    print(f"   Risk Score vs {water_col}: {corr_water:.4f}")
            except:
                metrics['risk_score_vs_water'] = None
    else:
        metrics['risk_score_vs_water'] = None

    # 2. Distribution by material type
    print("\n2. RISK SCORE DISTRIBUTION BY MATERIAL (Standardized)")
    print("-" * 60)

    # Use standardized material names if available
    material_col = 'pipe_material_standardized' if 'pipe_material_standardized' in df.columns else 'pipe_material'
    material_stats = df.groupby(material_col)['risk_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)
    metrics['avg_risk_by_material'] = {}

    print(f"   {'Material':<30} {'Avg Risk':<12} {'Count':<10}")
    print(f"   {'-'*30} {'-'*12} {'-'*10}")

    for material, row in material_stats.head(15).iterrows():
        avg_risk = row['mean']
        count = row['count']
        metrics['avg_risk_by_material'][str(material)] = round(avg_risk, 2)
        print(f"   {str(material):<30} {avg_risk:>10.2f}  {count:>8,}")

    if len(material_stats) > 15:
        print(f"   ... and {len(material_stats) - 15} more materials")

    # 3. Distribution by age group
    print("\n3. RISK SCORE DISTRIBUTION BY AGE BAND")
    print("-" * 60)

    # Create age bands
    df['age_band'] = pd.cut(df['pipe_age_years'],
                            bins=[0, 30, 50, 70, 90, float('inf')],
                            labels=['0-30', '31-50', '51-70', '71-90', '90+'])

    age_stats = df.groupby('age_band')['risk_score'].agg(['mean', 'count'])
    metrics['avg_risk_by_age_band'] = {}

    print(f"   {'Age Band':<15} {'Avg Risk':<12} {'Count':<10}")
    print(f"   {'-'*15} {'-'*12} {'-'*10}")

    for age_band, row in age_stats.iterrows():
        avg_risk = row['mean']
        count = row['count']
        metrics['avg_risk_by_age_band'][str(age_band)] = round(avg_risk, 2)
        print(f"   {str(age_band):<15} {avg_risk:>10.2f}  {count:>8,}")

    # 4. Analysis by spill cause
    print("\n4. RISK SCORE BY SPILL CAUSE")
    print("-" * 60)

    if 'spill_cause' in df.columns:
        cause_stats = df.groupby('spill_cause')['risk_score'].agg(['mean', 'count']).sort_values('mean', ascending=False)
        metrics['avg_risk_by_cause'] = {}

        print(f"   {'Cause':<30} {'Avg Risk':<12} {'Count':<10}")
        print(f"   {'-'*30} {'-'*12} {'-'*10}")

        for cause, row in cause_stats.head(10).iterrows():
            avg_risk = row['mean']
            count = row['count']
            metrics['avg_risk_by_cause'][str(cause)] = round(avg_risk, 2)
            print(f"   {str(cause)[:30]:<30} {avg_risk:>10.2f}  {count:>8,}")

        if len(cause_stats) > 10:
            print(f"   ... and {len(cause_stats) - 10} more causes")
    else:
        metrics['avg_risk_by_cause'] = {}
        print("   spill_cause column not found")

    # 5. Overall scoring validation
    print("\n5. SCORING VALIDATION SUMMARY")
    print("-" * 60)

    # Check if higher risk scores align with worse outcomes
    if metrics.get('risk_score_vs_volume'):
        if metrics['risk_score_vs_volume'] > 0:
            print("   ✓ Positive correlation with spill volume (expected)")
        else:
            print("   ⚠ Negative/no correlation with spill volume (unexpected)")

    # Check age band progression
    age_band_order = ['0-30', '31-50', '51-70', '71-90', '90+']
    age_scores = [metrics['avg_risk_by_age_band'].get(band, 0) for band in age_band_order if band in metrics['avg_risk_by_age_band']]
    if age_scores == sorted(age_scores):
        print("   ✓ Risk scores increase with pipe age (expected)")
    else:
        print("   ⚠ Risk scores do not consistently increase with age")

    # Check material scoring makes sense
    high_risk_materials = ['VCP', 'vcp', 'Concrete', 'concrete']
    material_dict = metrics['avg_risk_by_material']
    high_risk_avg = np.mean([material_dict.get(mat, 0) for mat in high_risk_materials if mat in material_dict])
    if high_risk_avg > 65:
        print("   ✓ High-risk materials (VCP, Concrete) have elevated scores")
    else:
        print("   ⚠ High-risk material scores lower than expected")

    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60 + "\n")

    return metrics


def save_metrics(metrics, output_path, total_records, records_scored, records_missing):
    """
    Save validation metrics to JSON file.

    Args:
        metrics: Dictionary of validation metrics
        output_path: Path to save JSON file
        total_records: Total records in original dataset
        records_scored: Records successfully scored
        records_missing: Records filtered out
    """
    # Get risk distribution from metrics if available
    output = {
        "total_records": total_records,
        "records_scored": records_scored,
        "records_missing_age_or_material": records_missing,
        "methodology": "80% Age / 20% Material weighted scoring",
        "correlations": {
            "risk_vs_volume": metrics.get('risk_score_vs_volume'),
            "risk_vs_water": metrics.get('risk_score_vs_water')
        },
        "avg_risk_by_material": metrics.get('avg_risk_by_material', {}),
        "avg_risk_by_age_band": metrics.get('avg_risk_by_age_band', {}),
        "avg_risk_by_cause": metrics.get('avg_risk_by_cause', {})
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Metrics saved to: {output_path}")


if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "sso_la_county_analyzed.csv")
    preprocessed_file = os.path.join(base_dir, "data", "preprocessed_data.csv")
    metrics_file = os.path.join(base_dir, "outputs", "model_metrics.json")

    # Load original data to get counts
    df_original = pd.read_csv(input_file)
    total_records = len(df_original)

    # Check if preprocessed data exists, otherwise create it
    if os.path.exists(preprocessed_file):
        print(f"Loading preprocessed data from: {preprocessed_file}\n")
        df = pd.read_csv(preprocessed_file)
    else:
        print("Preprocessed data not found. Running preprocessing...\n")
        df = preprocess_data(input_file, preprocessed_file)

    records_scored = len(df)
    records_missing = total_records - records_scored

    # Run validation
    metrics = validate_risk_scoring(df)

    # Save metrics
    save_metrics(metrics, metrics_file, total_records, records_scored, records_missing)
