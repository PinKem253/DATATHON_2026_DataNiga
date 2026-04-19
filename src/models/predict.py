import joblib
import pandas as pd
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.versioning import get_next_submission_version, get_latest_model_version
from utils.reproducibility import SubmissionLogger


def predict_baseline(
    X_test, model_dir="../outputs/models/", model_version: Optional[int] = None
) -> Tuple:
    """
    Predict Revenue and COGS using trained models.

    Args:
        X_test: Test features
        model_dir: Base model directory
        model_version: Specific model version to use (if None, uses latest)

    Returns:
        Tuple of (pred_revenue, pred_cogs, model_version_used, model_dir_used)
    """
    if model_version is None:
        # Get latest model version
        model_version, model_version_dir = get_latest_model_version(model_dir, "model")
        if model_version is None:
            raise ValueError(f"No model versions found in {model_dir}")
    else:
        model_version_dir = os.path.join(model_dir, f"model_v{model_version}")

    revenue_model_path = os.path.join(model_version_dir, "revenue_model.pkl")
    cogs_model_path = os.path.join(model_version_dir, "cogs_model.pkl")

    if not os.path.exists(revenue_model_path) or not os.path.exists(cogs_model_path):
        raise FileNotFoundError(
            f"Model files not found in {model_version_dir}. "
            f"Expected: {revenue_model_path}, {cogs_model_path}"
        )

    revenue_model = joblib.load(revenue_model_path)
    cogs_model = joblib.load(cogs_model_path)

    pred_revenue = revenue_model.predict(X_test)
    pred_cogs = cogs_model.predict(X_test)

    return pred_revenue, pred_cogs, model_version, model_version_dir


def create_submission(
    test_df,
    pred_revenue,
    pred_cogs,
    submission_dir="../outputs/submissions/",
    model_version: Optional[int] = None,
    notes: Optional[str] = None,
    submission_version: Optional[int] = None,
) -> Tuple[str, int]:
    """
    Create versioned submission file in the required format.

    Args:
        test_df: Test dataframe with Date column
        pred_revenue: Predicted revenue values
        pred_cogs: Predicted COGS values
        submission_dir: Directory to save submissions
        model_version: Version of model used for predictions
        notes: Optional notes about this submission
        submission_version: Specific version number (if None, creates next version)

    Returns:
        Tuple of (submission_file_path, submission_version_number)
    """
    # Get next submission version
    if submission_version is None:
        version_num, output_path = get_next_submission_version(submission_dir)
    else:
        version_num = submission_version
        output_path = os.path.join(submission_dir, f"submission_v{version_num}.csv")

    os.makedirs(submission_dir, exist_ok=True)

    # Create submission dataframe
    submission = test_df[["Date"]].copy()
    submission["Revenue"] = pred_revenue
    submission["COGS"] = pred_cogs

    # Save submission file
    submission.to_csv(output_path, index=False)
    print(f"Submission v{version_num} saved to {output_path}")

    # Log submission metadata
    submission_logger = SubmissionLogger(output_path, version_num)
    if model_version is not None:
        submission_logger.set_source_model_version(model_version)
    if notes:
        submission_logger.set_notes(notes)

    submission_logger.set_metrics(
        {
            "num_rows": len(submission),
            "revenue_mean": float(pred_revenue.mean()),
            "revenue_std": float(pred_revenue.std()),
            "cogs_mean": float(pred_cogs.mean()),
            "cogs_std": float(pred_cogs.std()),
        }
    )

    metadata_file = submission_logger.save_metadata()
    print(f"Submission metadata saved to {metadata_file}")

    return output_path, version_num
