# 🚗 CAN Bus Intrusion Detection System

This project is a real-time **CAN Bus Intrusion Detection System (IDS)** designed to detect fake or malicious CAN messages in vehicle networks. It uses machine learning to classify CAN data as normal or intrusion and includes a live GUI for monitoring.

---

## 🔐 Project Goal

To enhance **vehicle security** by detecting anomalies in CAN traffic using a trained machine learning model.

---

## 🛠️ Features-

- ✅ Real-time monitoring of CAN messages via `vcan0`
- ✅ GUI with live status, intrusion alerts, and logging
- ✅ Option to filter and focus on specific CAN IDs (e.g., `0x666`)
- ✅ Ability to inject fake CAN signals for testing
- ✅ Save log to file functionality

---

## 💻 Technology Stack

- **Python **
- **Tkinter** – GUI interface
- **Scikit-learn** – ML model (Random Forest Classifier)
- **pandas** – Data processing
- **python-can** – open source available in github  CAN bus interaction
- **joblib** – Model serialization

---

## 🛠️ How to Run?
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- sudo modprobe vcan
- sudo ip link add dev vcan0 type vcan
- sudo ip link set up vcan0
- python3 scripts/train_model.py
- python3 scripts/gui_intrusion_detection.py
