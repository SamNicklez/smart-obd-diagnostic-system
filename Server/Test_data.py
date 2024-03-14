from datetime import datetime, timedelta
import random
import json

def random_binary_string(length=8):
    return ''.join(random.choice(['0', '1']) for _ in range(length))

def random_timestamp():
    start = datetime.now() - timedelta(days=4)
    end = datetime.now()
    random_date = start + (end - start) * random.random()
    return random_date.strftime('%Y-%m-%d %H:%M:%S')

def random_varchar(length=5):
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))

def generate_car_info_json(n=4):
    data = []
    for _ in range(n):
        car_info = {
            "stage_id": random.randint(1, 255),
            "timestamp": random_timestamp(),
            "airflow_rate": round(random.uniform(0.1, 100.0), 4),
            "speed": round(random.uniform(0.1, 200.0), 4),
            "relative_throttle_pos": round(random.uniform(0.1, 100.0), 4),
            "distance_w_mil": round(random.uniform(0.1, 1000.0), 4),
            "runtime": round(random.uniform(0.1, 500.0), 4),
            "commanded_egr": round(random.uniform(0.1, 100.0), 4),
            "time_since_dtc_cleared": round(random.uniform(0.1, 1000.0), 4),
            "runtime_mil": round(random.uniform(0.1, 500.0), 4),
            "intake_pressure": round(random.uniform(0.1, 100.0), 4),
            "coolant_temp": round(random.uniform(-20.0, 100.0), 4),
            "oil_temp": round(random.uniform(-20.0, 100.0), 4),
            "barometric_pressure": round(random.uniform(0.1, 100.0), 4),
            "rpm": round(random.uniform(0.1, 8000.0), 4),
            "pids_b": random_binary_string(16),
            "intake_temp": round(random.uniform(-20.0, 100.0), 4),
            "voltage": round(random.uniform(0.1, 14.0), 4),
            "absolute_load": round(random.uniform(0.1, 100.0), 4),
            "engine_load": round(random.uniform(0.1, 100.0), 4),
            "status": random_varchar(),
            "dtc": random_varchar(3),
            "current_dtc": random_varchar(3),
            "lattitude": round(random.uniform(-90.0, 90.0), 8),
            "longitude": round(random.uniform(-180.0, 180.0), 8),
        }
        data.append(car_info)
    return json.dumps(data, indent=4)