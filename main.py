import cv2
import time
import glob
import requests
import json
import os
from ultralytics import YOLO

# ----------------------------
# OTA CONFIG LOAD
# ----------------------------
def load_config():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, "config", "adas_config.json")

        print(path)

        with open(path, "r") as f:
            return json.load(f)

    except Exception as e:
        print("Error:", e)
        print("Using default config (OTA failed)")
        return {
            "VERSION": "v1.0",
            "FEATURES": {"FCW": True, "ACC": True, "AEB": True},
            "ACC": {"time_gap": 2.0},
            "AEB": {"ttc_critical": 1.2},
            "FCW": {"ttc_warning": 2.5},
            "MODEL": {"path": "yolov8n.pt"}
        }

config = load_config()
# print("Running ADAS Version:", config["VERSION"])

# ----------------------------
# SERVICES
# ----------------------------
class FCWService:
    def __init__(self, cfg):
        self.ttc_warning = cfg["ttc_warning"]

    def evaluate(self, distance, rel_speed):
        if rel_speed <= 0:
            return {"status": "SAFE", "ttc": float('inf')}

        ttc = distance / rel_speed

        if ttc < self.ttc_warning:
            return {"status": "WARNING", "ttc": ttc}
        return {"status": "SAFE", "ttc": ttc}


class ACCService:
    def __init__(self, cfg):
        self.time_gap = cfg["time_gap"]

    def evaluate(self, ego_speed, distance):
        safe_dist = ego_speed * self.time_gap

        if distance < safe_dist:
            return "SLOW_DOWN"
        return "MAINTAIN"


class AEBService:
    def __init__(self, cfg):
        self.ttc_critical = cfg["ttc_critical"]

    def evaluate(self, distance, rel_speed):
        if rel_speed <= 0:
            return {"brake": False}

        ttc = distance / rel_speed

        return {
            "brake": ttc < self.ttc_critical,
            "ttc": ttc
        }

# ----------------------------
# INIT
# ----------------------------
model = YOLO(config["MODEL"]["path"])

FOCAL_LENGTH = 800
REAL_HEIGHT = 1.5

image_files = sorted(glob.glob("training/image_2/*.png"))

fcw = FCWService(config["FCW"])
acc = ACCService(config["ACC"])
aeb = AEBService(config["AEB"])

prev_distance = None
prev_time = time.time()

ego_speed = 10  # m/s (dummy)

# ----------------------------
# MAIN LOOP
# ----------------------------
for img_path in image_files:

    frame = cv2.imread(img_path)
    if frame is None:
        continue

    results = model(frame)[0]

    current_time = time.time()
    delta_time = current_time - prev_time

    for box in results.boxes:

        cls = int(box.cls[0])
        if cls != 2:  # car class (COCO)
            continue

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        bbox_height = y2 - y1

        if bbox_height <= 0:
            continue

        # ----------------------------
        # DISTANCE
        # ----------------------------
        distance = (FOCAL_LENGTH * REAL_HEIGHT) / bbox_height

        # ----------------------------
        # RELATIVE SPEED
        # ----------------------------
        if prev_distance is not None and delta_time > 0:
            rel_speed = (prev_distance - distance) / delta_time
        else:
            rel_speed = 0

        prev_distance = distance
        prev_time = current_time

        label = f"{distance:.1f}m"

        # ----------------------------
        # FCW
        # ----------------------------
        if config["FEATURES"]["FCW"]:
            fcw_out = fcw.evaluate(distance, rel_speed)
            label += f" | FCW: {fcw_out['status']}"

        # ----------------------------
        # ACC
        # ----------------------------
        if config["FEATURES"]["ACC"]:
            acc_out = acc.evaluate(ego_speed, distance)
            label += f" | ACC: {acc_out}"

        # ----------------------------
        # AEB
        # ----------------------------
        if config["FEATURES"]["AEB"]:
            aeb_out = aeb.evaluate(distance, rel_speed)
            if aeb_out["brake"]:
                label += " | AEB: BRAKE"

        # ----------------------------
        # DRAW
        # ----------------------------
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(frame, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    cv2.imshow("ADAS SDV Demo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()