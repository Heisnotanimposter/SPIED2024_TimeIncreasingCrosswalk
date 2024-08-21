import cv2
import numpy as np
import requests
from ultralytics import YOLO

# ESP32 URL
URL = "http://<IP address>"
AWB = True

# Load your YOLO model (make sure you have `yolov8s.pt` or any other model variant in the same directory)
model = YOLO("yolov8s.pt")  # Update with the path to your YOLO model if necessary

# Start video capture from the ESP32 CAM
cap = cv2.VideoCapture(URL + ":81/stream")

def set_resolution(url: str, index: int = 1, verbose: bool = False):
    try:
        if verbose:
            resolutions = ("10: UXGA(1600x1200)\n9: SXGA(1280x1024)\n8: XGA(1024x768)\n7: SVGA(800x600)\n"
                           "6: VGA(640x480)\n5: CIF(400x296)\n4: QVGA(320x240)\n3: HQVGA(240x176)\n0: QQVGA(160x120)")
            print(f"Available resolutions\n{resolutions}")

        if index in [10, 9, 8, 7, 6, 5, 4, 3, 0]:
            requests.get(url + f"/control?var=framesize&val={index}")
        else:
            print("Wrong index")
    except Exception as e:
        print(f"SET_RESOLUTION: something went wrong - {e}")

def set_quality(url: str, value: int = 1):
    try:
        if 10 <= value <= 63:
            requests.get(url + f"/control?var=quality&val={value}")
    except Exception as e:
        print(f"SET_QUALITY: something went wrong - {e}")

def set_awb(url: str, awb: int = 1):
    try:
        awb = not awb
        requests.get(url + f"/control?var=awb&val={1 if awb else 0}")
    except Exception as e:
        print(f"SET_AWB: something went wrong - {e}")
    return awb

def set_person_detect(url: str, person_detect: int = 1):
    try:
        requests.get(url + f"/control?var=person_detect&val={1 if person_detect else 0}")
    except Exception as e:
        print(f"SET_PERSON_DETECT: something went wrong - {e}")
    return person_detect

if __name__ == '__main__':
    set_resolution(URL, index=8)
    set_person_detect(URL, 1)

    while True:
        if cap.isOpened():
            ret, frame = cap.read()

            if ret:
                # Run YOLO object detection
                results = model(frame)

                # Get detections for persons
                for result in results:
                    for box in result.boxes:
                        if box.cls == 0:  # Class 0 is 'person' in COCO dataset
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 4)
                            cv2.putText(frame, f'Person {box.conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

            cv2.imshow("frame", frame)

            key = cv2.waitKey(1)

            if key == ord('r'):
                idx = int(input("Select resolution index: "))
                set_resolution(URL, index=idx, verbose=True)

            elif key == ord('q'):
                val = int(input("Set quality (10 - 63): "))
                set_quality(URL, value=val)

            elif key == ord('a'):
                AWB = set_awb(URL, AWB)

            elif key == 27:  # ESC key
                break

    cv2.destroyAllWindows()
    cap.release()
