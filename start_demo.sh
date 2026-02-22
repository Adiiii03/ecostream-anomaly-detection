#!/bin/bash

echo "🚀 Starting EcoStream IIoT Pipeline..."

# 1. Start the Database
echo "📦 Starting TimescaleDB (Docker)..."
docker-compose up -d
sleep 3 # Give the DB a moment to wake up

# 2. Start the Backend API
echo "🧠 Starting FastAPI Server..."
source venv/bin/activate
uvicorn app.main:app --port 8000 &
BACKEND_PID=$!

# 3. Start the Frontend Dashboard
echo "🖥️ Starting React Dashboard..."
cd dashboard
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3 # Give servers a moment to bind to ports

# 4. Start the Data Faucet
echo "🏭 Streaming live factory data... (Press Ctrl+C to stop everything)"
python3 scripts/sensor_generator.py

# --- CLEANUP ---
# When you press Ctrl+C, this block catches it and gracefully shuts down the background servers.
trap "echo '🛑 Shutting down EcoStream...'; kill $BACKEND_PID; kill $FRONTEND_PID; docker-compose stop; exit" INT TERM