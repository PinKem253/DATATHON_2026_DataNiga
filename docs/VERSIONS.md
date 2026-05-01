# BÁO CÁO KỸ THUẬT: BASELINE THUẦN THỜI GIAN (PURE TIME-SERIES)

## 1. Triết lý thiết kế (Design Philosophy)
Sau khi đánh giá sự thiếu hụt của dữ liệu ngoại sinh (số lượng đơn hàng, lượt truy cập web) trong giai đoạn dự báo tương lai (2023 - 2024), nhóm quyết định áp dụng triết lý thiết kế Bất biến với tương lai (Deterministic).

Baseline này từ bỏ việc dùng các chỉ số giao dịch quá khứ (Lag features) để tránh rò rỉ dữ liệu (Data Leakage), thay vào đó chỉ tập trung khai thác các quy luật nội tại của trục thời gian nhằm xây dựng một mốc cản chuẩn xác.

## 2. Chi tiết Feature Engineering (Trích xuất Đặc trưng)
Mô hình hiện tại chỉ sử dụng dữ liệu từ file `sales.csv` và biến đổi duy nhất cột `Date` thành hai nhóm đặc trưng cốt lõi:

| Nhóm Đặc trưng | Tên Feature | Ý nghĩa & Giải thích (Why we use it) |
| --- | --- | --- |
| **Tính Chu kỳ (Seasonality)** | `day_of_week` | Bắt nhịp mua sắm trong tuần. Ví dụ: Cuối tuần có thể cao hơn ngày thường. |
| | `day_of_month` | Bắt hiệu ứng "ngày nhận lương" hoặc các chiến dịch sale cố định hàng tháng (ví dụ: ngày 15, ngày 25). |
| | `month`, `quarter` | Nắm bắt tính mùa vụ dài hạn. Khách hàng E-commerce thường chi tiêu mạnh vào Quý 4 (mùa lễ hội, cuối năm). |
| | `is_weekend` | Biến cờ (0/1) giúp thuật toán phân tách rõ ràng hành vi mua sắm cuối tuần. |
| **Tính Xu hướng (Trend)** | `days_since_start` | Đây là biến số đếm tịnh tiến từ ngày đầu tiên có dữ liệu (0, 1, 2...). Nó đóng vai trò như một trục tọa độ, giúp mô hình nhận biết sự phát triển quy mô (Scale) của doanh nghiệp qua từng năm. |

## 3. Chiến lược Thuật toán (Modeling Strategy)
- **Tối ưu hóa siêu tham số (Hyperparameter Tuning):** Sử dụng Optuna kết hợp TimeSeriesSplit (Cross-validation dạng chuỗi) để dò tìm cấu hình tốt nhất cho mô hình mà không phá vỡ tính thứ tự của thời gian.
- **Học máy & Tập hợp (Ensemble):** Sử dụng song song hai thuật toán Gradient Boosting mạnh nhất hiện nay là XGBoost và LightGBM. Kết quả dự báo là trung bình cộng dự báo từ cả hai mô hình nhằm làm mượt kết quả và giảm thiểu phương sai (Variance).