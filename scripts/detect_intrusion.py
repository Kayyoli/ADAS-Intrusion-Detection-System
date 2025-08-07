# scripts/detect_intrusion.py
import can
import joblib
import pandas as pd

model = joblib.load("model/can_intrusion_model.pkl")
bus = can.interface.Bus(channel='vcan0', bustype='socketcan')

print("🔍 Listening on vcan0 for intrusions...")

try:
    while True:
        msg = bus.recv()
        data = {
            'timestamp': msg.timestamp,
            'can_id': msg.arbitration_id
        }

        for i in range(8):
            data[f'byte{i}'] = msg.data[i] if i < len(msg.data) else 0

        df = pd.DataFrame([data])

        # Drop timestamp column before prediction
        features = df.drop(columns=['timestamp'], errors='ignore')
        prediction = model.predict(features)[0]

        if prediction == 'attack':
            print(f"🚨 [INTRUSION DETECTED] CAN ID: {hex(data['can_id'])}, Data: {msg.data.hex()}")
        else:
            print(f"[NORMAL] CAN ID: {hex(data['can_id'])}")

except KeyboardInterrupt:
    print("⛔ Stopped.")
