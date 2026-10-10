from config import SLOT_FILE, SLOT_COUNTS
from storage import load_data, save_data


def initialize_slots():
    slots = load_data(SLOT_FILE)

    if slots:
        return

    for vehicle_type, count in SLOT_COUNTS.items():
        prefix = vehicle_type[:3].upper()

        for number in range(1, count + 1):
            slots.append({
                "id": f"{prefix}-{number:03d}",
                "vehicle_type": vehicle_type,
                "occupied": False,
                "parking_id": None
            })

    save_data(SLOT_FILE, slots)


def view_slots():
    initialize_slots()
    slots = load_data(SLOT_FILE)

    print("\n========== PARKING SLOT STATUS ==========")

    for vehicle_type in SLOT_COUNTS:
        type_slots = [
            slot for slot in slots
            if slot["vehicle_type"] == vehicle_type
        ]

        available = sum(
            1 for slot in type_slots
            if not slot["occupied"]
        )

        print(f"\n{vehicle_type}")
        print(
            f"Available: {available}/{len(type_slots)}"
        )

        for slot in type_slots:
            status = (
                "Occupied" if slot["occupied"]
                else "Available"
            )

            print(f"  {slot['id']} - {status}")


def find_available_slot(vehicle_type):
    initialize_slots()
    slots = load_data(SLOT_FILE)

    return next(
        (
            slot for slot in slots
            if slot["vehicle_type"] == vehicle_type
            and not slot["occupied"]
        ),
        None
    )


def occupy_slot(slot_id, parking_id):
    slots = load_data(SLOT_FILE)

    for slot in slots:
        if slot["id"] == slot_id:
            if slot["occupied"]:
                raise ValueError("Parking slot is already occupied.")

            slot["occupied"] = True
            slot["parking_id"] = parking_id
            save_data(SLOT_FILE, slots)
            return

    raise ValueError("Parking slot not found.")


def release_slot(slot_id, parking_id):
    slots = load_data(SLOT_FILE)

    for slot in slots:
        if slot["id"] == slot_id:
            if (
                not slot["occupied"]
                or slot["parking_id"] != parking_id
            ):
                raise ValueError(
                    "Slot does not belong to this parking record."
                )

            slot["occupied"] = False
            slot["parking_id"] = None
            save_data(SLOT_FILE, slots)
            return

    raise ValueError("Parking slot not found.")
