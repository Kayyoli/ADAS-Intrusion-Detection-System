import can
import csv
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# Connect to virtual CAN interface
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Open CSV file for writing
with open('data/can_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "can_id", "data"])  # header row

    print("Logging CAN data from vcan0... Press Ctrl+C to stop.")
    try:
        while True:
            msg = bus.recv()
            writer.writerow([msg.timestamp, msg.arbitration_id, msg.data.hex()])
    except KeyboardInterrupt:
        print("CAN logging stopped.")
