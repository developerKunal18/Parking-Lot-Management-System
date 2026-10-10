from datetime import datetime

from config import (
    VEHICLE_FILE,
    PARKING_FILE,
    VEHICLE_TYPES
)
from storage import load_data, save_data
from utils import (
    generate_id,
    current_datetime,
    parse_datetime,
    money
)
from slot_manager import (
    find_available_slot,
    occupy_slot,
    release_slot
)


def vehicle_entry():
    vehicles = load_data(VEHICLE_FILE)
    records = load_data(PARKING_FILE)

    registration = input(
        "Vehicle Registration Number: "
    ).strip().upper()

    vehicle = next(
        (
            item for item in vehicles
            if item["registration"] == registration
        ),
        None
    )

    if not vehicle:
        print("Vehicle not registered. Register it first.")
        return

    already_parked = any(
        record["vehicle_id"] == vehicle["id"]
        and record["status"] == "Parked"
        for record in records
    )

    if already_parked:
        print("This vehicle is already parked.")
        return

    slot = find_available_slot(vehicle["type"])

    if not slot:
        print(f"No available slots for {vehicle['type']}.")
        return

    parking_id = generate_id("PKG")
    entry_time = current_datetime()

    record = {
        "id": parking_id,
        "vehicle_id": vehicle["id"],
        "registration": vehicle["registration"],
        "owner": vehicle["owner"],
        "vehicle_type": vehicle["type"],
        "slot_id": slot["id"],
        "entry_time": entry_time,
        "exit_time": None,
        "duration_hours": None,
        "charge": None,
        "status": "Parked"
    }

    # Save the parking record first so that the slot can
    # be associated with a real parking record.
    records.append(record)
    save_data(PARKING_FILE, records)

    try:
        occupy_slot(slot["id"], parking_id)
    except (ValueError, RuntimeError) as error:
        # Roll back the newly added record if slot allocation fails.
        records = load_data(PARKING_FILE)
        records = [
            item for item in records
            if item["id"] != parking_id
        ]
        save_data(PARKING_FILE, records)

        print("Unable to allocate slot:", error)
        return

    print("\nVehicle entry recorded!")
    print("Parking ID:", parking_id)
    print("Registration:", vehicle["registration"])
    print("Assigned Slot:", slot["id"])
    print("Entry Time:", entry_time)


def vehicle_exit():
    records = load_data(PARKING_FILE)

    parking_id = input("Enter Parking ID: ").strip()

    record = next(
        (
            item for item in records
            if item["id"] == parking_id
            and item["status"] == "Parked"
        ),
        None
    )

    if not record:
        print("Active parking record not found.")
        return

    exit_time = datetime.now()
    entry_time = parse_datetime(record["entry_time"])

    seconds = (exit_time - entry_time).total_seconds()

    if seconds < 0:
        print("Exit time cannot be earlier than entry time.")
        return

    # Charge at least one hour; any partial hour is rounded up.
    duration_hours = max(1, int((seconds + 3599) // 3600))

    hourly_rate = VEHICLE_TYPES_BY_NAME(record["vehicle_type"])

    if hourly_rate is None:
        print("Unknown vehicle type. Cannot calculate fee.")
        return

    charge = round(duration_hours * hourly_rate, 2)
    formatted_exit = exit_time.strftime("%Y-%m-%d %H:%M:%S")

    # Release the slot before closing the record.
    try:
        release_slot(record["slot_id"], parking_id)
    except (ValueError, RuntimeError) as error:
        print("Unable to release parking slot:", error)
        return

    record["exit_time"] = formatted_exit
    record["duration_hours"] = duration_hours
    record["charge"] = charge
    record["status"] = "Exited"

    try:
        save_data(PARKING_FILE, records)
    except RuntimeError as error:
        # Best-effort recovery: restore slot occupancy if saving
        # the exit record fails.
        try:
            occupy_slot(record["slot_id"], parking_id)
        except (ValueError, RuntimeError):
            pass

        print("Unable to save exit record:", error)
        return

    print("\n========== PARKING EXIT ==========")
    print("Parking ID:", parking_id)
    print("Registration:", record["registration"])
    print("Slot:", record["slot_id"])
    print("Entry:", record["entry_time"])
    print("Exit:", formatted_exit)
    print("Billable Hours:", duration_hours)
    print("Hourly Rate:", money(hourly_rate))
    print("Total Charge:", money(charge))
    print("==================================")


def VEHICLE_TYPES_BY_NAME(vehicle_type):
    for details in VEHICLE_TYPES.values():
        if details["name"] == vehicle_type:
            return details["hourly_rate"]

    return None


def active_parking():
    records = load_data(PARKING_FILE)

    active = [
        record for record in records
        if record["status"] == "Parked"
    ]

    if not active:
        print("No vehicles are currently parked.")
        return

    print("\n========== CURRENTLY PARKED ==========")

    for record in active:
        print("-" * 40)
        print("Parking ID:", record["id"])
        print("Registration:", record["registration"])
        print("Owner:", record["owner"])
        print("Type:", record["vehicle_type"])
        print("Slot:", record["slot_id"])
        print("Entry:", record["entry_time"])
