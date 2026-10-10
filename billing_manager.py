from config import PARKING_FILE
from storage import load_data
from utils import money


def view_completed_bills():
    records = load_data(PARKING_FILE)

    completed = [
        record for record in records
        if record["status"] == "Exited"
    ]

    if not completed:
        print("No completed parking bills found.")
        return

    print("\n========== COMPLETED PARKING BILLS ==========")

    for record in completed:
        print("-" * 45)
        print("Parking ID:", record["id"])
        print("Vehicle:", record["registration"])
        print("Owner:", record["owner"])
        print("Entry:", record["entry_time"])
        print("Exit:", record["exit_time"])
        print("Hours:", record["duration_hours"])
        print("Charge:", money(record["charge"]))


def search_parking_bill():
    records = load_data(PARKING_FILE)

    parking_id = input("Enter Parking ID: ").strip()

    record = next(
        (
            item for item in records
            if item["id"] == parking_id
        ),
        None
    )

    if not record:
        print("Parking record not found.")
        return

    print("\n========== PARKING BILL ==========")
    print("Parking ID:", record["id"])
    print("Vehicle:", record["registration"])
    print("Vehicle Type:", record["vehicle_type"])
    print("Owner:", record["owner"])
    print("Slot:", record["slot_id"])
    print("Entry Time:", record["entry_time"])
    print("Exit Time:", record["exit_time"] or "Not exited")
    print("Status:", record["status"])

    if record["charge"] is not None:
        print("Billable Hours:", record["duration_hours"])
        print("Total Charge:", money(record["charge"]))
    else:
        print("Charge will be calculated at vehicle exit.")

    print("=" * 36)
