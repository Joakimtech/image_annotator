import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import json
import os
from utils.canvas_helper import extract_bboxes_from_canvas
from utils.yolo_exporter import export_yolo
from utils.coco_exporter import export_coco

st.set_page_config(page_title="Image Annotator", layout="wide")
st.title(" Interactive Image Annotation Tool")

# Initialize session state
if "all_annotations" not in st.session_state:
    st.session_state.all_annotations = {}  # {image_filename: [bboxes]}

# Sidebar
st.sidebar.header("Settings")
class_names = st.sidebar.text_input("Class names (comma separated)", "cat,dog,bird")
class_list = [c.strip() for c in class_names.split(",")]
current_class = st.sidebar.selectbox("Assign class to NEW boxes", class_list)

uploaded_file = st.sidebar.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Load image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    # Retrieve existing annotations for this image (if any)
    filename = uploaded_file.name
    if filename not in st.session_state.all_annotations:
        st.session_state.all_annotations[filename] = []

    # Canvas
    canvas_result = st_canvas(
        fill_color="rgba(255,165,0,0.3)",
        stroke_width=2,
        stroke_color="#00FF00",
        background_image=Image.fromarray(image),
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="rect",
        key=f"canvas_{filename}",
    )

    # When a new rectangle is drawn, add it to session state 
    if canvas_result.json_data:
        new_bboxes = extract_bboxes_from_canvas(canvas_result.json_data, current_class)
        # To avoid duplicates, we replace all boxes (since canvas_result gives complete list)
        # Better: we store the full list from canvas as the source of truth.
        st.session_state.all_annotations[filename] = new_bboxes

    # Display current boxes
    current_boxes = st.session_state.all_annotations[filename]
    st.write(f"**Total boxes for this image:** {len(current_boxes)}")
    for i, box in enumerate(current_boxes):
        st.write(f"{i+1}. {box['class_name']} → (x:{box['left']:.0f}, y:{box['top']:.0f}, w:{box['width']:.0f}, h:{box['height']:.0f})")

    # Export section
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export as YOLO .txt"):
            os.makedirs("exports", exist_ok=True)
            txt_path = f"exports/{filename.rsplit('.',1)[0]}.txt"
            class_map = {name: i for i, name in enumerate(class_list)}
            export_yolo(current_boxes, w, h, class_map, txt_path)
            st.success(f"Saved to {txt_path}")

    with col2:
        if st.button("Export as COCO JSON"):
            os.makedirs("exports", exist_ok=True)
            json_path = f"exports/{filename.rsplit('.',1)[0]}_coco.json"
            export_coco(current_boxes, filename, w, h, class_list, json_path)
            st.success(f"Saved to {json_path}")

    # Statistics
    st.sidebar.subheader("Statistics")
    if current_boxes:
        class_counts = {}
        for box in current_boxes:
            cls = box['class_name']
            class_counts[cls] = class_counts.get(cls, 0) + 1
        st.sidebar.write(class_counts)
    else:
        st.sidebar.write("No annotations yet")
