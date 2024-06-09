from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import cv2
import torch
import numpy as np

app = Flask(__name__)
CORS(app)

model = torch.hub.load("ultralytics/yolov5", "custom", path="./best.pt")

model.eval()
model.conf = 0.35
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


def process_image(image):
    global greyscale, edge, sharpening, bilateral, negative, brightness, contrast

    result = np.array(image)
    if greyscale:
        result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
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

    return result


def detect_objects(image):
    results = model(image, size=640)
    img = np.squeeze(results.render())
    img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img_BGR


@app.route("/detect_objects", methods=["GET","POST"])
def detect_objects_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Convert image to numpy array
    img_array = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Process image
    processed_image = process_image(image)

    # Detect objects
    detected_image = detect_objects(processed_image)

    # Encode image to send as response
    _, buffer = cv2.imencode('.jpg', detected_image)
    response_image = buffer.tobytes()

    return Response(response_image, mimetype="image/jpeg")


if __name__ == "__main__":
    app.run(debug=True)

    
    
    # https://chatgpt.com/c/83990222-0f8c-4113-8457-3bb7bc4eb3c9
