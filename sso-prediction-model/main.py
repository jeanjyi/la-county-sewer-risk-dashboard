"""
Main orchestrator for SSO Pipe Failure Prediction Model.
Runs preprocessing, validation, and prediction generation in sequence.
"""

import os
import sys
import time
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.preprocess import preprocess_data
from src.model import validate_risk_scoring, save_metrics
from src.predict import generate_predictions, save_results, generate_feature_importance
import pandas as pd


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    """
    Run the complete SSO risk scoring pipeline.
    """
    start_time = time.time()

    print_header("SSO PIPE FAILURE PREDICTION MODEL")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, "data", "sso_la_county_analyzed.csv")
    preprocessed_file = os.path.join(base_dir, "data", "preprocessed_data.csv")
    results_file = os.path.join(base_dir, "outputs", "model_results.csv")
    metrics_file = os.path.join(base_dir, "outputs", "model_metrics.json")
    importance_file = os.path.join(base_dir, "outputs", "feature_importance.csv")

    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        print("Please ensure sso_la_county_analyzed.csv is in the data/ directory")
        return 1

    try:
        # Step 1: Preprocessing
        print_header("STEP 1/3: DATA PREPROCESSING")
        df_original = pd.read_csv(input_file)
        total_records = len(df_original)

        df_preprocessed = preprocess_data(input_file, preprocessed_file)
        records_scored = len(df_preprocessed)
        records_missing = total_records - records_scored

        # Step 2: Model Validation
        print_header("STEP 2/3: MODEL VALIDATION")
        metrics = validate_risk_scoring(df_preprocessed)
        save_metrics(metrics, metrics_file, total_records, records_scored, records_missing)

        # Step 3: Generate Predictions
        print_header("STEP 3/3: GENERATE PREDICTIONS")
        df_results = generate_predictions(df_preprocessed)
        save_results(df_results, results_file)

        # Save feature importance
        print(f"\nSaving feature importance to: {importance_file}")
        importance_df = generate_feature_importance()
        importance_df.to_csv(importance_file, index=False)
        print("   ✓ Feature importance saved")

        # Final Summary
        print_header("PIPELINE COMPLETE")

        elapsed_time = time.time() - start_time

        print("OUTPUT FILES GENERATED:")
        print(f"   1. {preprocessed_file}")
        print(f"      └─ Preprocessed data with risk scores")
        print(f"\n   2. {results_file}")
        print(f"      └─ Final predictions ready for Power BI")
        print(f"\n   3. {metrics_file}")
        print(f"      └─ Validation metrics and correlations")
        print(f"\n   4. {importance_file}")
        print(f"      └─ Feature weights (80% Age / 20% Material)")

        print(f"\nFINAL STATISTICS:")
        print(f"   Total records processed: {total_records:,}")
        print(f"   Records scored: {records_scored:,}")
        print(f"   Records filtered out: {records_missing:,}")
        print(f"   Success rate: {(records_scored/total_records)*100:.1f}%")

        print(f"\nExecution time: {elapsed_time:.2f} seconds")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print("\n" + "=" * 70)
        print("  READY FOR POWER BI IMPORT")
        print("=" * 70 + "\n")

        return 0

    except Exception as e:
        print(f"\nERROR: Pipeline failed with exception:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
