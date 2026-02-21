# 🌬️ OpenOA Monte Carlo AEP Risk Dashboard

A full-stack production deployment of a Monte Carlo Annual Energy Production (AEP) risk analysis system built using **OpenOA**, **FastAPI**, **React (Vite)**, and deployed using **Render (Docker)** and **Vercel**.

This project simulates wind farm production uncertainty and provides a financial risk interpretation based on P50–P90 spread.

---

## 🚀 Live Demo

Frontend (Vercel):  
👉 https://openoa-monte-carlo-dashboard.vercel.app  

Backend API (Render):  
👉 https://openoa-monte-carlo-dashboard.onrender.com  

Swagger Docs:  
👉 https://openoa-monte-carlo-dashboard.onrender.com/docs  

---

## 🧠 Project Overview

Wind energy production is uncertain due to inter-annual variability and operational factors.  
This project performs **Monte Carlo AEP simulations** using the OpenOA framework and visualizes the distribution along with financial risk classification.

The system:

- Runs Monte Carlo simulations
- Computes Mean AEP, P50, P90
- Calculates risk spread (P50 - P90)
- Classifies financial risk level
- Visualizes distribution as histogram
- Fully deployed in production

---

## 🏗️ Architecture

```
Frontend (React + Vite + Recharts)
        ↓
Backend API (FastAPI + Docker on Render)
        ↓
OpenOA Monte Carlo Engine
        ↓
Wind Farm SCADA Data
```

---

## ⚙️ Tech Stack

### Frontend
- React (Vite)
- Recharts
- Deployed on Vercel

### Backend
- FastAPI
- OpenOA
- Pandas
- Docker
- Deployed on Render

### Data
- La Haute Borne Wind Farm SCADA Dataset
- Provided in OpenOA examples

---

## 📊 API Endpoints

### Root

```
GET /
```

Response:

```json
{
  "message": "OpenOA Backend Running"
}
```

---

### Basic Data Summary

```
GET /analysis
```

Returns:
- Total records
- Time range
- Number of turbines
- Average wind speed
- Average power
- Total energy

---

### Monte Carlo AEP Analysis

```
GET /analysis/aep?num_sim=100
```

Query Parameters:

| Parameter | Type | Description |
|------------|------|------------|
| num_sim | int | Number of Monte Carlo simulations (10–5000) |

Example Response:

```json
{
  "mean_aep_GWh": 15.2,
  "p50_GWh": 15.1,
  "p90_GWh": 14.3,
  "std_dev": 0.8,
  "distribution": [...],
  "risk": {
    "level": "Moderate Risk",
    "spread": 0.8,
    "description": "Moderate production variability. Some financial uncertainty.",
    "color": "orange"
  }
}
```

---

## 📈 Risk Classification Logic

The project classifies financial risk based on the P50–P90 spread:

| Spread | Risk Level |
|--------|------------|
| < 0.5 GWh | Low Risk |
| 0.5 – 1.5 GWh | Moderate Risk |
| > 1.5 GWh | High Risk |

This reflects production variability and revenue uncertainty.

---

## 🐳 Backend Deployment (Docker)

Dockerfile uses:

```
python:3.11.9-slim
```

Steps:
1. Install dependencies
2. Copy backend files
3. Run FastAPI using Uvicorn

---

## 🖥️ Local Development

### Backend

```
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### Frontend

```
cd frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

## 🌍 Production Deployment

### Backend (Render)
- Docker-based deployment
- Auto redeploy on Git push
- Free tier (sleeps after inactivity)

### Frontend (Vercel)
- Root directory: `frontend`
- Framework preset: Vite
- Environment variable:
  ```
  VITE_API_URL=https://openoa-monte-carlo-dashboard.onrender.com
  ```

---

## 🔐 CORS Configuration

Backend allows:

```
http://localhost:5173
https://openoa-monte-carlo-dashboard.vercel.app
```

---

## 📊 Features

- Adjustable Monte Carlo simulation size
- Dynamic histogram binning
- Risk color classification
- Financial spread interpretation
- Production-ready deployment
- Dockerized backend
- Fully separated frontend & backend

---

## 🧪 Example Use Case

An energy finance analyst can:

1. Run 1000 Monte Carlo simulations
2. Observe AEP distribution
3. Evaluate P50–P90 spread
4. Assess financial exposure
5. Make investment decisions accordingly

---

## 📌 Key Engineering Highlights

- Full-stack ML deployment
- Dockerized FastAPI service
- Cross-origin secure configuration
- Production environment variable management
- Statistical simulation pipeline
- Clean frontend visualization
- Financial interpretation layer

---

## 🧑‍💻 Author

Harsh Tadas  
Wind Energy Analytics & Full-Stack Engineering Project

---

## 📄 License

This project is for educational and demonstration purposes.
