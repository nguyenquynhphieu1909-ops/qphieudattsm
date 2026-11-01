# 🚚 Smart Logistics - ML Travel Time Prediction (ETA)

Mô hình Machine Learning dự báo thời gian di chuyển (Travel Time / ETA) hỗ trợ lựa chọn tuyến đường giao hàng trên một số hành lang giao thông tại TP.HCM.

---

## 📌 Tổng quan Tuần 02
- **Tác giả:** Nguyễn Quỳnh Phiếu
- **Nhiệm vụ:** Tiền xử lý dữ liệu, xây dựng Baseline Model, huấn luyện Random Forest Regressor và đóng gói Pipeline (`.joblib`).
- **Dữ liệu huấn luyện:** `trips_ml_v1.csv`

---

## 📊 Kết quả Huấn luyện & Đánh giá Model

| Chỉ số đánh giá | Baseline Model | Random Forest Regressor | Đánh giá |
| :--- | :--- | :--- | :--- |
| **MAE (Sai số trung bình)** | **5.63 phút** | **2.99 phút** | Giảm 46.89% sai số |
| **Tỷ lệ sai số $\le 10$ phút** | **90.9%** | **100.0%** | Đạt mục tiêu đồ án |
| **Độ phù hợp $R^2$ Score** | *N/A* | **0.836** | Giải thích tốt 83.6% dữ liệu |

---

## 📁 Cấu trúc Thư mục

```text
DATT_Smartlogistics/
├── trips_ml_v1.csv            # Dữ liệu chuyến đi thực tế & mô phỏng
├── baseline.py                # Script chạy mô hình Baseline
├── train_pipeline.py          # Script huấn luyện ML & đóng gói Pipeline
├── rf_model_pipeline.joblib   # Model Pipeline đã đóng gói cho Backend
└── .gitignore                 # File cấu hình bỏ qua thư mục rác Git
---

## 🚀 Báo Cáo Tiến Độ Tuần 03: Tích Hợp Inference & Data

### 📊 1. Kết Quả Huấn Luyện Mô Hình (ETA Model)
Mô hình **Random Forest** đã được tái huấn luyện thành công với bộ dữ liệu sạch `ml_features.csv` (741 chuyến đi) do Thảo Vy chuẩn bị.

| Chỉ số kiểm định | Kết quả | Đánh giá |
| :--- | :---: | :--- |
| **MAE** (Sai số trung bình) | **0.94 phút** | 🟢 Cực kỳ chính xác |
| **Tỷ lệ sai số < 10 phút** | **99.3%** | 🟢 Vượt chỉ tiêu |
| **Độ phù hợp (R² Score)** | **0.893** | 🟢 Mô hình khớp dữ liệu tốt |

*📍 File Pipeline mới nhất đã được lưu tại: `rf_model_pipeline.joblib`*

### 🛠️ 2. Dịch Vụ Inference & Cấu Trúc Backend
Đã xây dựng xong module dự báo thời gian thực (`ml/inference/predict_eta.py`) để Backend (Đình Phú, Tấn Phát) dễ dàng gọi API.

**Cú pháp gọi hàm:**
```python
from ml.inference.predict_eta import predict_eta

# Trả về dict chứa ETA và source (ML_RANDOM_FOREST hoặc FALLBACK)
result = predict_eta(
    route_id="ROUTE_01", 
    distance_km=8.5, 
    departure_time="2026-11-01T17:30:00"
)