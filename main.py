from vehicle_manager import (
    register_vehicle,
    view_vehicles,
    search_vehicle
)

from slot_manager import (
    initialize_slots,
    view_slots
)

from parking_manager import (
    vehicle_entry,
    vehicle_exit,
    active_parking
)

from billing_manager import (
    view_completed_bills,
    search_parking_bill
)

from report_manager import (
    parking_statistics,
    daily_revenue_report,
    slot_availability_report,
    vehicle_type_report
)


def main():
    initialize_slots()

    actions = {
        "1": register_vehicle,
        "2": view_vehicles,
        "3": search_vehicle,
        "4": view_slots,
        "5": vehicle_entry,
        "6": vehicle_exit,
        "7": active_parking,
        "8": view_completed_bills,
        "9": search_parking_bill,
        "10": parking_statistics,
        "11": daily_revenue_report,
        "12": slot_availability_report,
        "13": vehicle_type_report
    }

    while True:
        print("\n" + "=" * 48)
        print("       PARKING LOT MANAGEMENT SYSTEM")
        print("=" * 48)

        print("1. Register Vehicle")
        print("2. View Registered Vehicles")
        print("3. Search Vehicle")
        print("4. View Parking Slots")
        print("5. Record Vehicle Entry")
        print("6. Record Vehicle Exit")
        print("7. View Currently Parked Vehicles")
        print("8. View Completed Parking Bills")
        print("9. Search Parking Bill")
        print("10. Parking Statistics")
        print("11. Daily Revenue Report")
        print("12. Slot Availability Report")
        print("13. Vehicle Type Report")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("Thank you for using the Parking Lot Management System!")
            break

        action = actions.get(choice)

        if action:
            try:
                action()
            except (RuntimeError, OSError) as error:
                print("An error occurred:", error)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
