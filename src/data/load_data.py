import os
import zipfile
import subprocess
import shutil
import pandas as pd

COMPETITION_NAME = "datathon-2026-round-1"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
KAGGLE_CONFIG_PATH = PROJECT_ROOT

FILE_MAPPING = {
    "master": ["products.csv", "customers.csv", "geography.csv", "promotions.csv"],
    "transaction": [
        "orders.csv",
        "order_items.csv",
        "payments.csv",
        "shipments.csv",
        "returns.csv",
        "reviews.csv",
    ],
    "analytics-operational": [
        "web_traffic.csv",
        "sales.csv",
        "sales_test.csv",
        "sample_submission.csv",
        "inventory.csv",
        "inventory_enhanced.csv",
    ],
}


def check_kaggle():
    kaggle_file = os.path.join(KAGGLE_CONFIG_PATH, "kaggle.json")
    if not os.path.exists(kaggle_file):
        raise FileNotFoundError("❌ kaggle.json not found in project root!")


def setup_env():
    os.environ["KAGGLE_CONFIG_DIR"] = KAGGLE_CONFIG_PATH


def download_data():
    print("📥 Downloading data from Kaggle...")
    os.makedirs(DATA_DIR, exist_ok=True)
    subprocess.run(
        ["kaggle", "competitions", "download", "-c", COMPETITION_NAME, "-p", DATA_DIR],
        check=True,
    )


def unzip_data():
    print("📦 Unzipping...")
    for file in os.listdir(DATA_DIR):
        if file.endswith(".zip"):
            path = os.path.join(DATA_DIR, file)
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(DATA_DIR)
            os.remove(path)


def organize_data():
    print("📁 Organizing files into subdirectories...")
    for folder, files in FILE_MAPPING.items():
        folder_path = os.path.join(DATA_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            source = os.path.join(DATA_DIR, file)
            destination = os.path.join(folder_path, file)

            if os.path.exists(source):
                shutil.move(source, destination)


def data_exists():
    for root, _, files in os.walk(DATA_DIR):
        if any(f.endswith(".csv") for f in files):
            return True
    return False


def prepare_data(force=False):
    check_kaggle()
    setup_env()

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if force or not data_exists():
        download_data()
        unzip_data()
        organize_data()
        print("✅ Data downloaded and organized successfully.")
    else:
        print("✅ Data already exists. Skipping download.")


def load_csv(folder, filename):
    """
    Load file theo cấu trúc mới: load_csv('master', 'products.csv')
    """
    path = os.path.join(DATA_DIR, folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {filename} not found in {DATA_DIR}/{folder}")

    return pd.read_csv(
        path,
        dtype={
            "product_id": str,
            "customer_id": str,
            "zip": str,
            "promo_id": str,
            "order_id": str,
        },
    )


def load_sales_data(train=True):
    """
    Load sales data for training or testing.
    If train=True, load sales.csv (train data).
    If train=False, load sales_test.csv (test data), but since test doesn't have labels, use sample_submission.csv for format.
    """
    if train:
        return load_csv("analytics-operational", "sales.csv")
    else:
        # For test, we need to predict, so load sample_submission.csv as template
        return load_csv("analytics-operational", "sample_submission.csv")


def load_all():
    prepare_data()

    data = {}
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                data[file] = pd.read_csv(
                    file_path,
                    dtype={
                        "product_id": str,
                        "customer_id": str,
                        "zip": str,
                        "promo_id": str,
                        "order_id": str,
                    },
                )

    print(f"✅ Loaded {len(data)} files: {list(data.keys())}")
    return data


if __name__ == "__main__":
    # Test script
    # prepare_data()
    data_dict = load_all()
