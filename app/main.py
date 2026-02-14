import time
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 1. LOAD THE TRAINED MODEL
# We load the "brain" once when the server starts
model = joblib.load("isolation_forest.pkl")

# 2. DATABASE CONFIGURATION
DATABASE_URL = "postgresql://user:password@localhost:5432/ecostream"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 3. DEFINE THE TABLE
class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    status = Column(String) # We will determine this using ML

Base.metadata.create_all(bind=engine)

app = FastAPI()

class SensorData(BaseModel):
    machine_id: str
    timestamp: str
    temperature: float
    pressure: float
    vibration: float
    status: str  # We receive this, but we might overwrite it!

@app.post("/ingest")
async def ingest_data(data: SensorData):
    db = SessionLocal()
    try:
        # --- THE AI BRAIN KICKS IN HERE ---
        # 1. Format the data exactly how the model expects it
        features = pd.DataFrame(
            [[data.temperature, data.pressure, data.vibration]], 
            columns=["temperature", "pressure", "vibration"]
        )
        
        # 2. Ask the model: Is this an anomaly?
        prediction = model.predict(features)[0] # Returns 1 (Normal) or -1 (Anomaly)
        
        # 3. Set status based on AI, not just what the sensor said
        if prediction == -1:
            ai_status = "CRITICAL" 
            print(f"🚨 ANOMALY DETECTED! Temp: {data.temperature}")
        else:
            ai_status = "NORMAL"

        # 4. Save to Database
        new_reading = SensorReading(
            machine_id=data.machine_id,
            timestamp=datetime.fromisoformat(data.timestamp),
            temperature=data.temperature,
            pressure=data.pressure,
            vibration=data.vibration,
            status=ai_status # <-- Using the AI's judgment
        )
        
        db.add(new_reading)
        db.commit()
        db.refresh(new_reading)
        
        return {"message": "Data processed", "ai_status": ai_status}
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()