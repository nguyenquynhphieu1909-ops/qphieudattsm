import pandas as pd
from sklearn.metrics import mean_absolute_error
from ml.inference.predict_eta import predict_remaining_eta
import warnings
warnings.filterwarnings('ignore')

def evaluate_realtime_eta(data_path="gps_simulated.csv"):
    df = pd.read_csv(data_path)
    
    if 'delivery_trip_id' in df.columns:
        df = df.rename(columns={'delivery_trip_id': 'route_id'})
    
    df['timestamp_dt'] = pd.to_datetime(df['timestamp'])
    
    # 1. Tính thời gian kết thúc của mỗi chuyến đi
    trip_stats = df.groupby('route_id').agg(
        arrival_time=('timestamp_dt', 'max')
    ).reset_index()
    df = df.merge(trip_stats, on='route_id')
    
    # 2. Tính Thời gian thực tế còn lại (phút)
    df['actual_remaining_time_min'] = (df['arrival_time'] - df['timestamp_dt']).dt.total_seconds() / 60.0
    
    # 3. Ước lượng Quãng đường còn lại (Giả định xe chạy ~25km/h tức là 0.41 km/phút)
    df['remaining_distance_km'] = df['actual_remaining_time_min'] * 0.41
    
    # 4. Lọc các điểm chưa tới đích (còn hơn 1 phút)
    df_eval = df[df['actual_remaining_time_min'] > 1.0].copy()
    print(f"[INFO] Đã chuẩn bị được {len(df_eval)} điểm GPS hợp lệ để đánh giá.")
    
    if len(df_eval) == 0:
        print("[LỖI] Không có dữ liệu hợp lệ!")
        return

    predictions = []
    # Lấy mẫu 500 điểm chạy cho nhanh
    df_eval_sample = df_eval.sample(n=min(500, len(df_eval)), random_state=42)
    
    for index, row in df_eval_sample.iterrows():
        result = predict_remaining_eta(
            route_id=row['route_id'],
            remaining_distance_km=row['remaining_distance_km'],
            current_time_str=row['timestamp']
        )
        predictions.append(result['remaining_eta_minutes'])

    df_eval_sample['predicted_remaining_eta'] = predictions
    mae = mean_absolute_error(df_eval_sample['actual_remaining_time_min'], df_eval_sample['predicted_remaining_eta'])
    
    print("\n" + "="*60)
    print(" BÁO CÁO ĐÁNH GIÁ MÔ HÌNH TUẦN 03 TRÊN DỮ LIỆU THỜI GIAN THỰC")
    print("="*60)
    print(f" MAE (Sai số trung bình): {mae:.2f} phút")
    print("="*60)

    if mae > 10:
        print("⚠️ KẾT LUẬN: Mô hình Tuần 03 KHÔNG phù hợp để dự báo chặng còn lại (MAE > 10 phút).")
        print("👉 Hành động: Chuyển sang sử dụng Baseline OSRM (Hoàn thành Task 4.3.3).")
    else:
        print("✅ KẾT LUẬN: Mô hình Tuần 03 nội suy rất tốt.")

if __name__ == "__main__":
    evaluate_realtime_eta()