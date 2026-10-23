import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

def load_and_preprocess_data(file_path="trips_ml_v1.csv"):
    if not os.path.exists(file_path):
        # Fallback về file sample_trips.csv nếu không thấy trips_ml_v1.csv
        file_path = "sample_trips.csv"
        if not os.path.exists(file_path):
            print(f"[LỖI] Không tìm thấy file dữ liệu CSV nào trong thư mục.")
            return None

    df = pd.read_csv(file_path)
    print(f"-> Đã đọc dữ liệu từ file: {file_path}")

    # 1. Xử lý chuẩn hóa cột nhãn (Target) - Tránh bị trùng lặp cột
    if 'actual_travel_time' not in df.columns:
        target_candidates = [
            'actual_duration_min', 'travel_time', 
            'duration', 'travel_time_min', 'actual_time', 'duration_min'
        ]
        for col in df.columns:
            if col.strip().lower() in [c.lower() for c in target_candidates]:
                df.rename(columns={col: 'actual_travel_time'}, inplace=True)
                print(f"-> Đã đổi tên cột '{col}' thành 'actual_travel_time'")
                break

    if 'actual_travel_time' not in df.columns:
        print(f"[LỖI] Không tìm thấy cột thời gian di chuyển trong file CSV. Các cột: {list(df.columns)}")
        return None

    # Loại bỏ các cột trùng tên nếu có trong file
    df = df.loc[:, ~df.columns.duplicated()].copy()

    # 2. Xử lý cột thời gian xuất phát (departure_time)
    if 'departure_time' in df.columns:
        if 'date' in df.columns and df['departure_time'].astype(str).str.len().mean() < 10:
            df['departure_time'] = df['date'].astype(str) + ' ' + df['departure_time'].astype(str)
        df['departure_time'] = pd.to_datetime(df['departure_time'], format='mixed', errors='coerce')
    else:
        print("[LỖI] Không tìm thấy cột 'departure_time' trong file CSV.")
        return None

    # 3. Trích xuất đặc trưng thời gian
    df['hour_of_day'] = df['departure_time'].dt.hour
    df['day_of_week'] = df['departure_time'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_rush_hour'] = df['hour_of_day'].isin([7, 8, 17, 18]).astype(int)

    # Sắp xếp theo trình tự thời gian
    df = df.sort_values(by='departure_time').reset_index(drop=True)
    return df

def main():
    csv_file = "trips_ml_v1.csv"
    df = load_and_preprocess_data(csv_file)
    if df is None:
        return

    print("==================================================")
    print(f"   ĐÃ TẢI DỮ LIỆU: {len(df)} dòng chuyến đi")
    print("==================================================")

    # Chia tập Train/Test theo chuỗi thời gian (80/20)
    split_idx = int(len(df) * 0.8)
    if split_idx < 1:
        split_idx = int(len(df) * 0.7)

    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()

    # 1. Baseline Model
    baseline_lookup = train_df.groupby(['route_id', 'is_rush_hour'])['actual_travel_time'].mean().reset_index()
    baseline_lookup.rename(columns={'actual_travel_time': 'baseline_pred'}, inplace=True)

    test_df = pd.merge(test_df, baseline_lookup, on=['route_id', 'is_rush_hour'], how='left')
    global_mean = train_df['actual_travel_time'].mean()
    test_df['baseline_pred'] = test_df['baseline_pred'].fillna(global_mean)

    mae_baseline = mean_absolute_error(test_df['actual_travel_time'], test_df['baseline_pred'])
    acc_10m_base = (np.abs(test_df['actual_travel_time'] - test_df['baseline_pred']) <= 10).mean() * 100

    # 2. Random Forest Model
    features = ['route_id', 'distance_km', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_rush_hour']
    target = 'actual_travel_time'

    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['route_id'])
        ],
        remainder='passthrough'
    )

    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42))
    ])

    model_pipeline.fit(X_train, y_train)
    y_pred_rf = model_pipeline.predict(X_test)

    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    r2_rf = r2_score(y_test, y_pred_rf)
    acc_10m_rf = (np.abs(y_test - y_pred_rf) <= 10).mean() * 100

    print("\n==================================================")
    print("         BÁO CÁO SO SÁNH KẾT QUẢ (TUẦN 02)        ")
    print("==================================================")
    print(f"{'Chỉ số đánh giá':<28} | {'Baseline':<10} | {'Random Forest':<10}")
    print("-" * 55)
    print(f"{'MAE (Sai số TB - phút)':<28} | {mae_baseline:<10.2f} | {mae_rf:<10.2f}")
    print(f"{'Tỷ lệ sai số <= 10 phút (%)':<28} | {acc_10m_base:<10.1f} | {acc_10m_rf:<10.1f}")
    print(f"{'Độ phù hợp R² Score':<28} | {'N/A':<10} | {r2_rf:<10.3f}")
    print("==================================================")

    # Xuất file pipeline .joblib
    model_filename = "rf_model_pipeline.joblib"
    joblib.dump(model_pipeline, model_filename)
    print(f"\n[THÀNH CÔNG] Đã lưu file Pipeline tại: '{model_filename}'")

if __name__ == "__main__":
    main()