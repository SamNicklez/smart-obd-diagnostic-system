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

def generate_sequential_timestamps(start, n, max_minutes_apart=10):
    timestamps = [start]
    for _ in range(1, n):
        timestamps.append(timestamps[-1] + timedelta(minutes=random.uniform(1, max_minutes_apart)))
    return [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

def generate_sequential_timestamps_with_breaks(start, n, max_minutes_apart=10, break_threshold=30):
    """Generate n sequential timestamps starting from 'start', each a random number of minutes apart,
    with occasional breaks longer than break_threshold indicating a new trip."""
    timestamps = [start]
    for _ in range(1, n):
        gap = random.uniform(1, max_minutes_apart)
        # Introduce a break indicating the end of a trip and the start of a new one
        if random.random() < 0.1:  # Adjust this value to control frequency of new trips
            gap += break_threshold + random.uniform(1, 60)  # Add a random gap between 30 to 90 minutes
        timestamps.append(timestamps[-1] + timedelta(minutes=gap))
    return [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in timestamps]

def generate_car_info_json(n=10):
    data = []
    start_time = datetime.now() - timedelta(days=1)
    timestamps = generate_sequential_timestamps_with_breaks(start_time, n)
    
    lat, lon = 40.0, -74.0
    
    for timestamp in timestamps:
        speed = round(random.uniform(0, 100), 4)
        lat += random.uniform(-0.01, 0.01)
        lon += random.uniform(-0.01, 0.01)
        
        car_info = {
            "timestamp": timestamp,
            "airflow_rate": round(random.uniform(0.1, 100.0), 4),
            "speed": speed,
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
            "lattitude": round(lat, 8),
            "longitude": round(lon, 8),
        }
        data.append(car_info)
    
    return json.dumps(data, indent=4)