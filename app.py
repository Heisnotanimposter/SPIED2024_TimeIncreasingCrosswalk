from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np

app = Flask(__name__)

# Load your YOLOv8 model
model = YOLO('path_to_your_yolov8_model.pt')

@app.route('/detect', methods=['POST'])
def detect():
    # Get the image from the request
    file = request.files['image'].read()
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    # Run the model
    results = model(img)
    
    # Process results
    detections = []
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result
        detections.append({
            "x1": int(x1),
            "y1": int(y1),
            "x2": int(x2),
            "y2": int(y2),
            "confidence": float(conf),
            "class": int(cls)
        })
    
    return jsonify(detections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
