import os
import zipfile
import subprocess
import pandas as pd

# =========================
# CONFIG
# =========================
COMPETITION_NAME = "datathon-2026-round-1"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
KAGGLE_CONFIG_PATH = PROJECT_ROOT  

# =========================
# CORE FUNCTIONS
# =========================

def check_kaggle():
    kaggle_file = os.path.join(KAGGLE_CONFIG_PATH, "kaggle.json")
    if not os.path.exists(kaggle_file):
        raise FileNotFoundError(
            "❌ kaggle.json not found in project root!"
        )


def setup_env():
    # set biến môi trường để Kaggle CLI nhận config
    os.environ["KAGGLE_CONFIG_DIR"] = KAGGLE_CONFIG_PATH


def download_data():
    print("📥 Downloading data from Kaggle...")

    os.makedirs(DATA_DIR, exist_ok=True)

    subprocess.run([
        "kaggle", "competitions", "download",
        "-c", COMPETITION_NAME,
        "-p", DATA_DIR
    ], check=True)


def unzip_data():
    print("📦 Unzipping...")

    for file in os.listdir(DATA_DIR):
        if file.endswith(".zip"):
            path = os.path.join(DATA_DIR, file)
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(DATA_DIR)


def data_exists():
    return any(f.endswith(".csv") for f in os.listdir(DATA_DIR))


def prepare_data(force=False):
    check_kaggle()
    setup_env()

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if force or not data_exists():
        download_data()
        unzip_data()
    else:
        print("✅ Data already exists. Skipping download.")


# =========================
# LOAD FUNCTIONS
# =========================

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {filename} not found in {DATA_DIR}")

    return pd.read_csv(path)


def load_all():
    prepare_data()

    data = {}
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            data[file] = pd.read_csv(os.path.join(DATA_DIR, file))

    print(f"✅ Loaded files: {list(data.keys())}")
    return data

if __name__ == "__main__":
    data = load_all()
    
    