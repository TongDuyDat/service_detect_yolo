import os
from pathlib import Path
import cv2
from io import BytesIO
from flask import Flask, jsonify, logging, request, send_from_directory
from flask_cors import CORS
from PIL import Image
from config import config
from database.files import File
from database.image_db import BBox, Images
from detector import detect, load_model
from database import *
# create app backend
app = Flask(__name__)
CORS(app)
model = load_model()
config()


@app.route("/")
def hello():
    return "Hello World!"


@app.route('/detect_objects', methods=['GET'])
def detect_objects():
    file_id = request.args['file_id']
    if file_id:
        try:
            file = File.get_file(file_id)
            if file == None:
                return jsonify({"status": "warning", "message": "File id does not exist"}), 400

            file = str(file.path)
            filename = os.path.basename(file)
            save_path = Path(os.path.join(os.getenv('save_path'), filename))
            image = cv2.imread(file)
            w, h, _ = image.shape
            # Perform object detection (this is a placeholder, replace with your actual detection code)
            detection_results = detect(image, model, save_path)
            status = File.update_file(file_id, save_path)

            if status == None:
                return jsonify({"status": "warning", "message": "File suploaded error"}), 400
            # bboxes = []
            # for result_dict in detection_results:
            #     bbox_from_dict = BBox(
            #                 box=result_dict["box"],
            #                 conf=result_dict["conf"],
            #                 class_id=result_dict["class_id"],
            #                 class_name=result_dict["class_name"])
            #     bboxes.append(bbox_from_dict)

            # Images.add_image(path_image=str(save_path), width = w, height = h, bbox_list = bboxes)
            return jsonify({"dectect_path": save_path})
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return f"Error processing image: {e}", 500
    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
