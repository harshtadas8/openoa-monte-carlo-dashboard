from backend.openoa_engine import initialize_cached_result
import json

print("Running Monte Carlo locally...")

result = initialize_cached_result(num_sim=50)

with open("precomputed_result.json", "w") as f:
    json.dump(result, f)

print("Precomputed result saved as precomputed_result.json")