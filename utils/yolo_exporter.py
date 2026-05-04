def export_yolo(bboxes, image_width, image_height, class_map, output_txt_path):
    """
    bboxes: list of dicts with keys 'left', 'top', 'width', 'height', 'class_name'
    class_map: dict mapping class_name -> class_id (int)
    """
    with open(output_txt_path, 'w') as f:
        for box in bboxes:
            x_center = (box['left'] + box['width']/2) / image_width
            y_center = (box['top'] + box['height']/2) / image_height
            width_norm = box['width'] / image_width
            height_norm = box['height'] / image_height
            class_id = class_map[box['class_name']]
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}\n")
