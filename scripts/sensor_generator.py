import time
import json
import random
import datetime

# Configuration
MACHINE_ID = "press_001"
NORMAL_TEMP_MEAN = 50
NORMAL_TEMP_STD = 2
ANOMALY_CHANCE = 0.05  # 5% chance of a spike

def generate_sensor_data():
    """Generates a single data point representing machine health."""
    # Decide if this reading is an anomaly
    is_anomaly = random.random() < ANOMALY_CHANCE

    timestamp = datetime.datetime.now().isoformat()

    if is_anomaly:
        # Simulate a dangerous spike (High heat, Pressure, Vibration)
        temperature = random.uniform(80, 120) 
        pressure = random.uniform(200, 300)    
        vibration = random.uniform(50, 100)    
        status = "CRITICAL"
    else:
        # Normal operating conditions
        temperature = random.gauss(NORMAL_TEMP_MEAN, NORMAL_TEMP_STD)
        pressure = random.gauss(100, 10)
        vibration = random.gauss(10, 2)
        status = "NORMAL"

    return {
        "machine_id": MACHINE_ID,
        "timestamp": timestamp,
        "temperature": round(temperature, 2),
        "pressure": round(pressure, 2),
        "vibration": round(vibration, 2),
        "status": status
    }

if __name__ == "__main__":
    print(f"Starting sensor simulation for {MACHINE_ID}...")
    try:
        while True:
            data = generate_sensor_data()
            print(json.dumps(data))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")