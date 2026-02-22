# 🏭 EcoStream: Industrial IoT Anomaly Detection Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![React](https://img.shields.io/badge/React-18.0+-61dafb.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ed.svg)
![TimescaleDB](https://img.shields.io/badge/TimescaleDB-PostgreSQL-f3bc16.svg)

[INSERT YOUR SCREENSHOT HERE]

## 📌 Overview
EcoStream is an end-to-end Industrial Internet of Things (IIoT) pipeline designed to ingest, process, and visualize factory sensor data in real-time. It utilizes a Machine Learning model (**Isolation Forest**) to instantly detect mechanical anomalies (like temperature spikes or abnormal vibrations) and alerts operators before catastrophic equipment failure occurs.

This project demonstrates a full-stack data architecture, moving from raw data generation to AI inference, persistent storage, and frontend visualization.

## 🏗️ Architecture & Tech Stack
* **Data Generation:** Python script simulating real-time machine telemetry (Temperature, Pressure, Vibration).
* **AI / Machine Learning:** `Scikit-Learn` (Isolation Forest) trained on synthetic baseline data to detect multidimensional outliers.
* **Backend API:** `FastAPI` serving as the ingestion layer and model inference engine.
* **Database:** `PostgreSQL` with `TimescaleDB` running in `Docker` for high-performance time-series data storage.
* **Frontend Dashboard:** `React` + `Vite` + `Recharts` featuring a responsive, dark-mode UI with real-time polling and visual alarms.

## 🚀 Quick Start (Demo Mode)
Want to run the entire pipeline on your local machine? 

**Prerequisites:** Ensure you have Python 3, Node.js, and Docker Desktop installed.

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/ecostream-anomaly-detection.git](https://github.com/yourusername/ecostream-anomaly-detection.git)
cd ecostream-anomaly-detection

# 2. Install Python Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Install Frontend Dependencies
cd dashboard
npm install
cd ..

# 4. Run the full stack (DB, Backend, Frontend, and Data Stream)
./start_demo.sh