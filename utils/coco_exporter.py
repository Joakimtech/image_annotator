import json

def export_coco(bboxes, image_filename, image_width, image_height, class_list, output_path):
    """
    Export annotations to COCO JSON format.
    
    Args:
        bboxes: list of dicts with keys 'class', 'left', 'top', 'width', 'height'
        image_filename: name of the image file
        image_width, image_height: dimensions
        class_list: list of class names (index = class id)
        output_path: path to save .json file
    """
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": [{"id": i, "name": name} for i, name in enumerate(class_list)]
    }
    
    # Image entry
    image_id = 1
    coco_data["images"].append({
        "id": image_id,
        "file_name": image_filename,
        "width": image_width,
        "height": image_height
    })
    
    # Annotation entries
    ann_id = 1
    for box in bboxes:
        category_id = class_list.index(box['class'])
        # COCO bbox format: [x, y, width, height]
        bbox = [box['left'], box['top'], box['width'], box['height']]
        area = box['width'] * box['height']
        coco_data["annotations"].append({
            "id": ann_id,
            "image_id": image_id,
            "category_id": category_id,
            "bbox": bbox,
            "area": area,
            "iscrowd": 0
        })
        ann_id += 1
    
    with open(output_path, 'w') as f:
        json.dump(coco_data, f, indent=2)
