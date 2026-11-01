# 🚚 Smart Logistics - Hệ thống Dự báo Thời gian đến (ETA)

Dự án xây dựng hệ thống Machine Learning dự báo chính xác thời gian hoàn thành chuyến đi (ETA) cho các đơn hàng logistics, tích hợp dự phòng rủi ro và API thời gian thực.

---

## 📂 Cấu trúc Thư mục (ML & Inference)

```text
DATT_Smartlogistics/
├── ml/
│   └── inference/
│       ├── __init__.py
│       └── predict_eta.py      # Hàm dự báo chính cho Backend gọi (có Fallback)
├── baseline.py                 # Script chạy mô hình Baseline
├── feature_spec.md             # Tài liệu đặc tả tính năng & API cho Backend
├── ml_features.csv             # Dữ liệu chuyến đi thực tế & mô phỏng (Tuần 3)
├── rf_model_pipeline.joblib    # Model Pipeline (Random Forest) đã đóng gói
├── test_inference.py           # Script kiểm thử hàm dự báo
├── train_pipeline.py           # Script huấn luyện ML & đóng gói Pipeline
└── .gitignore                  # File cấu hình bỏ qua thư mục rác Git