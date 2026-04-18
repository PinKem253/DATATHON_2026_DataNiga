import os
import zipfile
import subprocess
import shutil
import pandas as pd

# =========================
# CONFIG
# =========================
COMPETITION_NAME = "datathon-2026-round-1"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
KAGGLE_CONFIG_PATH = PROJECT_ROOT  

# Định nghĩa cấu trúc thư mục con và các file tương ứng
FILE_MAPPING = {
    "master": [
        "products.csv", "customers.csv", "geography.csv", "promotions.csv"
    ],
    "transaction": [
        "orders.csv", "order_items.csv", "payments.csv", "shipments.csv", "returns.csv", "reviews.csv"
    ],
    "analytics-operational": [
        "web_traffic.csv", "sales.csv", "sales_test.csv", "sample_submission.csv", "inventory.csv", "inventory_enhanced.csv"
    ]
}

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
    # Set biến môi trường để Kaggle CLI nhận config
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
            os.remove(path) # Xóa file zip cho nhẹ máy

def organize_data():
    print("📁 Organizing files into subdirectories...")
    for folder, files in FILE_MAPPING.items():
        folder_path = os.path.join(DATA_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        for file in files:
            source = os.path.join(DATA_DIR, file)
            destination = os.path.join(folder_path, file)
            
            # Nếu file đang nằm ở ngoài data/raw, hãy chuyển nó vào thư mục con
            if os.path.exists(source):
                shutil.move(source, destination)

def data_exists():
    # Quét cả thư mục con để xem có file CSV nào không
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
        organize_data() # Gọi hàm sắp xếp sau khi giải nén
        print("✅ Data downloaded and organized successfully.")
    else:
        print("✅ Data already exists. Skipping download.")

# =========================
# LOAD FUNCTIONS
# =========================

def load_csv(folder, filename):
    """
    Load file theo cấu trúc mới: load_csv('master', 'products.csv')
    """
    path = os.path.join(DATA_DIR, folder, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {filename} not found in {DATA_DIR}/{folder}")

    # Đảm bảo mã định danh không bị mất số 0 ở đầu khi load
    # Chuyển ID thành kiểu chuỗi thay vì integer
    return pd.read_csv(path, dtype={
        'product_id': str, 'customer_id': str, 'zip': str, 
        'promo_id': str, 'order_id': str
    })

def load_all():
    prepare_data()

    data = {}
    # Dùng os.walk để đi sâu vào từng thư mục con lấy file
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".csv"):
                # Load và lưu vào dict với key là tên file (VD: data['products.csv'])
                file_path = os.path.join(root, file)
                
                # Ép kiểu chuỗi cho các trường ID phổ biến để bảo toàn dữ liệu
                data[file] = pd.read_csv(file_path, dtype={
                    'product_id': str, 'customer_id': str, 'zip': str, 
                    'promo_id': str, 'order_id': str
                })

    print(f"✅ Loaded {len(data)} files: {list(data.keys())}")
    return data

if __name__ == "__main__":
    # Test script
    prepare_data()
    # data_dict = load_all()