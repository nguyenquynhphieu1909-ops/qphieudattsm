# 📄 Đặc tả tính năng ML & Cơ chế Fallback (Tuần 03)

Tài liệu hướng dẫn cho Backend (Đình Phú / Huỳnh Tấn Phát) để gọi hàm dự báo ETA.

## 1. Input Features (Cần truyền vào hàm)
- `route_id` (str): Mã định danh tuyến đường (vd: `'ROUTE_01'`).
- `distance_km` (float): Chiều dài tuyến tính bằng km (từ OSRM).
- `departure_time` (str): Thời gian xuất phát chuẩn ISO (vd: `'2026-11-01T17:30:00'`).

## 2. Derived Features (Hàm tự động trích xuất)
Model ML sẽ tự động trích xuất các thông tin sau từ `departure_time`:
- `hour_of_day`: Giờ trong ngày (0-23).
- `day_of_week`: Ngày trong tuần (0=Thứ 2, 6=Chủ nhật).
- `is_weekend`: `1` nếu cuối tuần, `0` nếu ngày thường.
- `is_rush_hour`: `1` nếu vào khung giờ cao điểm (7h-9h, 17h-19h).

## 3. Cơ chế Fallback (An toàn API)
Nếu code gặp tuyến lạ chưa từng có trong tập huấn luyện (Unseen Route) hoặc model ML bị lỗi load, hàm sẽ kích hoạt **Fallback**:
- Tính toán dự phòng dựa trên vận tốc trung bình **25 km/h**.
- Thuộc tính `source` trả về sẽ là `BASELINE_FALLBACK` để báo cho Backend biết.