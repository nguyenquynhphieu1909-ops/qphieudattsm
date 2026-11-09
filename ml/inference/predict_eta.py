import os
import joblib
import pandas as pd
from datetime import datetime

class ETAPredictor:
    def __init__(self):
        # Lấy đường dẫn tuyệt đối đến file model
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(base_dir, 'rf_model_pipeline.joblib')
        
        try:
            self.model_pipeline = joblib.load(model_path)
            print("[INFO] Đã nạp thành công mô hình ML Random Forest.")
        except Exception as e:
            self.model_pipeline = None
            print(f"[CẢNH BÁO] Không tìm thấy model tại {model_path}. Fallback sẽ được kích hoạt.")

    def predict_eta(self, route_id: str, distance_km: float, departure_time: str) -> dict:
        """Hàm dự báo ban đầu (Tuần 03)"""
        if self.model_pipeline is None:
            return {"status": "warning", "eta_minutes": round((distance_km / 25.0) * 60, 2), "source": "FALLBACK_AVERAGE_SPEED"}
        
        try:
            dt = pd.to_datetime(departure_time)
            input_data = pd.DataFrame([{
                'route_id': route_id,
                'distance_km': distance_km,
                'hour_of_day': dt.hour,
                'day_of_week': dt.dayofweek,
                'is_weekend': int(dt.dayofweek >= 5),
                'is_rush_hour': int(dt.hour in [7, 8, 17, 18])
            }])
            pred_eta = self.model_pipeline.predict(input_data)[0]
            return {"status": "success", "eta_minutes": round(pred_eta, 2), "source": "ML_MODEL_WEEK3"}
        except Exception as e:
            return {"status": "warning", "eta_minutes": round((distance_km / 25.0) * 60, 2), "source": "FALLBACK_AVERAGE_SPEED"}

    def predict_remaining_eta(self, route_id: str, remaining_distance_km: float, current_time_str: str, osrm_remaining_eta: float = None) -> dict:
        """Hàm dự báo Real-time cho Backend gọi khi xe đang di chuyển (Tuần 04)"""
        # 1. BASELINE TỪ OSRM (Dành cho Task 4.3.3)
        if self.model_pipeline is None:
            if osrm_remaining_eta is not None:
                return {"status": "success", "remaining_eta_minutes": round(osrm_remaining_eta, 2), "source": "BASELINE_OSRM"}
        
        # 2. DỰ BÁO BẰNG MODEL TUẦN 03 (Dành cho Task 4.3.2)
        try:
            current_time = pd.to_datetime(current_time_str)
            input_data = pd.DataFrame([{
                'route_id': route_id,
                'distance_km': remaining_distance_km,
                'hour_of_day': current_time.hour,
                'day_of_week': current_time.dayofweek,
                'is_weekend': int(current_time.dayofweek >= 5),
                'is_rush_hour': int(current_time.hour in [7, 8, 17, 18])
            }])
            pred_eta = self.model_pipeline.predict(input_data)[0]
            return {"status": "success", "remaining_eta_minutes": round(pred_eta, 2), "source": "ML_MODEL_WEEK3"}
        except Exception as e:
            # 3. FALLBACK AN TOÀN (Dành cho Task 4.3.5)
            return {"status": "warning", "remaining_eta_minutes": round((remaining_distance_km / 25.0) * 60, 2), "source": "FALLBACK_AVERAGE_SPEED"}

# Khởi tạo đối tượng chung
predictor = ETAPredictor()

def predict_eta(route_id: str, distance_km: float, departure_time: str) -> dict:
    return predictor.predict_eta(route_id, distance_km, departure_time)

def predict_remaining_eta(route_id: str, remaining_distance_km: float, current_time_str: str, osrm_remaining_eta: float = None) -> dict:
    return predictor.predict_remaining_eta(route_id, remaining_distance_km, current_time_str, osrm_remaining_eta)