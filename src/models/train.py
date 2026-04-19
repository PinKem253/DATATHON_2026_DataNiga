from sklearn.linear_model import LinearRegression
import joblib
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.versioning import get_next_model_version
from utils.reproducibility import ReproducibilityLogger


def train_baseline_model(
    X_train,
    y_revenue,
    y_cogs,
    model_dir="../outputs/models/",
    hyperparameters: Optional[Dict[str, Any]] = None,
    create_version: bool = True,
    version_num: Optional[int] = None,
) -> Tuple[LinearRegression, LinearRegression, int, str]:
    """
    Train baseline Linear Regression models for Revenue and COGS.

    Args:
        X_train: Training features
        y_revenue: Revenue labels
        y_cogs: COGS labels
        model_dir: Directory to save models
        hyperparameters: Dictionary of hyperparameters (optional)
        create_version: Whether to create a versioned model directory
        version_num: Specific version number to use (if None, creates next version)

    Returns:
        Tuple of (revenue_model, cogs_model, version_number, model_directory)
    """
    os.makedirs(model_dir, exist_ok=True)

    # Get versioning if requested
    if create_version:
        if version_num is None:
            version_num, model_version_dir = get_next_model_version(model_dir, "model")
        else:
            model_version_dir = os.path.join(model_dir, f"model_v{version_num}")

        os.makedirs(model_version_dir, exist_ok=True)

        # Initialize reproducibility logger
        logger = ReproducibilityLogger(model_version_dir, version_num)

        # Log hyperparameters
        if hyperparameters is None:
            hyperparameters = {
                "model_type": "LinearRegression",
                "fit_intercept": True,
            }
        logger.log_hyperparameters(hyperparameters)

        logger.log_message(f"Starting training for model version {version_num}")
    else:
        logger = None
        model_version_dir = model_dir
        version_num = 0

    # Train Revenue model
    revenue_model = LinearRegression()
    revenue_model.fit(X_train, y_revenue)

    # Train COGS model
    cogs_model = LinearRegression()
    cogs_model.fit(X_train, y_cogs)

    # Save models
    revenue_model_path = os.path.join(model_version_dir, "revenue_model.pkl")
    cogs_model_path = os.path.join(model_version_dir, "cogs_model.pkl")

    joblib.dump(revenue_model, revenue_model_path)
    joblib.dump(cogs_model, cogs_model_path)

    if logger:
        logger.log_message(f"Revenue model saved to {revenue_model_path}")
        logger.log_message(f"COGS model saved to {cogs_model_path}")

        # Log training metrics (R² scores)
        train_metrics = {
            "revenue_r2_score": revenue_model.score(X_train, y_revenue),
            "cogs_r2_score": cogs_model.score(X_train, y_cogs),
            "n_features": X_train.shape[1],
            "n_samples": X_train.shape[0],
        }
        logger.log_metrics(train_metrics, stage="training")
        logger.save_metadata()
        logger.log_message(f"Training complete for model version {version_num}")

    return revenue_model, cogs_model, version_num, model_version_dir
