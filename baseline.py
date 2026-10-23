import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
import os

def create_mock_data(file_path="sample_trips.csv", n_samples=1000):
    """Hàm tự động tạo bộ dữ liệu giả lập giao thông TP.HCM nếu chưa có file"""
    np.random.seed(42)
    # 3 tuyến đường giả định tại TP.HCM
    routes = ['Tuyen_A_TanBinh_Q1', 'Tuyen_B_Q7_Q1', 'Tuyen_C_ThuDuc_BinhThanh']
    route_distances = {'Tuyen_A_TanBinh_Q1': 6.5, 'Tuyen_B_Q7_Q1': 8.0, 'Tuyen_C_ThuDuc_BinhThanh': 12.0}
    
    # Sinh thời gian xuất phát liên tục trong 1 tháng
    start_dates = pd.date_range(start='2026-10-01 06:00:00', periods=n_samples, freq='35min')
    
    data = []
    for dt in start_dates:
        route = np.random.choice(routes)
        dist = route_distances[route] + np.random.uniform(-0.3, 0.3) # Nhiễu khoảng cách do sai số GPS
        
        # Mô phỏng tốc độ giao thông TP.HCM (km/h)
        hour = dt.hour
        is_rush_hour = hour in [7, 8, 17, 18]
        is_weekend = dt.weekday() >= 5
        
        if is_rush_hour and not is_weekend:
            speed_kmh = np.random.uniform(12, 18)  # Kẹt xe
        elif is_weekend:
            speed_kmh = np.random.uniform(25, 35)  # Cuối tuần đường vắng
        else:
            speed_kmh = np.random.uniform(20, 28)  # Giờ bình thường
            
        # Tính thời gian thực tế = (Quãng đường / Tốc độ) * 60 phút + Nhiễu ngẫu nhiên
        actual_time = (dist / speed_kmh) * 60 + np.random.normal(0, 4) 
        actual_time = max(actual_time, 5) # Tối thiểu 5 phút
        
        data.append({
            'trip_id': f"TRIP_{len(data)+1:04d}",
            'route_id': route,
            'distance_km': round(dist, 2),
            'departure_time': dt,
            'actual_travel_time': round(actual_time, 2)
        })
        
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"[HỆ THỐNG] Đã tạo file dữ liệu giả lập thành công tại: {file_path}")

def main():
    file_path = "sample_trips.csv"
    
    # 1. Tạo dữ liệu giả lập nếu chưa nhận được file từ bạn Thảo Vy
    if not os.path.exists(file_path):
        create_mock_data(file_path)
        
    # 2. Đọc và tiền xử lý dữ liệu
    print("\n--- BƯỚC 1: ĐỌC VÀ TRÍCH XUẤT ĐẶC TRƯNG ---")
    df = pd.read_csv(file_path)
    df['departure_time'] = pd.to_datetime(df['departure_time'])
    
    # QUAN TRỌNG: Sắp xếp dữ liệu theo trình tự thời gian trước khi chia Train/Test
    df = df.sort_values('departure_time').reset_index(drop=True)
    
    # Trích xuất các biến thời điểm (Sẵn có lúc dự báo)
    df['hour_of_day'] = df['departure_time'].dt.hour
    df['day_of_week'] = df['departure_time'].dt.dayofweek
    
    print(f"Tổng số dữ liệu: {len(df)} chuyến đi.")
    
    # 3. Chia tập dữ liệu Train / Test (Tỉ lệ 80/20)
    print("\n--- BƯỚC 2: CHIA TẬP DỮ LIỆU TRAIN/TEST ---")
    train_size = int(len(df) * 0.8)
    train_df = df.iloc[:train_size].copy()
    test_df = df.iloc[train_size:].copy()
    print(f"Số lượng Train (80%): {len(train_df)}")
    print(f"Số lượng Test (20%): {len(test_df)}")
    
    # 4. Tính toán mô hình Baseline
    print("\n--- BƯỚC 3: XÂY DỰNG MÔ HÌNH BASELINE ---")
    # Theo lý thuyết: Baseline = Thời gian di chuyển trung bình theo TUYẾN trên tập Train
    baseline_lookup = train_df.groupby('route_id')['actual_travel_time'].mean().reset_index()
    baseline_lookup.rename(columns={'actual_travel_time': 'predicted_travel_time'}, inplace=True)
    
    # Áp dụng dự báo lên tập Test bằng cách merge (map) dữ liệu
    test_df = test_df.merge(baseline_lookup, on='route_id', how='left')
    
    # Xử lý ngoại lệ: Nếu tập Test xuất hiện một tuyến đường mới toanh chưa từng có ở tập Train
    global_mean_train = train_df['actual_travel_time'].mean()
    test_df['predicted_travel_time'] = test_df['predicted_travel_time'].fillna(global_mean_train)
    
    # 5. Đánh giá chất lượng mô hình
    print("\n--- BƯỚC 4: BÁO CÁO KẾT QUẢ ĐÁNH GIÁ (EVALUATION) ---")
    y_true = test_df['actual_travel_time']
    y_pred = test_df['predicted_travel_time']
    
    # Tính sai số tuyệt đối trung bình (MAE)
    mae = mean_absolute_error(y_true, y_pred)
    
    # Tính tỷ lệ dự báo có sai số <= 10 phút
    test_df['absolute_error'] = np.abs(y_true - y_pred)
    accuracy_within_10m = (test_df['absolute_error'] <= 10).mean() * 100
    
    print(f">> 1. Chỉ số MAE (Sai số trung bình): {mae:.2f} phút")
    print(f">> 2. Tỷ lệ dự báo sai số <= 10 phút: {accuracy_within_10m:.2f}%")
    
    print("\n[Mẫu 5 dòng kết quả dự báo chi tiết trên tập Test]:")
    print(test_df[['route_id', 'departure_time', 'actual_travel_time', 'predicted_travel_time', 'absolute_error']].head().to_string())

if __name__ == "__main__":
    main()