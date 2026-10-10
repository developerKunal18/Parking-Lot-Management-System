import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

VEHICLE_FILE = os.path.join(DATA_DIR, "vehicles.json")
SLOT_FILE = os.path.join(DATA_DIR, "slots.json")
PARKING_FILE = os.path.join(DATA_DIR, "parking_records.json")

VEHICLE_TYPES = {
    "1": {"name": "Bike", "hourly_rate": 10},
    "2": {"name": "Car", "hourly_rate": 30},
    "3": {"name": "Heavy Vehicle", "hourly_rate": 50},
}

SLOT_COUNTS = {
    "Bike": 10,
    "Car": 10,
    "Heavy Vehicle": 5,
}

# Minimum charge is one hour. Additional time is rounded up
# to the next whole hour.
MINIMUM_CHARGE_HOURS = 1
