# Dự án DATATHON 2026 - Đội DATANIGA

Repository này chứa mã nguồn, tài liệu và cấu trúc dữ liệu cho cuộc thi Datathon 2026 của đội DATANIGA.

## 📂 Cấu trúc Thư mục (Project Structure)

Dự án được tổ chức theo chuẩn cấu trúc khoa học dữ liệu nhằm đảm bảo tính gọn gàng và dễ tái hiện:
```text
DATATHON_2026_DATANIGA/
├── data/                       # Thư mục chứa dữ liệu (không đẩy lên Git)
│   └── raw/                    # Dữ liệu thô nguyên bản từ ban tổ chức
│       ├── analytics-operational/ 
│       ├── master/             
│       ├── transaction/        
│       └── .gitkeep            
├── docs/                       # Tài liệu liên quan đến cuộc thi
│   ├── Đề thi Vòng 1.pdf       # Đề bài chính thức
├── notebooks/                  # Nơi chứa mã nguồn chính và kết quả thực nghiệm
│   ├── MCQ.ipynb               # Notebook giải quyết phần câu hỏi trắc nghiệm/phân tích
│   ├── shap_v7_ensemble.png    # Biểu đồ phân tích độ quan trọng của đặc trưng (SHAP)
│   ├── submission_v7_ensemble.csv # File kết quả dự báo cuối cùng để submit
│   └── train.ipynb             # Notebook chính để tiền xử lý, huấn luyện và tạo kết quả
├── venv/                       # Môi trường ảo Python (Virtual Environment)
├── .gitignore                  # Cấu hình bỏ qua file khi commit Git (vd: bỏ qua data/, venv/)
├── README.md                   # File hướng dẫn này
└── requirements.txt            # Danh sách các thư viện Python cần thiết