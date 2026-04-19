"""
Reproducibility tracking for models and experiments.
Logs hyperparameters, metrics, environment info, and metadata.
"""

import os
import json
import sys
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import subprocess


class ReproducibilityLogger:
    """Logs model training information for reproducibility."""

    def __init__(self, version_dir: str, version_num: int):
        """
        Initialize reproducibility logger.

        Args:
            version_dir: Directory to store metadata files
            version_num: Version number of the model
        """
        self.version_dir = version_dir
        self.version_num = version_num
        self.metadata = {
            "version": version_num,
            "timestamp": datetime.now().isoformat(),
            "hyperparameters": {},
            "training_metrics": {},
            "environment": self._get_environment_info(),
        }

        os.makedirs(version_dir, exist_ok=True)

        # Setup logging
        self.logger = self._setup_logging()

    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information for reproducibility."""
        info = {
            "python_version": sys.version,
            "timestamp": datetime.now().isoformat(),
        }

        # Try to get git information
        try:
            git_commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
            ).strip()
            git_branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True,
            ).strip()
            info["git_commit"] = git_commit
            info["git_branch"] = git_branch
        except:
            info["git_commit"] = "Not available"
            info["git_branch"] = "Not available"

        return info

    def _setup_logging(self) -> logging.Logger:
        """Setup logging to both file and console."""
        logger = logging.getLogger(f"version_v{self.version_num}")
        logger.setLevel(logging.DEBUG)

        # File handler
        log_file = os.path.join(
            self.version_dir, f"training_log_v{self.version_num}.txt"
        )
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    def log_hyperparameters(self, hyperparameters: Dict[str, Any]) -> None:
        """
        Log hyperparameters.

        Args:
            hyperparameters: Dictionary of hyperparameters
        """
        self.metadata["hyperparameters"] = hyperparameters
        self.logger.info(f"Hyperparameters: {json.dumps(hyperparameters, indent=2)}")

    def log_metric(self, metric_name: str, value: Any, stage: str = "training") -> None:
        """
        Log a single metric.

        Args:
            metric_name: Name of the metric
            value: Value of the metric
            stage: Stage of training (training, validation, test)
        """
        key = f"{stage}_{metric_name}"
        self.metadata["training_metrics"][key] = value
        self.logger.info(f"{key}: {value}")

    def log_metrics(self, metrics: Dict[str, Any], stage: str = "training") -> None:
        """
        Log multiple metrics at once.

        Args:
            metrics: Dictionary of metrics
            stage: Stage of training (training, validation, test)
        """
        for metric_name, value in metrics.items():
            self.log_metric(metric_name, value, stage)

    def log_message(self, message: str, level: str = "info") -> None:
        """
        Log a custom message.

        Args:
            message: Message to log
            level: Logging level (debug, info, warning, error)
        """
        log_func = getattr(self.logger, level.lower())
        log_func(message)

    def save_metadata(self) -> str:
        """
        Save metadata to JSON file.

        Returns:
            Path to saved metadata file
        """
        metadata_file = os.path.join(
            self.version_dir, f"metadata_v{self.version_num}.json"
        )

        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

        self.logger.info(f"Metadata saved to {metadata_file}")
        return metadata_file

    def get_metadata(self) -> Dict[str, Any]:
        """Get current metadata."""
        return self.metadata


class SubmissionLogger:
    """Logs submission information for tracking."""

    def __init__(self, submission_path: str, version_num: int):
        """
        Initialize submission logger.

        Args:
            submission_path: Path to submission file
            version_num: Version number
        """
        self.submission_path = submission_path
        self.version_num = version_num
        self.submission_dir = os.path.dirname(submission_path)
        self.metadata = {
            "version": version_num,
            "submission_file": os.path.basename(submission_path),
            "timestamp": datetime.now().isoformat(),
            "path": submission_path,
        }

    def set_source_model_version(self, model_version: int) -> None:
        """Set the source model version used for this submission."""
        self.metadata["source_model_version"] = model_version

    def set_notes(self, notes: str) -> None:
        """Add notes about this submission."""
        self.metadata["notes"] = notes

    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        """Set metrics associated with this submission."""
        self.metadata["metrics"] = metrics

    def save_metadata(self) -> str:
        """
        Save submission metadata to JSON file.

        Returns:
            Path to saved metadata file
        """
        metadata_file = os.path.join(
            self.submission_dir, f"submission_v{self.version_num}_metadata.json"
        )

        with open(metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

        return metadata_file

    def get_metadata(self) -> Dict[str, Any]:
        """Get current metadata."""
        return self.metadata


def load_model_metadata(version_dir: str, version_num: int) -> Optional[Dict[str, Any]]:
    """
    Load metadata for a specific model version.

    Args:
        version_dir: Base model directory
        version_num: Version number

    Returns:
        Metadata dictionary or None if not found
    """
    metadata_file = os.path.join(
        version_dir, f"model_v{version_num}", f"metadata_v{version_num}.json"
    )

    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f)

    return None


def load_submission_metadata(
    submission_dir: str, version_num: int
) -> Optional[Dict[str, Any]]:
    """
    Load metadata for a specific submission version.

    Args:
        submission_dir: Submission directory
        version_num: Version number

    Returns:
        Metadata dictionary or None if not found
    """
    metadata_file = os.path.join(
        submission_dir, f"submission_v{version_num}_metadata.json"
    )

    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f)

    return None
