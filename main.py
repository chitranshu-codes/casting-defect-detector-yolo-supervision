import cv2
import supervision as sv
from ultralytics import YOLO
import os
import time

# --- CONFIGURATION ---
# Use '0' for default webcam, or '1' for external USB camera
CAMERA_INDEX = 0 
MODEL_PATH = "best.pt"
EVIDENCE_FOLDER = "rejected_logs"

# Ensure folder exists
os.makedirs(EVIDENCE_FOLDER, exist_ok=True)

def main():
    # 1. Load Model
    print("Loading model...")
    model = YOLO(MODEL_PATH)

    # 2. Setup Webcam
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Get webcam resolution
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # 3. Define the Line (Vertical Line in the Middle)
    # Since you will likely hold objects and move them Left-to-Right
    start_point = sv.Point(width // 2, 0)
    end_point = sv.Point(width // 2, height)
    
    line_zone = sv.LineZone(start=start_point, end=end_point)

    # 4. Annotators
    box_annotator = sv.BoxAnnotator(thickness=2)
    label_annotator = sv.LabelAnnotator(text_scale=0.5, text_thickness=1)
    dot_annotator = sv.DotAnnotator(color=sv.Color.WHITE, radius=5)
    
    line_annotator = sv.LineZoneAnnotator(
        thickness=2, text_thickness=1, text_scale=0.5,
        display_in_count=False, display_out_count=False
    )

    print("🚀 System Active. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # A. Tracking
        results = model.track(frame, persist=True, verbose=False)[0]
        detections = sv.Detections.from_ultralytics(results)
        
        # If no detections, just show the line and frame
        if detections.tracker_id is None:
            line_annotator.annotate(frame, line_counter=line_zone)
            cv2.imshow("Quality Control System", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break
            continue

        # B. Trigger Logic
        crossed_in, crossed_out = line_zone.trigger(detections=detections)

        # C. Evidence Logging
        if any(crossed_in) or any(crossed_out):
            timestamp = time.strftime("%H-%M-%S")
            ms = int(time.time() * 1000) % 1000
            filename = f"{EVIDENCE_FOLDER}/defect_{timestamp}_{ms}.jpg"
            cv2.imwrite(filename, frame) # Save raw frame or annotated_frame
            print(f"📸 Rejected! Saved: {filename}")

        # D. Annotate Frame
        labels = [f"#{tracker_id} {model.model.names[class_id]}"
                  for class_id, tracker_id in zip(detections.class_id, detections.tracker_id)]

        frame = box_annotator.annotate(frame, detections=detections)
        frame = label_annotator.annotate(frame, detections=detections, labels=labels)
        frame = dot_annotator.annotate(frame, detections=detections)
        line_annotator.annotate(frame, line_counter=line_zone)

        # E. Dashboard Text
        total_count = line_zone.in_count + line_zone.out_count
        cv2.putText(frame, f"REJECTED: {total_count}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # F. Show Live
        cv2.imshow("Quality Control System", frame)

        # Exit logic
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()