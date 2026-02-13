import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 1. DATABASE CONFIGURATION
# This connects to the Docker container we just started.
# user: user, password: password, db: ecostream, host: localhost, port: 5432
DATABASE_URL = "postgresql://user:password@localhost:5432/ecostream"

# Set up the database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. DEFINE THE TABLE (Schema)
class SensorReading(Base):
    __tablename__ = "sensor_readings"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    status = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# 3. INITIALIZE FASTAPI
app = FastAPI()

# Pydantic model for input validation (The "Bouncer")
class SensorData(BaseModel):
    machine_id: str
    timestamp: str
    temperature: float
    pressure: float
    vibration: float
    status: str

# 4. THE INGEST ENDPOINT
@app.post("/ingest")
async def ingest_data(data: SensorData):
    db = SessionLocal()
    try:
        # Create a new database record
        new_reading = SensorReading(
            machine_id=data.machine_id,
            timestamp=datetime.fromisoformat(data.timestamp),
            temperature=data.temperature,
            pressure=data.pressure,
            vibration=data.vibration,
            status=data.status
        )
        
        # Save to the database
        db.add(new_reading)
        db.commit()
        db.refresh(new_reading)
        
        print(f"✅ SAVED to DB: {data.machine_id} | {data.temperature}°C")
        return {"message": "Data saved successfully", "id": new_reading.id}
        
    except Exception as e:
        print(f"❌ Error saving to DB: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "EcoStream API is connected to TimescaleDB!"}