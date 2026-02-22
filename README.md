# EcoStream: Industrial Anomaly Detection System
A real-time full-stack IoT dashboard that detects machine failures using ML.

# EcoStream: Industrial Anomaly Detection System
A real-time full-stack IoT dashboard that detects machine failures using ML.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-TimescaleDB-336791.svg)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E.svg)

*(Drag and drop your dashboard screenshot here!)*

## 📌 Overview
EcoStream is an end-to-end telemetry and analytics pipeline designed to monitor critical infrastructure and industrial machinery. Instead of relying on static, historical datasets, this project ingests live, streaming sensor data (temperature, pressure, vibration) and applies **Machine Learning in real-time** to detect anomalies before catastrophic failures occur.

This architecture bridges the gap between data science and actionable operational intelligence—a crucial requirement for modern civic, environmental, and industrial monitoring systems.

## 🏗️ The Architecture
The system is built on a microservices architecture, ensuring high performance and separation of concerns:

1. **Data Ingestion Faucet:** A Python-based IoT simulator generates realistic, multi-variate time-series telemetry.
2. **The AI Brain (Scikit-Learn):** An **Isolation Forest** unsupervised machine learning model evaluates incoming data streams to flag statistical outliers in milliseconds.
3. **The Nervous System (FastAPI):** A high-performance REST API acts as the bridge, receiving telemetry, querying the ML model, and routing the results.
4. **Persistent Memory (Docker + TimescaleDB):** Data is permanently stored in a containerized PostgreSQL database optimized for time-series analytics.
5. **The Face (React + Recharts):** A dark-mode, responsive web dashboard provides real-time data visualization and instant visual alarms for critical system states.

## ✨ Key Features
* **Real-Time ML Inference:** Deploys a serialized `.pkl` model directly into the API flow.
* **Time-Series Optimization:** Utilizes TimescaleDB to handle high-frequency sensor writes.
* **Live Polling Dashboard:** React frontend automatically updates every 2 seconds without page refreshes.
* **"Demo Mode" Automation:** A custom bash script (`start_demo.sh`) spins up the entire full-stack environment (Database, API, Frontend, and Data Stream) with a single command.

## 🚀 Quick Start (Run it Locally)

**Prerequisites:** Ensure you have `Python 3`, `Node.js`, and `Docker Desktop` installed and running.

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/ecostream-anomaly-detection.git](https://github.com/yourusername/ecostream-anomaly-detection.git)
cd ecostream-anomaly-detection

# 2. Setup the Python Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Setup the React Frontend
cd dashboard
npm install
cd ..

# 4. Launch the Entire Pipeline
./start_demo.sh
