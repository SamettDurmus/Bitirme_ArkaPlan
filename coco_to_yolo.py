import os
import json
from tqdm import tqdm
import shutil


def make_folders(path="output"):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    return path


def convert_bbox_coco2yolo(img_width, img_height, bbox):
    x_tl, y_tl, w, h = bbox
    dw = 1.0 / img_width
    dh = 1.0 / img_height
    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0
    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh
    return [x, y, w, h]


def convert_coco_json_to_yolo_txt(output_path, json_file):
    path = make_folders(output_path)
    with open(json_file) as f:
        json_data = json.load(f)
    # write _darknet.labels, which holds names of all classes (one class per line)
    label_file = os.path.join(output_path, "_darknet.labels")
    with open(label_file, "w") as f:
        for category in tqdm(json_data["categories"], desc="Categories"):
            category_name = category["name"]
            f.write(f"{category_name}\n")
    for image in tqdm(json_data["images"], desc="Annotation txt for each iamge"):
        img_id = image["id"]
        img_name = image["file_name"]
        img_width = image["width"]
        img_height = image["height"]
        anno_in_image = [
            anno for anno in json_data["annotations"] if anno["image_id"] == img_id]
        anno_txt = os.path.join(output_path, img_name.split(".")[0] + ".txt")
        with open(anno_txt, "w") as f:
            for anno in anno_in_image:
                category = anno["category_id"]
                bbox_COCO = anno["bbox"]
                x, y, w, h = convert_bbox_coco2yolo(
                    img_width, img_height, bbox_COCO)
                f.write(f"{category} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
    print("Converting COCO Json to YOLO txt finished!")
