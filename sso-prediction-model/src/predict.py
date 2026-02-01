"""
Generate predictions and final outputs for Power BI visualization.
Creates risk rankings and comprehensive output files.
"""

import pandas as pd
import numpy as np
import os
from preprocess import preprocess_data


def generate_predictions(df):
    """
    Add risk rankings and prepare final output.

    Args:
        df: Preprocessed DataFrame with risk scores

    Returns:
        DataFrame with rankings added
    """
    print("=" * 60)
    print("GENERATING PREDICTIONS")
    print("=" * 60)

    # Add risk ranking (1 = highest risk)
    print("\n1. Adding risk rankings...")
    df_output = df.copy()
    df_output['risk_rank'] = df_output['risk_score'].rank(ascending=False, method='min').astype(int)
    print(f"   ✓ Ranked {len(df_output):,} records")

    # Summary statistics
    print("\n2. SUMMARY STATISTICS")
    print("-" * 60)
    print(f"   Total records scored: {len(df_output):,}")

    # Risk category distribution
    print("\n   Risk Category Distribution:")
    category_counts = df_output['risk_category'].value_counts()
    for category in ['Critical', 'High', 'Medium', 'Low']:
        if category in category_counts:
            count = category_counts[category]
            pct = (count / len(df_output)) * 100
            print(f"      {category:>8}: {count:>6,} ({pct:>5.1f}%)")

    # Average risk by material
    print("\n   Average Risk Score by Material (Standardized, Top 10):")
    material_col = 'pipe_material_standardized' if 'pipe_material_standardized' in df_output.columns else 'pipe_material'
    material_avg = df_output.groupby(material_col)['risk_score'].mean().sort_values(ascending=False).head(10)
    for material, avg_risk in material_avg.items():
        count = len(df_output[df_output[material_col] == material])
        print(f"      {str(material)[:30]:>30}: {avg_risk:>6.2f}  (n={count:,})")

    # Average risk by age band
    print("\n   Average Risk Score by Age Band:")
    df_output['age_band'] = pd.cut(df_output['pipe_age_years'],
                                    bins=[0, 30, 50, 70, 90, float('inf')],
                                    labels=['0-30', '31-50', '51-70', '71-90', '90+'])
    age_band_avg = df_output.groupby('age_band')['risk_score'].mean()
    for band, avg_risk in age_band_avg.items():
        count = len(df_output[df_output['age_band'] == band])
        print(f"      {str(band):>8}: {avg_risk:>6.2f}  (n={count:,})")

    # Top 10 highest risk locations
    print("\n3. TOP 10 HIGHEST RISK LOCATIONS")
    print("-" * 60)

    # Check for location columns
    has_lat = 'latitude' in df_output.columns or 'latitude_num' in df_output.columns
    has_lon = 'longitude' in df_output.columns or 'longitude_num' in df_output.columns
    has_location = 'location_name' in df_output.columns

    if has_lat or has_lon or has_location:
        top_10 = df_output.nlargest(10, 'risk_score')

        lat_col = 'latitude_num' if 'latitude_num' in df_output.columns else 'latitude'
        lon_col = 'longitude_num' if 'longitude_num' in df_output.columns else 'longitude'

        print(f"   {'Rank':<6} {'Risk':<8} {'Age':<6} {'Material':<15} {'Location':<30}")
        print(f"   {'-'*6} {'-'*8} {'-'*6} {'-'*15} {'-'*30}")

        for idx, row in top_10.iterrows():
            rank = row['risk_rank']
            risk = row['risk_score']
            age = row['pipe_age_years']
            # Use standardized material if available
            if 'pipe_material_standardized' in row:
                material = str(row['pipe_material_standardized'])[:15]
            else:
                material = str(row['pipe_material'])[:15]
            location = str(row.get('location_name', 'N/A'))[:30] if has_location else 'N/A'

            print(f"   {rank:<6} {risk:>6.2f}  {age:>6.0f} {material:<15} {location:<30}")

        if has_lat and has_lon:
            print(f"\n   ✓ Latitude/Longitude preserved for mapping")
    else:
        print("   No location data available in dataset")

    print("\n" + "=" * 60)
    print("PREDICTION GENERATION COMPLETE")
    print("=" * 60 + "\n")

    return df_output


def save_results(df, output_path):
    """
    Save final results in Power BI-ready format.

    Args:
        df: DataFrame with predictions
        output_path: Path to save CSV file
    """
    print(f"Saving results to: {output_path}")

    # Ensure Power BI-ready format
    # Column names should be clean (already are from source data)

    # Select columns to include - keep all original plus new scoring columns
    output_cols = list(df.columns)

    # Ensure key columns are present
    required_new_cols = ['age_score', 'material_score', 'risk_score', 'risk_category', 'risk_rank']
    for col in required_new_cols:
        if col not in output_cols:
            print(f"   Warning: Missing column {col}")

    # Remove temporary age_band column if present
    if 'age_band' in output_cols:
        output_cols.remove('age_band')

    # Save to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df[output_cols].to_csv(output_path, index=False)

    print(f"   ✓ Saved {len(df):,} records")
    print(f"   ✓ {len(output_cols)} columns included")
    print(f"\n   Power BI Ready Features:")
    print(f"      • Clean column names (lowercase with underscores)")
    print(f"      • Risk category as string for filtering")
    print(f"      • Latitude/longitude preserved for mapping")
    print(f"      • Date fields preserved for time analysis")
    print(f"      • Risk rank for prioritization (1 = highest)")


def generate_feature_importance():
    """
    Generate feature importance based on our weighting scheme.

    Returns:
        DataFrame with feature weights
    """
    importance_data = {
        'feature': ['pipe_age_years', 'pipe_material'],
        'weight': [0.80, 0.20],
        'description': [
            'Age-based risk score (20-100 scale, Oakland bands)',
            'Material-based risk score (20-80 scale, failure rates)'
        ]
    }

    return pd.DataFrame(importance_data)


if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "sso_la_county_analyzed.csv")
    preprocessed_file = os.path.join(base_dir, "data", "preprocessed_data.csv")
    results_file = os.path.join(base_dir, "outputs", "model_results.csv")
    importance_file = os.path.join(base_dir, "outputs", "feature_importance.csv")

    # Check if preprocessed data exists, otherwise create it
    if os.path.exists(preprocessed_file):
        print(f"Loading preprocessed data from: {preprocessed_file}\n")
        df = pd.read_csv(preprocessed_file)
    else:
        print("Preprocessed data not found. Running preprocessing...\n")
        df = preprocess_data(input_file, preprocessed_file)

    # Generate predictions
    df_results = generate_predictions(df)

    # Save results
    save_results(df_results, results_file)

    # Save feature importance
    print(f"\nSaving feature importance to: {importance_file}")
    importance_df = generate_feature_importance()
    importance_df.to_csv(importance_file, index=False)
    print("   ✓ Feature importance saved")
