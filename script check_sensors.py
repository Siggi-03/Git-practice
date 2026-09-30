import json
import yaml
import pandas as pd

# 1. Les innstillinger fra config.yml
with open("config.yml") as f:
    config = yaml.safe_load(f)

max_days = config["max_days_since_calibration"]
output_file = config["output_file"]
print(f"Maks dager siden kalibrering: {max_days}")
print(f"Output-fil: {output_file}")

# 2. Les data
sensors = pd.read_excel("sensors.xlsx")
calibrations = pd.read_csv("calibrations.csv")

# Rydd kolonnenavn (fjerner mellomrom og gjør dem små bokstaver)
sensors.columns = sensors.columns.str.strip().str.lower()
calibrations.columns = calibrations.columns.str.strip().str.lower()

print("Kolonner i sensors.xlsx:", list(sensors.columns))
print("Kolonner i calibrations.csv:", list(calibrations.columns))

# 3. Slå sammen på sensor_id
merged = pd.merge(sensors, calibrations, on="sensor_id")
print(f"Antall sensorer etter sammenslåing: {len(merged)}")

# 4. Filtrer ut sensorer som har gått over fristen
overdue = merged[merged["days_since_calibration"] > max_days]
print(f"Antall sensorer som er over fristen: {len(overdue)}")

# Velg bare kolonnene oppgaven ber om (de som finnes i dataene)
wanted = ["sensor_id", "lab_room", "owner", "days_since_calibration"]
columns = [c for c in wanted if c in overdue.columns]
overdue = overdue[columns]

# 5. Eksporter til JSON
records = overdue.to_dict(orient="records")
with open(output_file, "w") as f:
    json.dump(records, f, indent=2, default=str)

print(f"Skrev {len(records)} sensorer til {output_file}")