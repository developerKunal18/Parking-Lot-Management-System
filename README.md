
# Parking Lot Management System

A Python command-line application for managing vehicle
registration, parking slots, vehicle entry and exit,
parking charges, and revenue reports.

## Features

- Vehicle registration and search
- Bike, car, and heavy vehicle support
- Automatic parking slot allocation
- Available and occupied slot tracking
- Vehicle entry and exit records
- Automatic parking charge calculation
- Parking bill generation
- Parking history and bill search
- Daily revenue reports
- Parking statistics
- Vehicle-type reports
- JSON-based data persistence

## Technologies Used

- Python
- JSON
- Datetime
- UUID
- OS

## Project Structure

```text
parking-lot-management/
├── main.py
├── config.py
├── storage.py
├── utils.py
├── vehicle_manager.py
├── slot_manager.py
├── parking_manager.py
├── billing_manager.py
├── report_manager.py
├── data/
│   ├── vehicles.json
│   ├── slots.json
│   └── parking_records.json
├── .gitignore
└── README.md
```

## Installation

Clone your repository:

```bash
git clone https://github.com/yourusername/parking-lot-management.git
```

Navigate to the project directory:

```bash
cd parking-lot-management
```

Run the application:

```bash
python main.py
```

No external packages are required.

## How to Use

1. Register a vehicle.
2. View the available parking slots.
3. Record vehicle entry using its registration number.
4. Note the generated Parking ID.
5. Record vehicle exit using the Parking ID.
6. View the calculated parking bill.
7. Generate daily revenue and parking reports.

## Sample Parking Charges

| Vehicle | Hourly Rate |
|---|---:|
| Bike | ₹10 |
| Car | ₹30 |
| Heavy Vehicle | ₹50 |

The sample program charges a minimum of one hour
and rounds partial hours up to the next hour.

## Example

Vehicle Type: Car

Parking Duration: 2 hours

Hourly Rate: ₹30

Total Parking Charge: ₹60

## Future Improvements

- Django web application
- MySQL database
- Admin authentication
- QR code parking tickets
- Monthly parking subscriptions
- PDF receipt generation
- Online payment integration
- Interactive parking dashboard
- Export reports to Excel

## Author

Kunal Karbhari

GitHub: https://github.com/developerKunal18

## Challenge

365 Days of Python Projects

Day 352 Completed
