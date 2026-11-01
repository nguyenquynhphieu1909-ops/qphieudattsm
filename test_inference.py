import json
from ml.inference.predict_eta import predict_eta

print("--- KIỂM THỬ KỊCH BẢN 1: TUYẾN ĐƯỜNG CHUẨN (ML HOẠT ĐỘNG) ---")
res1 = predict_eta(
    route_id="ROUTE_01",
    distance_km=8.5,
    departure_time="2026-11-02T17:30:00"  # Thứ 2, giờ cao điểm
)
print(json.dumps(res1, indent=4, ensure_ascii=False))

print("\n--- KIỂM THỬ KỊCH BẢN 2: TUYẾN ĐƯỜNG ĐÊM ---")
res2 = predict_eta(
    route_id="ROUTE_01",
    distance_km=8.5,
    departure_time="2026-11-02T23:00:00"  # Đêm khuya vắng
)
print(json.dumps(res2, indent=4, ensure_ascii=False))