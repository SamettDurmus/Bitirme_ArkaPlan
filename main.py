from flask import Flask, render_template, request, Response
import cv2
import torch
from io import BytesIO
from PIL import Image
import numpy as np

# WSGI Application
app = Flask(__name__)
camera = cv2.VideoCapture(0)

model = torch.hub.load("ultralytics/yolov5", "custom", path="./best.pt")

model.eval()
model.conf = 0.25
model.iou = 0.45

greyscale = False
sharpening = False
edge = False
bilateral = False
negative = False

brightness = 0.0
contrast = 1.0

filters_list = []


def set_filter_status(filters_list):
    global greyscale, edge, sharpening, bilateral, negative

    edge = "edge" in filters_list
    greyscale = "greyscale" in filters_list
    sharpening = "super" in filters_list
    bilateral = "bilateral" in filters_list
    negative = "negative" in filters_list


def generate_frames():
    global greyscale, edge, sharpening, bilateral, negative, brightness, contrast, sharpening

    while camera.isOpened():
        # read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            result = frame.copy()

            if greyscale:
                result = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            else:
                if edge:
                    result = cv2.Canny(result, 100, 50)

                if bilateral:
                    result = cv2.bilateralFilter(result, 9, 75, 75)

                if negative:
                    result = cv2.bitwise_not(result)

                if sharpening:
                    result = cv2.filter2D(
                        result, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))

            result = cv2.convertScaleAbs(
                result, alpha=contrast, beta=brightness)

            ret, buffer = cv2.imencode('.jpg', result)
            result = buffer.tobytes()

            img = Image.open(BytesIO(result))
            results = model(img, size=640)
            img = np.squeeze(results.render())
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            result = cv2.imencode('.jpg', img_BGR)[1].tobytes()

        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + result + b"\r\n")


def generate_frames_original():
    while True:
        # read the camera frame
        success, frame = camera.read()
        frame = cv2.flip(frame, 1)
        # xray camerası kullanırken gerekli olur mu bilmiyorum ama sanırım değil
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/", methods=["GET", "POST"])
def index():
    global filters_list, brightness, contrast

    if request.method == "POST":
        filters_list = request.form.getlist("filters")
        set_filter_status(filters_list)

        brightness = float(request.form.get("brightness")) if request.form.get(
            "brightness") is not None else 0.0
        contrast = float(request.form.get("contrast")) if request.form.get(
            "contrast") is not None else 1.0

    return render_template("main.html", edge=edge)


@app.route("/edited_video")
def edited_video():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/video")
def video():
    return Response(generate_frames_original(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
