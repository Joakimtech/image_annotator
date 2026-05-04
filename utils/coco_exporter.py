import json
from datetime import datetime

def export_coco(bboxes, image_path, image_width, image_height, class_list, output_json_path):
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": [{"id": i, "name": name} for i, name in enumerate(class_list)]
    }
    
    image_id = 1
    annotation_id = 1
    
    # Add image info
    coco_format["images"].append({
        "id": image_id,
        "file_name": image_path,
        "width": image_width,
        "height": image_height
    })
    
    # Add each bounding box as an annotation
    for box in bboxes:
        # COCO bbox format: [x, y, width, height]
        x, y, w, h = box['left'], box['top'], box['width'], box['height']
        area = w * h
        category_id = class_list.index(box['class_name'])  # 0-indexed
        coco_format["annotations"].append({
            "id": annotation_id,
            "image_id": image_id,
            "bbox": [x, y, w, h],
            "area": area,
            "category_id": category_id,
            "iscrowd": 0
        })
        annotation_id += 1
    
    with open(output_json_path, 'w') as f:
        json.dump(coco_format, f, indent=2)
