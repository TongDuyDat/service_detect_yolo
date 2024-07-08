from flask import Flask, jsonify, logging, request, send_from_directory
from flask_cors import CORS
from PIL import Image
from database.image_db import BBox, Images
from detector import detect, load_model
from database import *
# create app backend
app = Flask(__name__)
CORS(app)
model = load_model()

@app.route("/")
def hello():
    return "Hello World!"


@app.route('/detect_objects', methods=['POST'])
def detect_objects():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        if file:
            try:
                # Read the image file
                image = Image.open(file.stream)
                w, h = image.size
                # Perform object detection (this is a placeholder, replace with your actual detection code)
                detection_results = detect(image, model)
                bboxes = []
                for result_dict in detection_results:
                    bbox_from_dict = BBox(
                                box=result_dict["box"],
                                conf=result_dict["conf"],
                                class_id=result_dict["class_id"],
                                class_name=result_dict["class_name"])
                    bboxes.append(bbox_from_dict)
                Images.add_image(path_image="", width = w, height = h, bbox_list = bboxes)
                return jsonify(detection_results)
            except Exception as e:
                logging.error(f"Error processing image: {e}")
                return f"Error processing image: {e}", 500
    return "Invalid request method", 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
