# scripts/generate_fake_data.py
import pandas as pd
import time
import random

fake_rows = []
for _ in range(50):
    fake_rows.append({
        'timestamp': time.time() + random.random(),
        'can_id': 0x666,
        'byte0': 0xFF,
        'byte1': 0x11,
        'byte2': 0x22,
        'byte3': 0x33,
        'byte4': 0x44,
        'byte5': 0x55,
        'byte6': 0x66,
        'byte7': 0x77,
        'label': 'attack'
    })

df_fake = pd.DataFrame(fake_rows)
df_fake.to_csv("data/fake_attacks.csv", index=False)
print("✅ Fake attack data with timestamp saved.")
