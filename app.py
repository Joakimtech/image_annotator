import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import json
import os

st.set_page_config(page_title="Image Annotator", layout="wide")
st.title("Interactive Image Annotation Tool")

# Sidebar controls
st.sidebar.header("Annotation Settings")
class_names = st.sidebar.text_input("Class names (comma separated)", "cat,dog,bird")
class_list = [c.strip() for c in class_names.split(",")]
selected_class = st.sidebar.selectbox("Select class", class_list)

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    # Create canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#00FF00",
        background_image=Image.fromarray(image),
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="rect",
        key="canvas",
    )

    # Display bounding box coordinates if any
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            st.write(f"**Detected boxes:** {len(objects)}")
            for i, obj in enumerate(objects):
                left = obj["left"]
                top = obj["top"]
                width = obj["width"]
                height = obj["height"]
                st.write(f"Box {i+1}: (x={left:.0f}, y={top:.0f}, w={width:.0f}, h={height:.0f}) class: {selected_class}")
else:
    st.info("Upload an image from the sidebar to start annotating")
