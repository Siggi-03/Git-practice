import json
import yaml
import pandas as pd


with open("config.yml") as f:
    config = yaml.safe_load(f)

max_days = config["max_days_since_calibration"]
output_file = config["output_file"]
print(f"Maks dager siden kalibrering: {max_days}")
print(f"Output-fil: {output_file}")


sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")


sensors.columns = sensors.columns.str.strip().str.lower()
calibrations.columns = calibrations.columns.str.strip().str.lower()

print("Kolonner i sensors.xlsx:", list(sensors.columns))
print("Kolonner i calibrations.csv:", list(calibrations.columns))

merged = pd.merge(sensors, calibrations, on="sensor_id")
print(f"Antall sensorer etter sammenslåing: {len(merged)}")


overdue = merged[merged["days_since_calibration"] > max_days]
print(f"Antall sensorer som er over fristen: {len(overdue)}")


wanted = ["sensor_id", "lab_room", "owner", "days_since_calibration"]
columns = [c for c in wanted if c in overdue.columns]
overdue = overdue[columns]

records = overdue.to_dict(orient="records")
with open(output_file, "w") as f:
    json.dump(records, f, indent=2, default=str)

print(f"Skrev {len(records)} sensorer til {output_file}")
