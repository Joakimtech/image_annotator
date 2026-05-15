import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import json
import os
from utils.yolo_exporter import export_yolo
from utils.coco_exporter import export_coco

st.set_page_config(page_title="Image Annotator", layout="wide")
st.title(" Interactive Image Annotation Tool")

# Session state
if "annotations" not in st.session_state:
    st.session_state.annotations = {}
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Sidebar
st.sidebar.header(" Settings")
class_names = st.sidebar.text_input("Class names (comma separated)", "cat,dog,bird")
class_list = [c.strip() for c in class_names.split(",")]
selected_class = st.sidebar.selectbox("Assign class to NEW boxes", class_list)

uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    filename = uploaded_file.name
    st.session_state.current_image = filename

    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    if filename not in st.session_state.annotations:
        st.session_state.annotations[filename] = []

    # Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#00FF00",
        background_image=Image.fromarray(image),
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="rect",
        key=f"canvas_{filename}",
    )

    # Process rectangles
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        new_bboxes = []
        for obj in objects:
            if obj.get("type") == "rect":
                new_bboxes.append({
                    "class": selected_class,
                    "left": obj["left"],
                    "top": obj["top"],
                    "width": obj["width"],
                    "height": obj["height"]
                })
        st.session_state.annotations[filename] = new_bboxes

    # Display annotations
    st.subheader(" Current Annotations")
    current_boxes = st.session_state.annotations.get(filename, [])
    if current_boxes:
        for i, box in enumerate(current_boxes):
            st.write(f"{i+1}. **{box['class']}** → x:{box['left']:.0f}, y:{box['top']:.0f}, w:{box['width']:.0f}, h:{box['height']:.0f}")
    else:
        st.write("No annotations yet. Draw rectangles on the image.")

    # Statistics sidebar
    st.sidebar.subheader(" Annotation Statistics")
    if current_boxes:
        class_counts = {}
        for box in current_boxes:
            cls = box['class']
            class_counts[cls] = class_counts.get(cls, 0) + 1
        for cls, count in class_counts.items():
            st.sidebar.write(f"**{cls}:** {count} box(es)")
        st.sidebar.write(f"**Total boxes:** {len(current_boxes)}")
    else:
        st.sidebar.write("No annotations yet")

    # Save/Load
    if st.sidebar.button(" Save all annotations"):
        os.makedirs("exports", exist_ok=True)
        with open("exports/annotations_backup.json", "w") as f:
            json.dump(st.session_state.annotations, f, indent=2)
        st.sidebar.success("Saved to exports/annotations_backup.json")

    if st.sidebar.button(" Load saved annotations"):
        if os.path.exists("exports/annotations_backup.json"):
            with open("exports/annotations_backup.json", "r") as f:
                st.session_state.annotations = json.load(f)
            st.sidebar.success("Annotations loaded")
            st.rerun()

    # Export buttons
    st.subheader(" Export Annotations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export as YOLO .txt"):
            os.makedirs("exports", exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            yolo_path = os.path.join("exports", f"{base_name}.txt")
            class_map = {name: i for i, name in enumerate(class_list)}
            export_yolo(current_boxes, w, h, class_map, yolo_path)
            st.success(f"✅ YOLO saved to {yolo_path}")

    with col2:
        if st.button("Export as COCO JSON"):
            os.makedirs("exports", exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            coco_path = os.path.join("exports", f"{base_name}_coco.json")
            export_coco(current_boxes, filename, w, h, class_list, coco_path)
            st.success(f"✅ COCO JSON saved to {coco_path}")

else:
    st.info(" Upload an image to start annotating")
