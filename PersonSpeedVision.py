import cv2
import numpy as np
from ultralytics import YOLO
import supervision as sv
from collections import defaultdict, deque
from google.colab.patches import cv2_imshow

# Load the YOLO model
model = YOLO("yolov8s.pt")  # Use the appropriate YOLOv8 model variant

# Set up video paths
SOURCE_VIDEO_PATH = "/content/drive/MyDrive/Team7dataset/Team7Shared/140sNightShinjuku.mp4"
TARGET_VIDEO_PATH = "/content/drive/MyDrive/Team7dataset/Team7Shared/140sNightShinjuku_yolov8_result.mp4"

# Initialize video capture
cap = cv2.VideoCapture(SOURCE_VIDEO_PATH)

# Video properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(TARGET_VIDEO_PATH, fourcc, fps, (width, height))

# Initialize ByteTrack tracker
byte_track = sv.ByteTrack(
    track_activation_threshold=0.3,
    lost_track_buffer=30,
    frame_rate=fps
)

# Initialize data structures to store past positions for speed estimation
past_positions = defaultdict(lambda: deque(maxlen=5))

# Placeholder for the conversion factor
pixel_to_meter = None

# Known average walking speed (6 km/h in meters per second)
average_walking_speed_mps = 6 * 1000 / 3600  # 6 km/h = 1.67 meters/second

# Process the video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO object detection
    results = model(frame, conf=0.5)  # Adjust confidence threshold as needed

    # Get detections
    detections = sv.Detections.from_ultralytics(results[0])

    # Filter detections by confidence
    detections = detections[detections.confidence > 0.3]

    # Update tracker with detections
    tracks = byte_track.update_with_detections(detections)

    # Annotate frame manually
    for track in tracks:
        track_id = track[0]
        bbox = track[1]  # Get bounding box coordinates

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

                    # Calculate the conversion factor only once
                    if pixel_to_meter is None:
                        # Estimate pixel speed in pixels/second
                        median_speed_pixels_per_sec = distance_pixels / (len(past_positions[track_id]) / fps)
                        # Calculate the pixel_to_meter conversion factor
                        pixel_to_meter = average_walking_speed_mps / median_speed_pixels_per_sec

                    # Convert pixel distance to meters
                    distance_meters = distance_pixels * pixel_to_meter

                    # Calculate speed in meters per second (m/s)
                    time_seconds = len(past_positions[track_id]) / fps
                    speed_mps = distance_meters / time_seconds

                    # Convert speed to km/h
                    speed_kmph = speed_mps * 3.6

                    # Categorize the speed
                    if speed_kmph > 10:  # Adjust these thresholds based on your data
                        speed_category = "High Speed"
                        color = (0, 0, 255)  # Red for high speed
                    elif 4 < speed_kmph <= 10:
                        speed_category = "Mid Speed"
                        color = (0, 255, 255)  # Yellow for mid speed
                    else:
                        speed_category = "Low Speed"
                        color = (0, 255, 0)  # Green for low speed

                    # Draw the speed category
                    cv2.putText(frame, f'{speed_category} ({int(speed_kmph)} km/h)', (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            else:
                past_positions[track_id].append((center_x, center_y))

            # Draw the track ID
            cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Write the annotated frame to the output video
    out.write(frame)

    # Display the frame (optional)
    cv2_imshow(frame)  # Use cv2_imshow instead of cv2.imshow
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# Save the results
print(f"Results saved to {TARGET_VIDEO_PATH}")