from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Define the Data "Shape" (Schema)
# This acts as a bouncer. If data doesn't match this format, the API rejects it.
class SensorData(BaseModel):
    machine_id: str
    timestamp: str
    temperature: float
    pressure: float
    vibration: float
    status: str


# 2. The "Ingest" Endpoint
# This is the door our sensor script will knock on to deliver data.
@app.post("/ingest")
async def ingest_data(data: SensorData):
    # for now print to console to prove we got it
    # later, we will save this to a database
    print(f"🔥 RECEIVED: {data.machine_id} | Status: {data.status} | Temp: {data.temperature}")
    return {"message": "Data received successfully"}


# 3. Health Check (Standard for cloud apps)
@app.get("/")
def root():
    return {"message:" "EcoStream API is running"}