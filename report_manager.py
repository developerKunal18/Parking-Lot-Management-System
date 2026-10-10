from datetime import datetime

from config import PARKING_FILE, SLOT_FILE
from storage import load_data
from slot_manager import initialize_slots
from utils import money


def parking_statistics():
    records = load_data(PARKING_FILE)

    total_sessions = len(records)

    active = [
        record for record in records
        if record["status"] == "Parked"
    ]

    completed = [
        record for record in records
        if record["status"] == "Exited"
    ]

    cancelled = [
        record for record in records
        if record["status"] == "Cancelled"
    ]

    revenue = sum(
        record["charge"] or 0
        for record in completed
    )

    print("\n========== PARKING STATISTICS ==========")
    print("Total Parking Sessions:", total_sessions)
    print("Currently Parked:", len(active))
    print("Completed Sessions:", len(completed))
    print("Cancelled Sessions:", len(cancelled))
    print("Total Revenue:", money(revenue))
    print("=" * 40)


def daily_revenue_report():
    records = load_data(PARKING_FILE)
    today = datetime.now().strftime("%Y-%m-%d")

    completed_today = [
        record for record in records
        if record["status"] == "Exited"
        and record["exit_time"]
        and record["exit_time"].startswith(today)
    ]

    revenue = sum(
        record["charge"] or 0
        for record in completed_today
    )

    print("\n========== DAILY REVENUE REPORT ==========")
    print("Date:", today)
    print("Vehicles Exited:", len(completed_today))
    print("Revenue:", money(revenue))
    print("=" * 40)


def slot_availability_report():
    initialize_slots()
    slots = load_data(SLOT_FILE)

    print("\n========== SLOT AVAILABILITY ==========")

    vehicle_types = sorted(
        set(slot["vehicle_type"] for slot in slots)
    )

    for vehicle_type in vehicle_types:
        matching = [
            slot for slot in slots
            if slot["vehicle_type"] == vehicle_type
        ]

        available = sum(
            1 for slot in matching
            if not slot["occupied"]
        )

        occupied = len(matching) - available

        print(f"\n{vehicle_type}")
        print("Total Slots:", len(matching))
        print("Available:", available)
        print("Occupied:", occupied)


def vehicle_type_report():
    records = load_data(PARKING_FILE)

    print("\n========== VEHICLE TYPE REPORT ==========")

    vehicle_types = sorted(
        set(record["vehicle_type"] for record in records)
    )

    if not vehicle_types:
        print("No parking records available.")
        return

    for vehicle_type in vehicle_types:
        matching = [
            record for record in records
            if record["vehicle_type"] == vehicle_type
        ]

        completed = [
            record for record in matching
            if record["status"] == "Exited"
        ]

        revenue = sum(
            record["charge"] or 0
            for record in completed
        )

        print("-" * 35)
        print("Vehicle Type:", vehicle_type)
        print("Total Sessions:", len(matching))
        print("Completed Sessions:", len(completed))
        print("Revenue:", money(revenue))
