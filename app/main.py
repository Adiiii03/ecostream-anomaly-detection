import time
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware # <--- NEW
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# 1. LOAD MODEL
model = joblib.load("isolation_forest.pkl")

# 2. DATABASE SETUP
DATABASE_URL = "postgresql://user:password@localhost:5432/ecostream"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SensorReading(Base):
    __tablename__ = "sensor_readings"
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    status = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 3. ENABLE CORS (Allow React to talk to FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SensorData(BaseModel):
    machine_id: str
    timestamp: str
    temperature: float
    pressure: float
    vibration: float
    status: str

# 4. INGEST ENDPOINT (POST)
@app.post("/ingest")
async def ingest_data(data: SensorData, db: Session = Depends(get_db)):
    try:
        features = pd.DataFrame(
            [[data.temperature, data.pressure, data.vibration]], 
            columns=["temperature", "pressure", "vibration"]
        )
        prediction = model.predict(features)[0]
        ai_status = "CRITICAL" if prediction == -1 else "NORMAL"

        new_reading = SensorReading(
            machine_id=data.machine_id,
            timestamp=datetime.fromisoformat(data.timestamp),
            temperature=data.temperature,
            pressure=data.pressure,
            vibration=data.vibration,
            status=ai_status
        )
        db.add(new_reading)
        db.commit()
        db.refresh(new_reading)
        return {"status": ai_status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. NEW: READ ENDPOINT (GET)
# This lets the frontend fetch the last 20 readings to graph them.
@app.get("/readings")
def get_readings(limit: int = 20, db: Session = Depends(get_db)):
    readings = db.query(SensorReading).order_by(desc(SensorReading.timestamp)).limit(limit).all()
    return readings[::-1] # Reverse so the graph goes Left -> Right