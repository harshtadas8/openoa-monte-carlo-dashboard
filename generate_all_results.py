import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).resolve().parent))

from backend.openoa_engine import run_monte_carlo_aep

simulation_sizes = [100, 300, 500, 1000]

for n in simulation_sizes:
    print(f"Running Monte Carlo with {n} simulations...")
    result = run_monte_carlo_aep(num_sim=n)

    with open(f"backend/precomputed_{n}.json", "w") as f:
        json.dump(result, f)

    print(f"Saved backend/precomputed_{n}.json")

print("All precomputed results generated.")