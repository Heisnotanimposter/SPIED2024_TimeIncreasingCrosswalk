
from flask import Flask, render_template, Response, jsonify, send_from_directory
import cv2
import numpy as np
from ultralytics import YOLO
import threading
import os

app = Flask(__name__)

# Load the YOLO model
model = YOLO("yolov8s.pt")

# Initialize counters and traffic light state
vehicle_count = {'Aphase': 0, 'Bphase': 0}
person_count = {'Aphase': 0, 'Bphase': 0}
traffic_light_state = {'Aphase': 'red', 'Bphase': 'red'}

# Define the green light phases
phases = {
    'Aphase': {'start': 28, 'end': 90, 'duration': 62, 'start_b': 170, 'end_b': 240, 'duration_b': 70},
    'Bphase': {'start': 108, 'end': 142, 'duration': 34, 'start_b': 247, 'end_b': 284, 'duration_b': 37}
}
median_A = (phases['Aphase']['duration'] + phases['Aphase']['duration_b']) // 2
median_B = (phases['Bphase']['duration'] + phases['Bphase']['duration_b']) // 2

# Define line positions
line_positions = {'vertical_line': (300, 0, 300, 640), 'horizontal_line': (0, 320, 480, 320)}

# Define the video path
SOURCE_VIDEO_PATH = "/Users/seungwonlee/ObjectDetection_with_Server/target/140sDayShinjuku.mp4"  # Adjust path
TARGET_VIDEO_PATH = "/Users/seungwonlee/ObjectDetection_with_Server/target/140sDayShinjuku_result.mp4"  # Adjust path

# Function to count detections in defined areas
def count_detections(frame, detections):
    global vehicle_count, person_count
    for detection in detections:
        if len(detection) < 6:
            print(f"Skipping detection due to insufficient data: {detection}")
            continue  # Skip if detection does not have enough data (e.g., missing class_id)
        x1, y1, x2, y2 = map(int, detection[:4])
        class_id = int(detection[5])

        if class_id in [2, 3, 5, 7]:  # Vehicle classes
            if x1 < 300:
                vehicle_count['Aphase'] += 1
            else:
                vehicle_count['Bphase'] += 1
            print(f"Vehicle detected in {'Aphase' if x1 < 300 else 'Bphase'}: {vehicle_count}")
        elif class_id == 0:  # Person class
            if y1 < 320:
                person_count['Aphase'] += 1
            else:
                person_count['Bphase'] += 1
            print(f"Person detected in {'Aphase' if y1 < 320 else 'Bphase'}: {person_count}")

# Background task to process video and update traffic light state
def process_video(video_path, output_path):
    global traffic_light_state, vehicle_count, person_count
    cap = cv2.VideoCapture(video_path)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, (640, 384))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLO object detection
        results = model(frame)
        
        # Extracting detections (using boxes attribute)
        detections = results[0].boxes.xyxy.cpu().numpy()  # Assuming detections in xyxy format

        # Count detections
        count_detections(frame, detections)

        # Update traffic light state based on counts
        if vehicle_count['Aphase'] > vehicle_count['Bphase']:
            traffic_light_state['Aphase'] = 'green'
            traffic_light_state['Bphase'] = 'red'
        else:
            traffic_light_state['Aphase'] = 'red'
            traffic_light_state['Bphase'] = 'green'

        # Annotate the frame
        for det in detections:
            if len(det) < 6:
                continue  # Skip if detection does not have enough data
            x1, y1, x2, y2 = map(int, det[:4])
            label = int(det[5])
            if label == 0:  # Person
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, 'Person', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif label in [2, 3, 5, 7]:  # Vehicle
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, 'Vehicle', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        out.write(frame)

    cap.release()
    out.release()

# Start the video processing in a separate thread
thread = threading.Thread(target=process_video, args=(SOURCE_VIDEO_PATH, TARGET_VIDEO_PATH))
thread.start()

# Define routes for the Flask app
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/traffic_state')
def traffic_state():
    print(f"Traffic Light State: {traffic_light_state}")
    return jsonify(traffic_light_state)

@app.route('/counts')
def counts():
    print(f"Vehicle Counts: {vehicle_count}, Person Counts: {person_count}")
    return jsonify({
        'vehicle_count': vehicle_count,
        'person_count': person_count
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
