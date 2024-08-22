from flask import Flask, render_template, Response, jsonify
import cv2
import time

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve video feed
def generate_frames():
    cap = cv2.VideoCapture(0)  # Use the laptop's webcam
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# API endpoint to get the current traffic light state and timer
@app.route('/traffic_light_state')
def traffic_light_state():
    # Logic to get the current state and timer
    state = 'green'  # or 'red'
    timer = 10  # seconds remaining
    return jsonify({'state': state, 'timer': timer})

if __name__ == "__main__":
    app.run(debug=True)