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


Tiến hành đánh giá khả năng nội suy của mô hình Tuần 03 khi áp dụng cho bài toán **thời gian thực** (xe đang di chuyển). Thử nghiệm trên 19.385 điểm tọa độ GPS mô phỏng (`gps_simulated.csv`) của Tuần 04.

| Kịch bản đánh giá | MAE (Sai số) | Kết luận |
| :--- | :---: | :--- |
| **Dự báo chặng đường còn lại** (Dùng model Tuần 03) | **36.21 phút** | 🔴 Sai số quá cao. Mô hình mất kiểm soát do học dựa trên tổng lộ trình ban đầu. |
| **Baseline OSRM** (Chế độ dự phòng) | **N/A** | 🟢 Chuyển sang dùng OSRM làm fallback để duy trì độ chính xác. |

**🛠️ Cập nhật hệ thống Inference:**
- Bổ sung hàm `predict_remaining_eta()` chuyên dụng cho Real-time.
- Cài đặt cơ chế bảo vệ: Khi Backend gọi API dự báo chặng còn lại, hệ thống sẽ **tự động bypass mô hình Tuần 03** và sử dụng trực tiếp Baseline OSRM để tránh sai số hiển thị cho tài xế.
- Bàn giao API an toàn cho team Backend xử lý Logic chậm trễ (Delay Risk).