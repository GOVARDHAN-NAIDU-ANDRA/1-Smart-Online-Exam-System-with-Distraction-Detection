from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
import cv2
import threading
import time
from focus_detector import FocusDetector
import alerts

app = Flask(__name__)
camera = cv2.VideoCapture(0)
focus_detector = FocusDetector()

# Alert state
latest_alert = ""
alert_lock = threading.Lock()
browser_alarm_trigger = False


def generate_frames():
    global latest_alert, browser_alarm_trigger
    distraction_threshold = 2  # seconds
    last_focus_time = time.time()

    while True:
        success, frame = camera.read()
        if not success:
            break

        face_count, is_focused = focus_detector.detect_focus(frame)

        with alert_lock:
            if face_count == 0:
                latest_alert = "No Face Detected!"
                browser_alarm_trigger = True
            elif face_count > 1:
                latest_alert = "Multiple Faces Detected!"
                browser_alarm_trigger = True
            elif not is_focused:
                if time.time() - last_focus_time > distraction_threshold:
                    latest_alert = "Distracted!"
                    browser_alarm_trigger = True
            else:
                latest_alert = ""
                browser_alarm_trigger = False
                last_focus_time = time.time()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def login():
    return render_template("login.html")


@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_alert')
def get_alert():
    global latest_alert, browser_alarm_trigger
    with alert_lock:
        return jsonify({'alert': latest_alert, 'alarm': browser_alarm_trigger})


@app.route('/toggle_detection')
def toggle_detection():
    return jsonify({"status": "on"})


@app.route('/save_log')
def save_log():
    return "📝 Session saved (demo only)"


@app.route('/report')
def report():
    return "📊 Weekly Report (demo only)"


if __name__ == '__main__':
    app.run(debug=True)
