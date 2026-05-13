import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Image Annotator", layout="wide")
st.title("sak Interactive Image Annotation Tool (Test)")

# Sidebar: file uploader
st.sidebar.header("Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert uploaded file to RGB image (OpenCV format)
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    # Create drawing canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # semi-transparent orange
        stroke_width=2,
        stroke_color="#00FF00",               # green outline
        background_image=Image.fromarray(image),
        update_streamlit=True,
        height=h,
        width=w,
        drawing_mode="rect",                  # draw rectangles
        key="test_canvas",
    )

    # If user drew boxes, show their coordinates
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        st.write(f"**Number of rectangles drawn:** {len(objects)}")
        for i, obj in enumerate(objects):
            if obj["type"] == "rect":
                left = obj["left"]
                top = obj["top"]
                width = obj["width"]
                height = obj["height"]
                st.write(f"Box {i+1}: x={left:.0f}, y={top:.0f}, w={width:.0f}, h={height:.0f}")
else:
    st.info(" Upload an image from the sidebar to start drawing bounding boxes.")
