from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from pathlib import Path
import pandas as pd

# Import OpenOA AEP service
from backend.openoa_engine import run_monte_carlo_aep

app = FastAPI(title="OpenOA Analysis API")

# ===============================
# CORS CONFIGURATION
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # local dev
        "https://openoa-monte-carlo-dashboard.onrender.com",  # backend self
        "https://your-frontend-domain.vercel.app",  # replace after frontend deploy
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "OpenOA" / "examples" / "data" / "la_haute_borne"


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

    total_rows = len(scada_df)
    start_time = scada_df["Date_time"].min()
    end_time = scada_df["Date_time"].max()

    avg_wind_speed = scada_df["Ws_avg"].mean()
    avg_power = scada_df["P_avg"].mean()
    total_energy = scada_df["P_avg"].sum()
    num_turbines = scada_df["Wind_turbine_name"].nunique()

    return {
        "total_records": total_rows,
        "time_range": {
            "start": str(start_time),
            "end": str(end_time),
        },
        "number_of_turbines": num_turbines,
        "average_wind_speed": round(float(avg_wind_speed), 2),
        "average_power": round(float(avg_power), 2),
        "total_energy": round(float(total_energy), 2),
    }


# ===============================
# MONTE CARLO AEP ANALYSIS
# ===============================
@app.get("/analysis/aep")
def get_aep_analysis(
    num_sim: int = Query(100, ge=10, le=5000)
):
    """
    Runs full OpenOA Monte Carlo AEP analysis.
    Accepts num_sim as query parameter.
    Returns distribution + summary statistics + risk interpretation.
    """

    results = run_monte_carlo_aep(num_sim=num_sim)

    mean = results["mean_aep_GWh"]
    p50 = results["p50_GWh"]
    p90 = results["p90_GWh"]

    spread = p50 - p90

    # Risk classification logic
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
        "color": color
    }

    results["num_simulations"] = num_sim

    return results