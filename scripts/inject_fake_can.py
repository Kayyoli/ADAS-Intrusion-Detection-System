import can
import random
import time

# Setup virtual CAN interface
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

# Define fake attack CAN IDs and data
attack_ids = [0x666, 0x999, 0x123]
attack_payloads = [
    bytes.fromhex("DEADBEEF12345678"),
    bytes.fromhex("1122334455667788"),
    bytes.fromhex("FFEECCDDBBAA9988")
]

print("🚨 Injecting fake CAN attacks on vcan0... Press Ctrl+C to stop.")

try:
    while True:
        # Pick a random fake ID and payload
        fake_id = random.choice(attack_ids)
        fake_data = random.choice(attack_payloads)
        
        msg = can.Message(arbitration_id=fake_id, data=fake_data, is_extended_id=False)
        bus.send(msg)

        print(f"✅ Sent fake msg: ID={hex(fake_id)}, Data={fake_data.hex()}")
        time.sleep(random.uniform(1.5, 3))  # inject every 1.5–3 seconds

except KeyboardInterrupt:
    print("\nStopped injection.")
