"""
Data preprocessing for SSO pipe failure prediction model.

METHODOLOGY:
- Age Scoring (80% weight): Exponential curve based on Isfahan failure data
  showing dramatic increase in failures after 40 years
- Material Scoring (20% weight): Comprehensive risk assessment across 6 failure
  modes (H2S corrosion, root intrusion, structural integrity, joint degradation,
  surface roughness, longevity)

RESEARCH BASIS:
- Dallas empirical study: Age 100% importance vs Material 25% → 80/20 weighting
- Isfahan study: Exponential failure curve (56 → 393 failures in 40-50 year band)
- Industry knowledge: Material vulnerability to H2S corrosion and root intrusion

LIMITATIONS:
- Material scores are informed estimates, not empirical failure rates
- Lack total pipe inventory by material for true rate calculations
- Designed for non-technical audience: defensibility over perfect precision
- 80/20 weighting means ±20% material uncertainty = only ±4% final score impact

ALIGNMENT:
- Oakland's Info360: "If no CCTV, use Age" for structural failure likelihood
- LASAN's RAMS: "Predicts condition when data unavailable using age, material"
"""

import pandas as pd
import numpy as np
import os


def calculate_age_score(age):
    """
    Calculate age-based risk score using exponential curve.

    Based on Isfahan study (Goodarzi 2024) showing exponential failure increase:
    - Failures increase from 56 to 393 in the 40-50 year age band
    - Exponential acceleration reflects real-world deterioration patterns

    Formula: score = min(100, 20 + ((age/100)^1.8) * 80)
    - Starts at 20 for new pipes (minimum risk)
    - Accelerates exponentially with age
    - Reaches 100 at age 100+

    Args:
        age: Pipe age in years

    Returns:
        Risk score from 20-100 (exponential scale)
    """
    if age <= 0:
        return 20

    # Exponential scoring: accelerates with age
    score = 20 + ((age / 100) ** 1.8) * 80

    return min(100, score)


def calculate_material_score(material):
    """
    Calculate material-based risk score using comprehensive vulnerability analysis.

    Scores based on six failure modes:
    1. H2S Corrosion - Hydrogen sulfide converts to sulfuric acid
    2. Root Intrusion - Tree roots penetrate joints/cracks
    3. Structural Integrity - Inherent strength and brittleness
    4. Joint Degradation - Deterioration of pipe connections
    5. Surface Roughness - Internal characteristics affecting flow
    6. Longevity - Expected service life

    NOTE: These are informed estimates based on known failure mechanisms,
    not rigorous empirical calculations from failure rate data.
    Material accounts for only 20% of final risk score; age is 80%.

    Args:
        material: Pipe material string (standardized)

    Returns:
        Risk score from 10-100
    """
    material_upper = str(material).upper().strip()

    # High risk materials
    if any(x in material_upper for x in ['CAST IRON', 'C.I.', 'CIP', 'CI']):
        return 100  # Severe H2S corrosion, old joint systems, brittleness

    # Medium-high risk
    if any(x in material_upper for x in ['CONCRETE', 'CONC', 'CON', 'RCP', 'CMP']):
        return 70   # H2S corrosion (1-10mm/yr), surface roughness

    if any(x in material_upper for x in ['STEEL']):
        return 60   # Corrosion susceptible

    # Medium risk
    if any(x in material_upper for x in ['VCP', 'VITRIFIED', 'CLAY', 'V.C.P']):
        return 50   # Paradox: Long pipe life BUT severe root intrusion via failed joints

    if any(x in material_upper for x in ['ASBESTOS', 'AC', 'A/C']):
        return 36   # Brittle, joint degradation (but H2S resistant)

    # Low risk (modern materials)
    if any(x in material_upper for x in ['DUCTILE', 'DIP', 'D.I.P']):
        return 18   # Better corrosion resistance than cast iron

    if any(x in material_upper for x in ['PVC', 'PLASTIC', 'POLY', 'HDPE', 'PE', 'POLYVINYL', 'POLYETHYLENE']):
        return 10   # H2S immune, good joints, flexible

    # Unknown - conservative moderate assumption
    return 50


def calculate_risk_category(risk_score):
    """
    Categorize risk score into bins.

    Args:
        risk_score: Combined risk score (0-100)

    Returns:
        Risk category string
    """
    if risk_score <= 40:
        return 'Low'
    elif risk_score <= 60:
        return 'Medium'
    elif risk_score <= 80:
        return 'High'
    else:
        return 'Critical'


def standardize_material_name(material):
    """
    Standardize material names to canonical forms.
    Handles capitalization, abbreviations, and variants.

    Args:
        material: Raw material string

    Returns:
        Standardized material name
    """
    if pd.isna(material):
        return 'Unknown'

    material_upper = str(material).upper().strip()

    # Handle numeric-only values and empty strings (data errors)
    if material_upper.isdigit() or material_upper == '' or len(material_upper) <= 2:
        # Short codes like 'MS' are likely data errors
        if material_upper not in ['CI', 'DI', 'AC', 'VC', 'CP']:  # Known valid 2-char codes
            return 'Unknown'

    # VCP / Vitrified Clay Pipe variants (includes terra cotta)
    if any(x in material_upper for x in ['VCP', 'VITRIFIED', 'CLAY', 'V.C.P', 'TCP', 'TERRA COTTA']):
        return 'VCP'

    # Handle standalone VC, BCP abbreviations for clay/vitrified pipes
    if material_upper in ['VC', 'V.C.', 'BCP']:
        return 'VCP'

    # Concrete Pipe variants (including CP, C.P., CON, CONC abbreviations)
    if any(x in material_upper for x in ['CONCRETE', 'CONC', 'RCP', 'NRCP', 'CMP']):
        if 'RCP' in material_upper or 'REINFORCED' in material_upper:
            return 'Concrete (Reinforced)'
        return 'Concrete'

    # Handle standalone abbreviations for Concrete Pipe
    if material_upper in ['CP', 'C.P.', 'CON', 'CONC.', 'CEMENT']:
        return 'Concrete'

    # Cast Iron variants
    if any(x in material_upper for x in ['CAST IRON', 'C.I.', 'CIP']):
        return 'Cast Iron'

    # Handle standalone CI abbreviation (but not as part of other words)
    if material_upper == 'CI':
        return 'Cast Iron'

    # Ductile Iron
    if any(x in material_upper for x in ['DUCTILE', 'DIP', 'D.I.P']):
        return 'Ductile Iron'

    # Handle standalone DI abbreviation for Ductile Iron
    if material_upper == 'DI':
        return 'Ductile Iron'

    # PVC variants (including C900 standard and ABS plastic)
    if any(x in material_upper for x in ['PVC', 'POLYVINYL', 'PVCP', 'C900', 'ABS']):
        return 'PVC'

    # HDPE / Plastic variants (including HDP/HPDE typos)
    if any(x in material_upper for x in ['HDPE', 'HPDE', 'POLYETHYLENE', 'PE', 'PLASTIC', 'HDP']):
        return 'HDPE'

    # Steel (including generic 'metal')
    if 'STEEL' in material_upper or material_upper == 'METAL':
        return 'Steel'

    # Brick (including B/C as Brick/Concrete composite)
    if 'BRICK' in material_upper or material_upper == 'B/C':
        return 'Brick'

    # Asbestos Cement (including Transite brand name)
    if any(x in material_upper for x in ['ASBESTOS', 'AC', 'A/C', 'TRANSITE']):
        return 'Asbestos Cement'

    # Fiberglass (including Techite brand name)
    if any(x in material_upper for x in ['FIBERGLASS', 'FRP', 'TECHITE']):
        return 'Fiberglass'

    # Unknown/Other (including UKN, UNK abbreviations and data entry errors)
    if any(x in material_upper for x in ['UNKNOWN', 'UKN', 'UNK', 'OTHER', 'N/A', 'NONE', 'GREASE', 'HAIR', 'BLUEBELL']):
        return 'Unknown'

    # If no match, return original (capitalized)
    return str(material).strip()


def fix_pipe_age(row):
    """
    Fix pipe ages with data quality issues.

    Common issues:
    1. Age > 1800: Installation year instead of age → calculate from spill date
    2. 150 < Age < 1800: Entered in months instead of years → divide by 12

    Args:
        row: DataFrame row with pipe_age_years and spill_date

    Returns:
        Corrected age in years
    """
    age = row['pipe_age_years']

    # If age is null or already reasonable, return as-is
    if pd.isna(age) or age <= 150:
        return age

    # If age > 1800, it's likely an installation year
    if age > 1800:
        try:
            # Extract year from spill_date
            spill_date = pd.to_datetime(row['spill_date'], errors='coerce')
            if pd.notna(spill_date):
                spill_year = spill_date.year
                calculated_age = spill_year - age
                # Sanity check: age should be positive and reasonable
                if 0 < calculated_age <= 150:
                    return calculated_age
        except:
            pass

    # If 150 < age < 1800, it's likely entered in months instead of years
    elif 150 < age < 1800:
        age_in_years = age / 12
        # Sanity check: converted age should be reasonable
        if 0 < age_in_years <= 150:
            return age_in_years

    # If we can't fix it, return as-is (will likely be filtered out)
    return age


def preprocess_data(input_path, output_path=None):
    """
    Load, filter, and score SSO data.

    Args:
        input_path: Path to input CSV file
        output_path: Path to save preprocessed data (optional)

    Returns:
        Preprocessed DataFrame with scores
    """
    print("=" * 60)
    print("PREPROCESSING SSO DATA")
    print("=" * 60)

    # Load data
    print(f"\n1. Loading data from: {input_path}")
    df = pd.read_csv(input_path)
    initial_count = len(df)
    print(f"   Initial records: {initial_count:,}")

    # Convert pipe_age_years to numeric (handle any string values)
    df['pipe_age_years'] = pd.to_numeric(df['pipe_age_years'], errors='coerce')

    # Data Quality Fixes
    print("\n2. Applying data quality fixes...")

    # Fix pipe ages (installation years -> actual ages)
    ages_before = df['pipe_age_years'].copy()
    ages_needing_fix = df[df['pipe_age_years'] > 1800].shape[0]
    print(f"   Ages that appear to be installation years (>1800): {ages_needing_fix:,}")

    if ages_needing_fix > 0:
        df['pipe_age_years_original'] = df['pipe_age_years']
        df['pipe_age_years'] = df.apply(fix_pipe_age, axis=1)
        ages_fixed = (df['pipe_age_years'] != ages_before).sum()
        print(f"   Ages successfully corrected: {ages_fixed:,}")

    # Standardize material names
    materials_before = df['pipe_material'].nunique()
    df['pipe_material_original'] = df['pipe_material']
    df['pipe_material_standardized'] = df['pipe_material'].apply(standardize_material_name)
    materials_after = df['pipe_material_standardized'].nunique()

    print(f"   Material variants before standardization: {materials_before:,}")
    print(f"   Material types after standardization: {materials_after:,}")
    print(f"   Reduction: {materials_before - materials_after:,} variants consolidated")

    # Filter null values
    print("\n3. Filtering records...")
    print(f"   Records with null pipe_age_years: {df['pipe_age_years'].isna().sum():,}")
    print(f"   Records with null pipe_material: {df['pipe_material'].isna().sum():,}")

    df_filtered = df[df['pipe_age_years'].notna() & df['pipe_material'].notna()].copy()
    filtered_count = len(df_filtered)
    print(f"   Records after filtering: {filtered_count:,}")
    print(f"   Records removed: {initial_count - filtered_count:,}")

    # Calculate scores
    print("\n4. Calculating risk scores...")
    df_filtered['age_score'] = df_filtered['pipe_age_years'].apply(calculate_age_score)
    df_filtered['material_score'] = df_filtered['pipe_material_standardized'].apply(calculate_material_score)
    df_filtered['risk_score'] = (df_filtered['age_score'] * 0.80) + (df_filtered['material_score'] * 0.20)
    df_filtered['risk_category'] = df_filtered['risk_score'].apply(calculate_risk_category)

    # Summary statistics
    print(f"   Age scores - Min: {df_filtered['age_score'].min():.1f}, "
          f"Max: {df_filtered['age_score'].max():.1f}, "
          f"Mean: {df_filtered['age_score'].mean():.1f}")
    print(f"   Material scores - Min: {df_filtered['material_score'].min():.1f}, "
          f"Max: {df_filtered['material_score'].max():.1f}, "
          f"Mean: {df_filtered['material_score'].mean():.1f}")
    print(f"   Risk scores - Min: {df_filtered['risk_score'].min():.1f}, "
          f"Max: {df_filtered['risk_score'].max():.1f}, "
          f"Mean: {df_filtered['risk_score'].mean():.1f}")

    print("\n5. Risk category distribution:")
    category_dist = df_filtered['risk_category'].value_counts().sort_index()
    for category, count in category_dist.items():
        pct = (count / filtered_count) * 100
        print(f"   {category}: {count:,} ({pct:.1f}%)")

    print("\n6. Standardized material distribution (top 10):")
    material_dist = df_filtered['pipe_material_standardized'].value_counts().head(10)
    for material, count in material_dist.items():
        pct = (count / filtered_count) * 100
        print(f"   {material:30} {count:>6,} ({pct:>5.1f}%)")

    # Save if output path provided
    if output_path:
        print(f"\n7. Saving preprocessed data to: {output_path}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_filtered.to_csv(output_path, index=False)
        print("   ✓ Saved successfully")

    print("\n" + "=" * 60)
    print("PREPROCESSING COMPLETE")
    print("=" * 60 + "\n")

    return df_filtered


if __name__ == "__main__":
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(base_dir, "data", "sso_la_county_analyzed.csv")
    output_file = os.path.join(base_dir, "data", "preprocessed_data.csv")

    # Run preprocessing
    df = preprocess_data(input_file, output_file)
