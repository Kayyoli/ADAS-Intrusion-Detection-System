import can
import joblib
import pandas as pd
import threading
import tkinter as tk
from tkinter import scrolledtext, filedialog

# Load the trained model
model = joblib.load("model/can_intrusion_model.pkl")

# Setup CAN interface
bus = can.interface.Bus(channel='vcan0', interface='socketcan')

# GUI Setup
root = tk.Tk()
root.title("CAN Intrusion Detection System")
root.geometry("800x550")

filter_enabled = tk.BooleanVar(value=True)
attack_count = tk.IntVar(value=0)

# Status Label
status_label = tk.Label(root, text="Status: Monitoring CAN Bus", font=("Helvetica", 16))
status_label.pack(pady=10)

# Toggle Filter Checkbox
filter_checkbox = tk.Checkbutton(root, text="Show Only CAN ID 0x666", variable=filter_enabled)
filter_checkbox.pack()

# Attack Count Label
attack_label = tk.Label(root, text="Intrusions Detected: 0", font=("Helvetica", 12), fg="red")
attack_label.pack(pady=5)

# Log Output
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=95, height=25)
log_text.pack(padx=10, pady=10)

# Save Log to File
def save_log():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(log_text.get("1.0", tk.END))

save_button = tk.Button(root, text="💾 Save Log", command=save_log)
save_button.pack(pady=5)

def monitor_can():
    while True:
        msg = bus.recv()

        if filter_enabled.get() and msg.arbitration_id != 0x666:
            continue

        data = {
            'timestamp': msg.timestamp,
            'can_id': msg.arbitration_id
        }

        for i in range(8):
            data[f'byte{i}'] = msg.data[i] if i < len(msg.data) else 0

        df = pd.DataFrame([data])
        features = df.drop(columns=['timestamp'], errors='ignore')
        prediction = model.predict(features)[0]

        log = f"CAN ID: {hex(data['can_id'])}, Data: {msg.data.hex()}"

        if prediction == 'attack':
            status_label.config(text="Status: 🚨 Intrusion Detected!", fg="red")
            log_text.insert(tk.END, f"[ALERT] {log}\n")
            attack_count.set(attack_count.get() + 1)
            attack_label.config(text=f"Intrusions Detected: {attack_count.get()}")
        else:
            status_label.config(text="Status: ✅ Normal", fg="green")
            log_text.insert(tk.END, f"[INFO] {log}\n")

        log_text.see(tk.END)

# Start background thread for monitoring
thread = threading.Thread(target=monitor_can, daemon=True)
thread.start()

# Run the GUI
root.mainloop()
