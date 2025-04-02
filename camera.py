from flask import Flask, Response
import cv2
import numpy
from pyzbar.pyzbar import decode

f = open("qrdata.txt", "w")
read = []
def scan_qr_codes(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        if data not in read:
            read.append(data)
            f.write(data + "\n")
            f.flush()

def process_frame(frame):
    scan_qr_codes(frame)
    return frame
    def display_scanned_data():
        if read:
            print("Scanned QR Codes:")
            for data in read:
                print(data)
app = Flask(__name__)
def draw_rectangle_around_qr(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        points = obj.polygon
        if len(points) == 4:  # Ensure it's a quadrilateral
            pts = numpy.array([[point.x, point.y] for point in points], numpy.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)

def process_frame(frame):
    draw_rectangle_around_qr(frame)
    scan_qr_codes(frame)
    return frame

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
