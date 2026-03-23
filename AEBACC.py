import cv2
import time
from ultralytics import YOLO
import glob
import sys
#from parking import ParkingDetector

# ----------------------------
# CONFIG
# ----------------------------
MODEL_NAME = "yolov8n.pt"
FOCAL_LENGTH = 800       # approximate camera focal length
REAL_HEIGHT = 1.5        # average vehicle height (meters)

image_files = sorted(glob.glob("training/image_2/*.png"))

# ----------------------------
# Initialize
# ----------------------------
model = YOLO(MODEL_NAME)
class_names = model.names

prev_dist = None
prev_time = time.time()

VEHICLE_CLASSES = [2, 3, 5, 7]  # car, motorcycle, bus, truck

# ----------------------------
# Helper Functions
# ----------------------------
def select_lead_vehicle(boxes, frame_width):
    center_x = frame_width // 2
    best = None
    min_offset = 1e9
    for box in boxes:
        x1, y1, x2, y2 = box
        obj_center = (x1 + x2) // 2
        offset = abs(obj_center - center_x)
        if offset < min_offset:
            min_offset = offset
            best = box
    return best

def estimate_distance(box):
    x1, y1, x2, y2 = box
    h = y2 - y1
    if h <= 0:
        return None
    return (REAL_HEIGHT * FOCAL_LENGTH) / h

def compute_ttc(dist, rel_speed):
    if rel_speed <= 0:
        return float("inf")
    return dist / rel_speed

def decide(ttc):
    if ttc < 1.5:
        return "AEB BRAKE!", (0, 0, 255)
    elif ttc < 3:
        return "ACC SLOW DOWN", (0, 165, 255)
    else:
        return "SAFE", (0, 255, 0)


def fcw_decision(ttc):
    if ttc < 1.0:
        return "HIGH RISK", (0, 0, 255)
    elif ttc < 2.0:
        return "WARNING", (0, 165, 255)
    elif ttc < 3.0:
        return "CAUTION", (0, 255, 255)
    else:
        return "SAFE", (0, 255, 0)

# ----------------------------
# Main Loop (User Controlled)
# ----------------------------
cv2.namedWindow("ACC / AEB Demo", cv2.WINDOW_NORMAL)

i = 0
while i < len(image_files):
    img_path = image_files[i]
    frame = cv2.imread(img_path)
    if frame is None:
        i += 1
        continue

    frame_h, frame_w = frame.shape[:2]
    results = model(frame, verbose=False)
    boxes = []
    detection_counts = {}  # initialize per frame

    # ----------------------------
    # Detection loop
    # ----------------------------
    for r in results:
        for b in r.boxes:
            cls = int(b.cls[0])
            label = class_names[cls]

            # Get bounding box coordinates
            x1, y1, x2, y2 = map(int, b.xyxy[0])

            # Count detections
            detection_counts[label] = detection_counts.get(label, 0) + 1

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 1)

            # Draw label above box
            cv2.putText(frame, label, (x1, y1 - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Filter only vehicle classes for ACC/AEB
            if cls in VEHICLE_CLASSES:
                boxes.append((x1, y1, x2, y2))

    # Print object counts per frame
    print("Detections:", detection_counts)

    # ----------------------------
    # ACC / AEB logic
    # ----------------------------
    # Situation Interpretation -->  select_lead_vehicle + estimate_distance + compute_ttc
    # Decision Making   & Planning       -->  decide
    lead_box = select_lead_vehicle(boxes, frame_w)
    if lead_box is not None:
        dist = estimate_distance(lead_box)
        curr_time = time.time()
        dt = curr_time - prev_time
        prev_time = curr_time

        if prev_dist is not None and dist is not None and dt > 0:
            rel_speed = (prev_dist - dist) / dt
        else:
            rel_speed = 0

        prev_dist = dist
        ttc = compute_ttc(dist, rel_speed)
        status, color = decide(ttc)

        print(f"Distance: {dist:.2f} m | RelSpeed: {rel_speed:.2f} m/s | TTC: {ttc:.2f} s | Status: {status}")

        x1, y1, x2, y2 = lead_box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)

        info = f"D:{dist:.1f}m TTC:{ttc:.1f}s {status}"
        cv2.putText(frame, info, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # ----------------------------
    # Show frame
    # ----------------------------
    cv2.imshow("ACC / AEB Demo", frame)
    key = cv2.waitKey(0) & 0xFF   # Mask with 0xFF for Ubuntu/Linux
    
    if key == ord('n'):            # Next image
        i += 1
    elif key == ord('q'):          # Quit completely
        cv2.destroyAllWindows()
        sys.exit()

# Cleanup (just in case)
#cv2.destroyAllWindows()#    key = cv2.waitKey(0)

    if key == ord('n'):   # next image
        i += 1
    elif key == ord('q'): # quit
        break

# Cleanup
cv2.destroyAllWindows()