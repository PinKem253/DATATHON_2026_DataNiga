"""
Versioning utility for managing model and submission versions.
"""

import os
import json
import re
from pathlib import Path
from typing import Optional, Tuple


class VersionManager:
    """Manages versioning for models and submissions."""

    @staticmethod
    def get_next_version(
        directory: str, prefix: str, extension: str = ""
    ) -> Tuple[int, str]:
        """
        Get the next version number for a given directory and prefix.

        Args:
            directory: Directory to search for existing versions
            prefix: Prefix of files to match (e.g., 'submission', 'model')
            extension: File extension to match (e.g., '.csv', '.pkl')

        Returns:
            Tuple of (next_version_number, next_version_filename)
        """
        os.makedirs(directory, exist_ok=True)

        # Find all files matching the pattern
        pattern = rf"{prefix}_v(\d+){re.escape(extension)}"
        existing_versions = []

        for filename in os.listdir(directory):
            match = re.match(pattern, filename)
            if match:
                existing_versions.append(int(match.group(1)))

        next_version = max(existing_versions) + 1 if existing_versions else 0
        filename = f"{prefix}_v{next_version}{extension}"

        return next_version, filename

    @staticmethod
    def get_model_path(
        model_dir: str, version: Optional[int] = None, model_name: str = "model"
    ) -> str:
        """
        Get path for a versioned model directory or file.

        Args:
            model_dir: Base model directory
            version: Version number. If None, gets the latest version
            model_name: Name of the model (e.g., 'revenue_model', 'cogs_model')

        Returns:
            Path to the model directory/file
        """
        if version is None:
            # Get latest version
            version, _ = VersionManager.get_next_version(model_dir, model_name, "")
            version = max(0, version - 1)

        model_version_dir = os.path.join(model_dir, f"{model_name}_v{version}")
        return model_version_dir

    @staticmethod
    def get_submission_path(submission_dir: str, version: Optional[int] = None) -> str:
        """
        Get path for a versioned submission file.

        Args:
            submission_dir: Base submission directory
            version: Version number. If None, gets the next version

        Returns:
            Path to the submission file
        """
        if version is None:
            version, filename = VersionManager.get_next_version(
                submission_dir, "submission", ".csv"
            )
        else:
            filename = f"submission_v{version}.csv"

        return os.path.join(submission_dir, filename), version

    @staticmethod
    def list_versions(directory: str, prefix: str, extension: str = "") -> list:
        """
        List all versions found in a directory.

        Args:
            directory: Directory to search
            prefix: Prefix to match
            extension: File extension to match

        Returns:
            List of version numbers, sorted
        """
        if not os.path.exists(directory):
            return []

        pattern = rf"{prefix}_v(\d+){re.escape(extension)}"
        versions = []

        for filename in os.listdir(directory):
            match = re.match(pattern, filename)
            if match:
                versions.append(int(match.group(1)))

        return sorted(versions)


def get_next_submission_version(submission_dir: str) -> Tuple[int, str]:
    """
    Convenience function to get next submission version.

    Args:
        submission_dir: Directory containing submissions

    Returns:
        Tuple of (version_number, full_filepath)
    """
    version, filename = VersionManager.get_next_version(
        submission_dir, "submission", ".csv"
    )
    filepath = os.path.join(submission_dir, filename)
    return version, filepath


def get_next_model_version(
    model_dir: str, model_name: str = "model"
) -> Tuple[int, str]:
    """
    Convenience function to get next model version directory.

    Args:
        model_dir: Base model directory
        model_name: Name of the model type

    Returns:
        Tuple of (version_number, version_directory_path)
    """
    version, _ = VersionManager.get_next_version(model_dir, model_name, "")
    model_path = os.path.join(model_dir, f"{model_name}_v{version}")
    return version, model_path


def get_latest_model_version(
    model_dir: str, model_name: str = "model"
) -> Tuple[Optional[int], Optional[str]]:
    """
    Get the latest model version.

    Args:
        model_dir: Base model directory
        model_name: Name of the model type

    Returns:
        Tuple of (version_number, version_directory_path) or (None, None) if no versions exist
    """
    versions = VersionManager.list_versions(model_dir, model_name, "")
    if not versions:
        return None, None

    latest_version = max(versions)
    model_path = os.path.join(model_dir, f"{model_name}_v{latest_version}")
    return latest_version, model_path
