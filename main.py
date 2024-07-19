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
from utils import *
# create app backend
app = Flask(__name__)
CORS(app)
model = load_model()
config()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/v1/api/detection", methods=["GET"])
def detect_objects():
    file_id = request.args.get("file_id")
    
    if file_id:
        try:
            file = File.get_file(file_id)
            if file == None:
                return (
                    jsonify({"status": "warning", "message": "File id does not exist"}),
                    400,
                )
            folder = str(file.folder)
            name = str(file.name)
            filename = f'{folder}/{name}'
            img_path = Path(os.path.join(os.getenv("save_path"), filename))
            image = cv2.imread(img_path)
            w, h, _ = image.shape
            # Perform object detection (this is a placeholder, replace with your actual detection code)
            
            filename = filename.lower()
            save_ext = file_extension(filename)
            save_image = filename.replace(save_ext, f"_detection{save_ext}")
            save_path = Path(os.path.join(os.getenv("save_path"), save_image)).as_posix()
            detection_results = detect(image, model, save_path)
            status = File.update_file(file_id, save_path)

            if status == None:
                return (
                    jsonify({"status": "warning", "message": "File suploaded error"}),
                    400,
                )
            # bboxes = []
            # for result_dict in detection_results:
            #     bbox_from_dict = BBox(
            #                 box=result_dict["box"],
            #                 conf=result_dict["conf"],
            #                 class_id=result_dict["class_id"],
            #                 class_name=result_dict["class_name"])
            #     bboxes.append(bbox_from_dict)

            return jsonify({"data": status.to_json()})
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return f"Error processing image: {e}", 500
    return {}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
