import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from collections import defaultdict, deque

# Load the YOLO model
model = YOLO("/Users/seungwonlee/ObjectDetection_with_Server/yolov8s.pt")  # Use the appropriate YOLOv8 model variant

# Set up video paths
SOURCE_VIDEO_PATH = "/Users/seungwonlee/ObjectDetection_with_Server/target/140sDayShinjuku.mp4"
TARGET_VIDEO_PATH = "/Users/seungwonlee/ObjectDetection_with_Server/target/140sDayShinjuku_result.mp4"

# Initialize video capture
cap = cv2.VideoCapture(SOURCE_VIDEO_PATH)

# Video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Set output video to 1 FPS
output_fps = 1

# Define the desired resize scale (e.g., 0.5 for half the original size)
resize_scale = 0.5
resized_width = int(width * resize_scale)
resized_height = int(height * resize_scale)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(TARGET_VIDEO_PATH, fourcc, output_fps, (resized_width, resized_height))

# Initialize ByteTrack tracker
byte_track = sv.ByteTrack(
    track_activation_threshold=0.3,
    lost_track_buffer=30,
    frame_rate=output_fps
)

# Initialize data structures to store past positions for speed estimation
past_positions = defaultdict(lambda: deque(maxlen=5))
speeds = []
person_count = 0

# Assumed conversion factor from pixels to meters (this depends on the camera setup)
pixel_to_meter = 0.05  # 1 pixel = 0.05 meters (adjust based on your video)

# Process the video at 1 FPS
frame_index = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Only process 1 frame per second
    if frame_index % int(fps) == 0:
        # Resize the frame for faster processing
        frame = cv2.resize(frame, (resized_width, resized_height))

        # Run YOLO object detection
        results = model(frame, conf=0.5)  # Adjust confidence threshold as needed

        # Get detections
        detections = sv.Detections.from_ultralytics(results[0])

        # Filter detections by confidence
        detections = detections[detections.confidence > 0.3]

        # Update tracker with detections
        tracks = byte_track.update_with_detections(detections)

        # Annotate frame and calculate speed
        for track in tracks:
            track_id = track[0]
            bbox = track[1]  # Get bounding box coordinates
            class_id = track[2]  # Get the class ID

            # Ensure we're only processing persons (class ID for 'person' is usually 0)
            if class_id == 0:
                person_count += 1
                if bbox is not None:
                    # Draw the bounding box
                    x1, y1, x2, y2 = map(int, bbox)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Calculate speed estimation
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2

                    if track_id in past_positions:
                        past_positions[track_id].append((center_x, center_y))
                        if len(past_positions[track_id]) > 1:
                            # Calculate the displacement between the first and last positions
                            x_start, y_start = past_positions[track_id][0]
                            x_end, y_end = past_positions[track_id][-1]
                            distance_pixels = np.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)
                            distance_meters = distance_pixels * pixel_to_meter

                            # Calculate speed in meters per second (m/s)
                            time_seconds = len(past_positions[track_id]) / output_fps
                            speed_mps = distance_meters / time_seconds

                            # Convert speed to km/h
                            speed_kmph = speed_mps * 3.6
                            speeds.append(speed_kmph)

                            # Draw the speed category
                            cv2.putText(frame, f'Speed: {int(speed_kmph)} km/h', (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    else:
                        past_positions[track_id].append((center_x, center_y))

                    # Draw the track ID
                    cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Write the annotated frame to the output video
        out.write(frame)

        # Display the frame (optional)
        cv2.imshow('frame', frame) 

    frame_index += 1

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Calculate the median speed of persons
median_speed = np.median(speeds) if speeds else 0

# Save the results
print(f"Results saved to {TARGET_VIDEO_PATH}")
print(f"Median Speed of Persons: {median_speed:.2f} km/h")
print(f"Total Persons Detected: {person_count}")

