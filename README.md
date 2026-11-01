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
## 🚀 Cập nhật Tuần 03 - Tích hợp Inference & Data
- **Mô hình & Dữ liệu:** Đã huấn luyện lại Random Forest với dữ liệu `ml_features.csv` (741 chuyến đi) từ Thảo Vy. Sai số trung bình (MAE) đạt cực thấp: **0.94 phút**. File model cập nhật tại `rf_model_pipeline.joblib`.
- **Dịch vụ Inference:** Đã thêm module `ml/inference/predict_eta.py` chứa hàm `predict_eta(route_id, distance_km, departure_time)` để Backend gọi API dự báo thời gian.
- **Cơ chế Fallback (Bảo vệ API):** Tự động xử lý các tuyến đường lạ (chưa có trong tập huấn luyện) hoặc lỗi dữ liệu bằng cách tính dự phòng theo vận tốc trung bình (25km/h).
- **Tài liệu API:** Backend xem chi tiết cấu trúc truyền dữ liệu tại `feature_spec.md`.