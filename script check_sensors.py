import json
import yaml
import pandas as pd

# 1. Les innstillinger
with open("config.yml") as f:
    config = yaml.safe_load(f)

max_days = config["max_days_since_calibration"]
output_file = config["output_file"]

# 2. Les data
sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")

# 3. Slå sammen på sensor_id
merged = pd.merge(sensors, calibrations, on="sensor_id")

# 4. Filtrer og eksporter
overdue = merged[merged["days_since_calibration"] > max_days]

with open(output_file, "w") as f:
    json.dump(overdue.to_dict(orient="records"), f, indent=2)