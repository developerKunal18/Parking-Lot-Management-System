from config import VEHICLE_FILE, VEHICLE_TYPES
from storage import load_data, save_data
from utils import generate_id, read_nonempty


def register_vehicle():
    vehicles = load_data(VEHICLE_FILE)

    registration = read_nonempty(
        "Vehicle Registration Number: "
    )

    if registration is None:
        return

    registration = registration.upper()

    if any(
        vehicle["registration"] == registration
        for vehicle in vehicles
    ):
        print("This vehicle is already registered.")
        return

    owner = read_nonempty("Owner Name: ")
    phone = read_nonempty("Phone Number: ")

    if owner is None or phone is None:
        return

    if not phone.isdigit() or not 10 <= len(phone) <= 15:
        print("Enter a valid phone number containing 10–15 digits.")
        return

    print("\nVehicle Types:")

    for key, details in VEHICLE_TYPES.items():
        print(f"{key}. {details['name']}")

    choice = input("Select vehicle type: ").strip()

    if choice not in VEHICLE_TYPES:
        print("Invalid vehicle type.")
        return

    vehicle_type = VEHICLE_TYPES[choice]["name"]

    vehicle = {
        "id": generate_id("VEH"),
        "registration": registration,
        "owner": owner,
        "phone": phone,
        "type": vehicle_type
    }

    vehicles.append(vehicle)
    save_data(VEHICLE_FILE, vehicles)

    print("\nVehicle registered successfully!")
    print("Vehicle ID:", vehicle["id"])


def view_vehicles():
    vehicles = load_data(VEHICLE_FILE)

    if not vehicles:
        print("No vehicles registered.")
        return

    print("\n========== REGISTERED VEHICLES ==========")

    for vehicle in vehicles:
        print("-" * 40)
        print("Vehicle ID:", vehicle["id"])
        print("Registration:", vehicle["registration"])
        print("Owner:", vehicle["owner"])
        print("Phone:", vehicle["phone"])
        print("Type:", vehicle["type"])


def search_vehicle():
    vehicles = load_data(VEHICLE_FILE)

    registration = input(
        "Enter registration number: "
    ).strip().upper()

    vehicle = next(
        (
            item for item in vehicles
            if item["registration"] == registration
        ),
        None
    )

    if vehicle:
        for key, value in vehicle.items():
            print(f"{key}: {value}")
    else:
        print("Vehicle not found.")
