import pandas as pd
import os

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Load raw CAN data
df = pd.read_csv("data/can_data.csv")

# Extract each byte from hex string in 'data' column
def extract_bytes(hex_data):
    hex_data = hex_data.ljust(16, '0')  # pad to 8 bytes if short
    return [int(hex_data[i:i+2], 16) for i in range(0, 16, 2)]

# Apply feature extraction
byte_columns = ['byte0', 'byte1', 'byte2', 'byte3', 'byte4', 'byte5', 'byte6', 'byte7']
features = df['data'].apply(extract_bytes).apply(pd.Series)
features.columns = byte_columns

# Combine with CAN ID and timestamp
df_final = pd.concat([df[['timestamp', 'can_id']], features], axis=1)

# Add labels (0 = normal, 1 = attack)
# Example: label messages with can_id = 0x123 (291) as attack
df_final['label'] = 0
df_final.loc[df_final['can_id'] == 291, 'label'] = 1

# Save preprocessed dataset
df_final.to_csv("data/labeled_can_data.csv", index=False)
print("Preprocessing complete. Output saved to data/labeled_can_data.csv")
