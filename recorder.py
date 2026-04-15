import cv2
import os
import time
from datetime import datetime

SAVE_FOLDER = "videos"
RECORD_SECONDS = 10
INTERVAL_SECONDS = 120   # 2 minutes
FPS = 20.0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

os.makedirs(SAVE_FOLDER, exist_ok=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

print("Recorder started. Press Ctrl+C to stop.")

try:
    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_{timestamp}.mp4"
        filepath = os.path.join(SAVE_FOLDER, filename)

        out = cv2.VideoWriter(filepath, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))

        print(f"Recording {filename} ...")
        start_time = time.time()

        while time.time() - start_time < RECORD_SECONDS:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            out.write(frame)

        out.release()
        print(f"Saved: {filepath}")
        print("Waiting for next recording...\n")

        time.sleep(INTERVAL_SECONDS)

except KeyboardInterrupt:
    print("Recorder stopped by user.")

cap.release()