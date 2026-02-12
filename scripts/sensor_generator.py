import time
import json
import random
import datetime
import requests  # <--- New import to send data

# Configuration
MACHINE_ID = "press_001"
API_URL = "http://127.0.0.1:8000/ingest"  # <--- Where we send the data
NORMAL_TEMP_MEAN = 50
NORMAL_TEMP_STD = 2
ANOMALY_CHANCE = 0.05

def generate_sensor_data():
    """Generates a single data point representing machine health."""
    is_anomaly = random.random() < ANOMALY_CHANCE
    timestamp = datetime.datetime.now().isoformat()
    
    if is_anomaly:
        temperature = random.uniform(80, 120) 
        pressure = random.uniform(200, 300)    
        vibration = random.uniform(50, 100)    
        status = "CRITICAL"
    else:
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
    print(f"🚀 Streaming sensor data to {API_URL}...")
    
    try:
        while True:
            data = generate_sensor_data()
            
            try:
                # Send the data to the API using a POST request
                response = requests.post(API_URL, json=data)
                
                # Check if the server accepted it (Status Code 200)
                if response.status_code == 200:
                    print(f"✅ Sent: {data['temperature']}°C | Status: {data['status']}")
                else:
                    print(f"⚠️ Failed: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                print("❌ Connection Error: Is the server running?")
                
            time.sleep(1)  # Send data every second
            
    except KeyboardInterrupt:
        print("\n🛑 Simulation stopped.")