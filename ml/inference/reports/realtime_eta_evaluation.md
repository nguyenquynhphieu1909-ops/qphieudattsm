# Báo cáo Đánh giá Mô hình ETA Thời gian thực (Real-time)

## 1. Mục tiêu Đánh giá
Kiểm tra xem mô hình Random Forest (Tuần 03) có khả năng dự báo thời gian còn lại (remaining ETA) khi xe đang di chuyển hay không.

## 2. Dữ liệu Thử nghiệm
- **Nguồn dữ liệu:** `gps_simulated.csv` do Data (Thảo Vy) cung cấp.
- **Số lượng mẫu hợp lệ:** Đã trích xuất và lọc các điểm tọa độ GPS chưa tới đích để tiến hành đánh giá.
- **Tính toán nhãn (Ground Truth):** Thời gian thực tế còn lại được nội suy tự động từ timestamp của điểm GPS hiện tại đến timestamp kết thúc chuyến đi.

## 3. Kết quả Đánh giá
- **Chỉ số đo lường:** MAE (Mean Absolute Error)
- **Kết quả:** **36.21 phút**

## 4. Phân tích và Kết luận
- **Nguyên nhân sai số cao:** Mô hình Tuần 03 được huấn luyện để nhìn nhận tổng thể chuyến đi từ điểm xuất phát (tổng quãng đường). Khi nạp "quãng đường còn lại" ở giữa chặng, mô hình hiểu nhầm đây là một chuyến đi hoàn toàn mới với độ dài ngắn, dẫn đến các đặc trưng nội suy bị sai lệch nghiêm trọng so với thực tế.
- **Hành động (Task 4.3.3):** Mô hình cũ **KHÔNG PHÙ HỢP** cho bài toán Real-time. Chuyển sang kích hoạt cơ chế Fallback (Baseline OSRM) hoặc vận tốc trung bình (25km/h) để đảm bảo hệ thống API trả về kết quả an toàn cho Backend.