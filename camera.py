from flask import Flask, Response
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)
f = open("qrdata.txt", "w")

scanned_data = set()

def scan_qr_codes(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        if data not in scanned_data:
            scanned_data.add(data)
            print(f"Scanned QR Code: {data}")
            f.write(data + "\n")
            f.flush()

def draw_rectangle_around_qr(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        points = obj.polygon
        if len(points) == 4:
            pts = np.array([[point.x, point.y] for point in points], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
    return frame

def process_frame(frame):
    scan_qr_codes(frame)
    frame = draw_rectangle_around_qr(frame)
    return frame

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = process_frame(frame)  # Apply QR detection before streaming

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
