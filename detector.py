import cv2
from ultralytics import YOLO


def load_model():
    """Load a model from a file."""
    model = YOLO("weights/yolov8s-oiv7.onnx")
    return model

def detect(frame, model):
    result = model(frame)[0]
    bboxes = []
    boxes = result.boxes.xyxy.int().tolist()  # Boxes object for bounding box outputs
    clss = result.boxes.cls.int().tolist()
    scores = result.boxes.conf.float().tolist()
    cls_names = [str(model.names[cls_id]) for cls_id in clss]
    for xyxy, conf, cls_id, cls_name in zip(boxes, scores, clss, cls_names):
        result_dict = {
            "box": xyxy,
            "conf": round(conf, 2),
            "class_id": cls_id,
            "class_name": cls_name
        }
        bboxes.append(result_dict)
    return bboxes