import json
from ml.inference.predict_eta import predict_eta, predict_remaining_eta

print("--- KIỂM THỬ KỊCH BẢN 1: DỰ BÁO ETA BAN ĐẦU (TUẦN 03) ---")
res1 = predict_eta(
    route_id="ROUTE_01",
    distance_km=8.5,
    departure_time="2026-11-02T17:30:00"
)
print(json.dumps(res1, indent=4, ensure_ascii=False))

print("\n--- KIỂM THỬ KỊCH BẢN 2: DỰ BÁO REAL-TIME ETA CHẶNG CÒN LẠI (TUẦN 04) ---")
res2 = predict_remaining_eta(
    route_id="ROUTE_01",
    remaining_distance_km=3.5,
    current_time_str="2026-11-02T17:45:00",
    osrm_remaining_eta=12.5
)
print(json.dumps(res2, indent=4, ensure_ascii=False))