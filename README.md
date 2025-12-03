# 🏭 Automated Quality Control & Defect Detection System

### A Computer Vision application simulating an industrial conveyor belt inspection system.

[](./rejected_logs/defect_detected_19-08-56_635.jpg)

---

## 📖 Project Overview
This project bridges the gap between **Mechanical Engineering** and **Artificial Intelligence**. It simulates a manufacturing Quality Control (QC) station where parts are inspected in real-time.

Instead of passive detection, this system acts as an **Active Logic Controller**:
1.  **Detects** casting defects (Blowholes) using a custom-trained YOLOv8 model.
2.  **Tracks** unique parts across the frame using ByteTrack (preventing double-counting).
3.  **Counts** throughput using a virtual sensor (Line Crossing Logic).
4.  **Logs Evidence** by automatically saving high-res snapshots of rejected parts for quality auditing.

## ⚙️ Key Features
* **Real-Time Inference:** Runs live on webcam/USB camera feeds.
* **Object Tracking:** utilizes `ByteTrack` to assign persistent IDs to moving parts, ensuring robust counting even if detection flickers.
* **Virtual Sensor Zone:** A defined vertical trigger line simulates a physical photoelectric sensor.
* **Automated Audit Log:** Automatically creates a `rejected_logs/` directory and saves time-stamped images of every defect found.
* **Visual Dashboard:** Displays live production counts and visual feedback (Bounding Boxes + Tracker IDs) on the screen.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Core Model:** YOLOv8 (Ultralytics) - Custom trained on Casting Defect Dataset.
* **Computer Vision:** OpenCV (Video processing).
* **Logic & Analytics:** Supervision (Roboflow) for line-zone math and annotators.

## 🕹️ Usage Guide
* **Camera Setup:** The script defaults to `CAMERA_INDEX = 0` (Webcam). If using an external USB industrial camera, change this to `1` in `main.py`.
* **Line Configuration:** The system is currently configured for objects moving **Left-to-Right** (Vertical Line in the center).
    * *To change to Top-to-Bottom:* Modify the `start_point` and `end_point` coordinates in `main.py` lines 34-35.
* **Exit:** Press `q` to stop the system.

## 🧠 Engineering Logic
The system uses a **Center-Point Crossing Logic** to trigger the counter:

1.  **Detection:** YOLOv8 identifies a defect and generates a Bounding Box.
2.  **Tracking:** The center pixel of the box is calculated.
3.  **Trigger:** When the center pixel crosses the defined Virtual Line:
    * `Total Count` increments by +1.
    * The frame is captured and written to disk (`cv2.imwrite`).
    * A visual alert is displayed on the dashboard.

## 🔜 Future Improvements
* [ ] Integration with PLC (Programmable Logic Controller) via Modbus/MQTT to trigger physical reject arms.
* [ ] Database integration (SQL) for long-term production statistics.
* [ ] Web-based Dashboard using Streamlit for remote monitoring.

---
