def extract_bboxes_from_canvas(canvas_json, class_name):
    """Parse canvas JSON and return list of bbox dicts"""
    bboxes = []
    if canvas_json is not None:
        objects = canvas_json["objects"]
        for obj in objects:
            if obj.get("type") == "rect":
                bboxes.append({
                    "left": obj["left"],
                    "top": obj["top"],
                    "width": obj["width"],
                    "height": obj["height"],
                    "class_name": class_name
                })
    return bboxes
