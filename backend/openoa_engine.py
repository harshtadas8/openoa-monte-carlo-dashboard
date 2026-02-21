from pathlib import Path
import json
import pandas as pd
import numpy as np

from openoa.plant import PlantData
from openoa.analysis.aep import MonteCarloAEP


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "OpenOA" / "examples" / "data" / "la_haute_borne"
META_FILE = BASE_DIR / "OpenOA" / "examples" / "data" / "plant_meta.json"

# 🔥 Global cache
CACHED_RESULT = None


def load_plant():
    with open(META_FILE) as f:
        metadata = json.load(f)

    metadata["meter"]["time"] = "time_utc"
    metadata["curtail"]["time"] = "time_utc"

    scada_df = pd.read_csv(DATA_DIR / "la-haute-borne-data-2014-2015.csv")
    scada_df["Date_time"] = pd.to_datetime(
        scada_df["Date_time"], utc=True
    ).dt.tz_convert(None)

    plant_df = pd.read_csv(DATA_DIR / "plant_data.csv")
    plant_df["time_utc"] = pd.to_datetime(
        plant_df["time_utc"], utc=True
    ).dt.tz_convert(None)

    meter_df = plant_df[["time_utc", "net_energy_kwh"]].copy()
    curtail_df = plant_df[["time_utc", "availability_kwh", "curtailment_kwh"]].copy()

    plant = PlantData(
        metadata=metadata,
        scada=scada_df,
        meter=meter_df,
        curtail=curtail_df,
        asset=DATA_DIR / "la-haute-borne_asset_table.csv",
        reanalysis={
            "era5": DATA_DIR / "era5_wind_la_haute_borne.csv",
            "merra2": DATA_DIR / "merra2_la_haute_borne.csv"
        }
    )

    return plant


def initialize_cached_result(num_sim=10):
    """
    Run Monte Carlo ONCE at startup and cache result.
    """
    global CACHED_RESULT

    if CACHED_RESULT is not None:
        return CACHED_RESULT

    plant = load_plant()

    aep = MonteCarloAEP(plant)
    aep.run(num_sim=num_sim)

    df = aep.results

    aep_values = df["aep_GWh"].values.tolist()

    mean_aep = float(np.mean(aep_values))
    p50 = float(np.percentile(aep_values, 50))
    p90 = float(np.percentile(aep_values, 10))
    std_dev = float(np.std(aep_values))

    CACHED_RESULT = {
        "distribution": aep_values,
        "mean_aep_GWh": mean_aep,
        "p50_GWh": p50,
        "p90_GWh": p90,
        "std_dev": std_dev,
        "num_simulations": num_sim
    }

    return CACHED_RESULT


def get_cached_result():
    """
    Return precomputed Monte Carlo result.
    """
    return CACHED_RESULT

def run_monte_carlo_aep(num_sim=100):
    plant = load_plant()

    aep = MonteCarloAEP(plant)
    aep.run(num_sim=num_sim)

    df = aep.results

    aep_values = df["aep_GWh"].values.tolist()

    mean_aep = float(np.mean(aep_values))
    p50 = float(np.percentile(aep_values, 50))
    p90 = float(np.percentile(aep_values, 10))
    std_dev = float(np.std(aep_values))

    return {
        "distribution": aep_values,
        "mean_aep_GWh": mean_aep,
        "p50_GWh": p50,
        "p90_GWh": p90,
        "std_dev": std_dev,
    }