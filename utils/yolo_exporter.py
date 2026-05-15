def export_yolo(bboxes, image_width, image_height, class_map, output_path):
    """
    Export annotations to YOLO format.
    
    Args:
        bboxes: list of dicts with keys 'class', 'left', 'top', 'width', 'height'
        image_width, image_height: dimensions of the image
        class_map: dict mapping class name to integer id
        output_path: path to save .txt file
    """
    with open(output_path, 'w') as f:
        for box in bboxes:
            class_id = class_map[box['class']]
            # Convert to YOLO normalized coordinates (center x, center y, width, height)
            x_center = (box['left'] + box['width'] / 2) / image_width
            y_center = (box['top'] + box['height'] / 2) / image_height
            width_norm = box['width'] / image_width
            height_norm = box['height'] / image_height
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}\n")
            
