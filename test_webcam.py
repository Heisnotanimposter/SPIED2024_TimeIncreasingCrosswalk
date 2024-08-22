{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "colab_type": "text",
    "id": "view-in-github"
   },
   "source": [
    "<a href=\"https://colab.research.google.com/github/Heisnotanimposter/ObjectDetection_with_Server/blob/main/PersonSpeedvision.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "3B2zj9HkxNgz",
    "outputId": "54a0ac60-8411-4c49-859f-3bdc5d517b86"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mounted at /content/drive\n"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "WgJklsACD0f3",
    "outputId": "f0b1185b-501e-44bd-f9a4-5deb95f20388"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Wed Aug 21 14:26:37 2024       \n",
      "+---------------------------------------------------------------------------------------+\n",
      "| NVIDIA-SMI 535.104.05             Driver Version: 535.104.05   CUDA Version: 12.2     |\n",
      "|-----------------------------------------+----------------------+----------------------+\n",
      "| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |\n",
      "| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |\n",
      "|                                         |                      |               MIG M. |\n",
      "|=========================================+======================+======================|\n",
      "|   0  Tesla T4                       Off | 00000000:00:04.0 Off |                    0 |\n",
      "| N/A   53C    P8               9W /  70W |      0MiB / 15360MiB |      0%      Default |\n",
      "|                                         |                      |                  N/A |\n",
      "+-----------------------------------------+----------------------+----------------------+\n",
      "                                                                                         \n",
      "+---------------------------------------------------------------------------------------+\n",
      "| Processes:                                                                            |\n",
      "|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |\n",
      "|        ID   ID                                                             Usage      |\n",
      "|=======================================================================================|\n",
      "|  No running processes found                                                           |\n",
      "+---------------------------------------------------------------------------------------+\n"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "VCZ_qDnLD87m",
    "outputId": "7639f847-86a5-48c2-b543-ec921bfe2c3d"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m41.3/41.3 kB\u001b[0m \u001b[31m2.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m135.7/135.7 kB\u001b[0m \u001b[31m7.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m869.1/869.1 kB\u001b[0m \u001b[31m34.7 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[?25hCollecting roboflow\n",
      "  Downloading roboflow-1.1.40-py3-none-any.whl.metadata (9.4 kB)\n",
      "Requirement already satisfied: certifi in /usr/local/lib/python3.10/dist-packages (from roboflow) (2024.7.4)\n",
      "Requirement already satisfied: idna==3.7 in /usr/local/lib/python3.10/dist-packages (from roboflow) (3.7)\n",
      "Requirement already satisfied: cycler in /usr/local/lib/python3.10/dist-packages (from roboflow) (0.12.1)\n",
      "Requirement already satisfied: kiwisolver>=1.3.1 in /usr/local/lib/python3.10/dist-packages (from roboflow) (1.4.5)\n",
      "Requirement already satisfied: matplotlib in /usr/local/lib/python3.10/dist-packages (from roboflow) (3.7.1)\n",
      "Requirement already satisfied: numpy>=1.18.5 in /usr/local/lib/python3.10/dist-packages (from roboflow) (1.26.4)\n",
      "Requirement already satisfied: opencv-python-headless==4.10.0.84 in /usr/local/lib/python3.10/dist-packages (from roboflow) (4.10.0.84)\n",
      "Requirement already satisfied: Pillow>=7.1.2 in /usr/local/lib/python3.10/dist-packages (from roboflow) (9.4.0)\n",
      "Requirement already satisfied: python-dateutil in /usr/local/lib/python3.10/dist-packages (from roboflow) (2.8.2)\n",
      "Collecting python-dotenv (from roboflow)\n",
      "  Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)\n",
      "Requirement already satisfied: requests in /usr/local/lib/python3.10/dist-packages (from roboflow) (2.32.3)\n",
      "Requirement already satisfied: six in /usr/local/lib/python3.10/dist-packages (from roboflow) (1.16.0)\n",
      "Requirement already satisfied: urllib3>=1.26.6 in /usr/local/lib/python3.10/dist-packages (from roboflow) (2.0.7)\n",
      "Requirement already satisfied: tqdm>=4.41.0 in /usr/local/lib/python3.10/dist-packages (from roboflow) (4.66.5)\n",
      "Requirement already satisfied: PyYAML>=5.3.1 in /usr/local/lib/python3.10/dist-packages (from roboflow) (6.0.2)\n",
      "Collecting requests-toolbelt (from roboflow)\n",
      "  Downloading requests_toolbelt-1.0.0-py2.py3-none-any.whl.metadata (14 kB)\n",
      "Collecting filetype (from roboflow)\n",
      "  Downloading filetype-1.2.0-py2.py3-none-any.whl.metadata (6.5 kB)\n",
      "Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->roboflow) (1.2.1)\n",
      "Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->roboflow) (4.53.1)\n",
      "Requirement already satisfied: packaging>=20.0 in /usr/local/lib/python3.10/dist-packages (from matplotlib->roboflow) (24.1)\n",
      "Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.10/dist-packages (from matplotlib->roboflow) (3.1.2)\n",
      "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.10/dist-packages (from requests->roboflow) (3.3.2)\n",
      "Downloading roboflow-1.1.40-py3-none-any.whl (79 kB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m79.1/79.1 kB\u001b[0m \u001b[31m4.9 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[?25hDownloading filetype-1.2.0-py2.py3-none-any.whl (19 kB)\n",
      "Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)\n",
      "Downloading requests_toolbelt-1.0.0-py2.py3-none-any.whl (54 kB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m54.5/54.5 kB\u001b[0m \u001b[31m4.5 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
      "\u001b[?25hInstalling collected packages: filetype, python-dotenv, requests-toolbelt, roboflow\n",
      "Successfully installed filetype-1.2.0 python-dotenv-1.0.1 requests-toolbelt-1.0.0 roboflow-1.1.40\n"
     ]
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 500
    },
    "id": "uMd_s5DE23cx",
    "outputId": "f022ffdd-429d-4239-f922-7162a24e992e"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "0: 384x640 1 person, 329.7ms\n",
      "Speed: 2.9ms preprocess, 329.7ms inference, 9.4ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 448.1ms\n",
      "Speed: 1.6ms preprocess, 448.1ms inference, 1.7ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 322.2ms\n",
      "Speed: 1.4ms preprocess, 322.2ms inference, 0.8ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 376.0ms\n",
      "Speed: 1.5ms preprocess, 376.0ms inference, 0.8ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 339.4ms\n",
      "Speed: 2.8ms preprocess, 339.4ms inference, 1.5ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 307.2ms\n",
      "Speed: 1.5ms preprocess, 307.2ms inference, 0.8ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 354.5ms\n",
      "Speed: 1.7ms preprocess, 354.5ms inference, 1.2ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 305.1ms\n",
      "Speed: 1.3ms preprocess, 305.1ms inference, 1.3ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 443.2ms\n",
      "Speed: 1.5ms preprocess, 443.2ms inference, 2.1ms postprocess per image at shape (1, 3, 384, 640)\n",
      "\n",
      "0: 384x640 1 person, 410.7ms\n",
      "Speed: 1.6ms preprocess, 410.7ms inference, 1.1ms postprocess per image at shape (1, 3, 384, 640)\n"
     ]
    },
    {
     "ename": "KeyboardInterrupt",
     "evalue": "",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m                         Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[5], line 41\u001b[0m\n\u001b[1;32m     39\u001b[0m \u001b[38;5;66;03m# Process the webcam feed in real-time\u001b[39;00m\n\u001b[1;32m     40\u001b[0m \u001b[38;5;28;01mwhile\u001b[39;00m cap\u001b[38;5;241m.\u001b[39misOpened():\n\u001b[0;32m---> 41\u001b[0m     ret, frame \u001b[38;5;241m=\u001b[39m \u001b[43mcap\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m     42\u001b[0m     \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m ret:\n\u001b[1;32m     43\u001b[0m         \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mError: Could not read frame from webcam.\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n",
      "\u001b[0;31mKeyboardInterrupt\u001b[0m: "
     ]
    }
   ],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "from ultralytics import YOLO\n",
    "import supervision as sv\n",
    "from collections import defaultdict, deque\n",
    "\n",
    "# Load the YOLO model\n",
    "model = YOLO(\"yolov8s.pt\")  # Use the appropriate YOLOv8 model variant\n",
    "\n",
    "# Initialize video capture with the laptop's webcam\n",
    "cap = cv2.VideoCapture(1)  # 0 is the default webcam. Use 1, 2, etc. if you have multiple cameras.\n",
    "\n",
    "# Check if the webcam is opened correctly\n",
    "if not cap.isOpened():\n",
    "    print(\"Error: Could not open webcam.\")\n",
    "    exit()\n",
    "\n",
    "# Video properties\n",
    "width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))\n",
    "height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))\n",
    "fps = cap.get(cv2.CAP_PROP_FPS)\n",
    "\n",
    "# Initialize ByteTrack tracker\n",
    "byte_track = sv.ByteTrack(\n",
    "    track_activation_threshold=0.3,\n",
    "    lost_track_buffer=30,\n",
    "    frame_rate=fps\n",
    ")\n",
    "\n",
    "# Initialize data structures to store past positions for speed estimation\n",
    "past_positions = defaultdict(lambda: deque(maxlen=5))\n",
    "\n",
    "# Placeholder for the conversion factor\n",
    "pixel_to_meter = None\n",
    "\n",
    "# Known average walking speed (6 km/h in meters per second)\n",
    "average_walking_speed_mps = 6 * 1000 / 3600  # 6 km/h = 1.67 meters/second\n",
    "\n",
    "# Process the webcam feed in real-time\n",
    "while cap.isOpened():\n",
    "    ret, frame = cap.read()\n",
    "    if not ret:\n",
    "        print(\"Error: Could not read frame from webcam.\")\n",
    "        break\n",
    "\n",
    "    # Run YOLO object detection\n",
    "    results = model(frame, conf=0.5)  # Adjust confidence threshold as needed\n",
    "\n",
    "    # Get detections\n",
    "    detections = sv.Detections.from_ultralytics(results[0])\n",
    "\n",
    "    # Filter detections by confidence\n",
    "    detections = detections[detections.confidence > 0.3]\n",
    "\n",
    "    # Update tracker with detections\n",
    "    tracks = byte_track.update_with_detections(detections)\n",
    "\n",
    "    # Annotate frame manually\n",
    "    for track in tracks:\n",
    "        track_id = track[0]\n",
    "        bbox = track[1]  # Get bounding box coordinates\n",
    "\n",
    "        if bbox is not None:\n",
    "            # Draw the bounding box\n",
    "            x1, y1, x2, y2 = map(int, bbox)\n",
    "            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)\n",
    "\n",
    "            # Calculate speed estimation\n",
    "            center_x = (x1 + x2) // 2\n",
    "            center_y = (y1 + y2) // 2\n",
    "\n",
    "            if track_id in past_positions:\n",
    "                past_positions[track_id].append((center_x, center_y))\n",
    "                if len(past_positions[track_id]) > 1:\n",
    "                    # Calculate the displacement between the first and last positions\n",
    "                    x_start, y_start = past_positions[track_id][0]\n",
    "                    x_end, y_end = past_positions[track_id][-1]\n",
    "                    distance_pixels = np.sqrt((x_end - x_start) ** 2 + (y_end - y_start) ** 2)\n",
    "\n",
    "                    # Calculate the conversion factor only once\n",
    "                    if pixel_to_meter is None:\n",
    "                        # Estimate pixel speed in pixels/second\n",
    "                        median_speed_pixels_per_sec = distance_pixels / (len(past_positions[track_id]) / fps)\n",
    "                        # Calculate the pixel_to_meter conversion factor\n",
    "                        pixel_to_meter = average_walking_speed_mps / median_speed_pixels_per_sec\n",
    "\n",
    "                    # Convert pixel distance to meters\n",
    "                    distance_meters = distance_pixels * pixel_to_meter\n",
    "\n",
    "                    # Calculate speed in meters per second (m/s)\n",
    "                    time_seconds = len(past_positions[track_id]) / fps\n",
    "                    speed_mps = distance_meters / time_seconds\n",
    "\n",
    "                    # Convert speed to km/h\n",
    "                    speed_kmph = speed_mps * 3.6\n",
    "\n",
    "                    # Categorize the speed\n",
    "                    if speed_kmph > 10:  # Adjust these thresholds based on your data\n",
    "                        speed_category = \"High Speed\"\n",
    "                        color = (0, 0, 255)  # Red for high speed\n",
    "                    elif 4 < speed_kmph <= 10:\n",
    "                        speed_category = \"Mid Speed\"\n",
    "                        color = (0, 255, 255)  # Yellow for mid speed\n",
    "                    else:\n",
    "                        speed_category = \"Low Speed\"\n",
    "                        color = (0, 255, 0)  # Green for low speed\n",
    "\n",
    "                    # Draw the speed category\n",
    "                    cv2.putText(frame, f'{speed_category} ({int(speed_kmph)} km/h)', (x1, y1 - 10),\n",
    "                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)\n",
    "            else:\n",
    "                past_positions[track_id].append((center_x, center_y))\n",
    "\n",
    "            # Draw the track ID\n",
    "            cv2.putText(frame, f'ID: {track_id}', (x1, y1 - 30),\n",
    "                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)\n",
    "\n",
    "    # Display the frame\n",
    "    cv2.imshow('YOLO Real-Time Detection', frame)\n",
    "    if cv2.waitKey(1) & 0xFF == ord('q'):\n",
    "        break\n",
    "\n",
    "# Release resources\n",
    "cap.release()\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "4hSKNwre2m_2"
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "gpuType": "T4",
   "include_colab_link": true,
   "machine_shape": "hm",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
