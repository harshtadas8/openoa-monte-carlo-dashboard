from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pathlib import Path
import json
import pandas as pd

app = FastAPI(title="OpenOA Analysis API")

# ===============================
# CORS CONFIGURATION
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://openoa-monte-carlo-dashboard.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "OpenOA" / "examples" / "data" / "la_haute_borne"
RESULT_FILE = BASE_DIR / "precomputed_result.json"


@app.get("/")
def root():
    return {"message": "OpenOA Backend Running"}


# ===============================
# BASIC DATA ANALYSIS
# ===============================
@app.get("/analysis")
def run_basic_analysis():
    scada_df = pd.read_csv(DATA_DIR / "la-haute-borne-data-2014-2015.csv")

    scada_df["Date_time"] = pd.to_datetime(
        scada_df["Date_time"],
        utc=True
    )

    return {
        "total_records": len(scada_df),
        "number_of_turbines": scada_df["Wind_turbine_name"].nunique(),
        "average_wind_speed": round(float(scada_df["Ws_avg"].mean()), 2),
        "average_power": round(float(scada_df["P_avg"].mean()), 2),
    }


# ===============================
# MONTE CARLO AEP ANALYSIS (PRECOMPUTED)
# ===============================
@app.get("/analysis/aep")
def get_aep_analysis():
    with open(RESULT_FILE) as f:
        results = json.load(f)

    mean = results["mean_aep_GWh"]
    p50 = results["p50_GWh"]
    p90 = results["p90_GWh"]

    spread = p50 - p90

    if spread < 0.5:
        risk_level = "Low Risk"
        description = "Stable production profile with low inter-annual variability."
        color = "green"
    elif spread < 1.5:
        risk_level = "Moderate Risk"
        description = "Moderate production variability. Some financial uncertainty."
        color = "orange"
    else:
        risk_level = "High Risk"
        description = "Significant production uncertainty. Higher financial risk exposure."
        color = "red"

    results["risk"] = {
        "level": risk_level,
        "spread": round(spread, 2),
        "description": description,
        "color": color,
    }

    return results