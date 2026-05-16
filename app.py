import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
from PIL import Image
import json
import os
from utils.yolo_exporter import export_yolo
from utils.coco_exporter import export_coco

st.set_page_config(page_title="Image Annotation Tool", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def get_css(theme):
    if theme == "dark":
        return """
        <style>
        .stApp { background-color: #0E1117 !important; }
        section[data-testid="stSidebar"] { background-color: #1E1E2E !important; }
        .annotation-card {
            background-color: #2A2A3A !important;
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            border-left: 4px solid #4CAF50;
            font-family: monospace;
            color: #FAFAFA !important;
        }
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px;
            width: 100%;
        }
        .stButton button:hover { background-color: #45a049 !important; }
        .stats-box {
            background: #2A2A3A !important;
            border-radius: 10px;
            padding: 12px;
            margin-top: 15px;
            color: #FAFAFA !important;
        }
        .canvas-container { border: 1px solid #3A3A4A; border-radius: 12px; padding: 6px; background: #1E1E2E; }
        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """
    else:
        return """
        <style>
        .stApp { background-color: #F5F5F7 !important; }
        section[data-testid="stSidebar"] { background-color: #F0F0F0 !important; }
        .annotation-card {
            background-color: #FFFFFF !important;
            border-radius: 8px;
            padding: 10px;
            margin: 8px 0;
            border-left: 4px solid #4CAF50;
            font-family: monospace;
            color: #1E1E2E !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .stButton button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 8px;
            width: 100%;
        }
        .stButton button:hover { background-color: #45a049 !important; }
        .stats-box {
            background: #FFFFFF !important;
            border-radius: 10px;
            padding: 12px;
            margin-top: 15px;
            color: #1E1E2E !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .canvas-container { border: 1px solid #DDD; border-radius: 12px; padding: 6px; background: #FFFFFF; }
        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """

st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# Brand header
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
    <div style="font-size: 2.5rem;">🖍️</div>
    <div>
        <h1 style="margin: 0;">Image Annotation Tool</h1>
        <p style="margin: 0; color: #888;">Draw bounding boxes · Assign classes · Export YOLO/COCO</p>
    </div>
</div>
""", unsafe_allow_html=True)

if "annotations" not in st.session_state:
    st.session_state.annotations = {}
if "current_image" not in st.session_state:
    st.session_state.current_image = None

st.sidebar.header("⚙️ Settings")

# Theme toggle button
if st.sidebar.button(f"🎨 Switch to {'Light' if st.session_state.theme == 'dark' else 'Dark'} Theme", use_container_width=True):
    toggle_theme()
    st.rerun()  # Force a clean rerun

# Debug indicator
st.sidebar.write(f"**Current theme:** {st.session_state.theme}")

class_names = st.sidebar.text_input("Class names (comma separated)", "cat,dog,bird")
class_list = [c.strip() for c in class_names.split(",")]
selected_class = st.sidebar.selectbox("Assign class to NEW boxes", class_list)
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    filename = uploaded_file.name
    st.session_state.current_image = filename
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]

    if filename not in st.session_state.annotations:
        st.session_state.annotations[filename] = []

    st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

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

    current_boxes = st.session_state.annotations.get(filename, [])

    st.subheader("📝 Current Annotations")
    if current_boxes:
        for i, box in enumerate(current_boxes):
            st.markdown(f"""
            <div class="annotation-card">
                <span style="font-weight: bold;">{box['class']}</span>
                <span style="float: right; color: #aaa;">#{i+1}</span><br>
                <span style="font-size: 0.8rem;">x: {box['left']:.0f}, y: {box['top']:.0f}, w: {box['width']:.0f}, h: {box['height']:.0f}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No annotations yet.")

    # Statistics
    st.sidebar.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.sidebar.markdown("#### 📊 Statistics")
    if current_boxes:
        class_counts = {}
        for box in current_boxes:
            cls = box['class']
            class_counts[cls] = class_counts.get(cls, 0) + 1
        for cls, count in class_counts.items():
            st.sidebar.markdown(f"**{cls}:** {count} box(es)")
        st.sidebar.markdown(f"**Total boxes:** {len(current_boxes)}")
    else:
        st.sidebar.markdown("*No annotations yet*")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    if st.sidebar.button("💾 Save all annotations", use_container_width=True):
        os.makedirs("exports", exist_ok=True)
        with open("exports/annotations_backup.json", "w") as f:
            json.dump(st.session_state.annotations, f, indent=2)
        st.sidebar.success("Saved to exports/annotations_backup.json")

    if st.sidebar.button("📂 Load saved annotations", use_container_width=True):
        if os.path.exists("exports/annotations_backup.json"):
            with open("exports/annotations_backup.json", "r") as f:
                st.session_state.annotations = json.load(f)
            st.sidebar.success("Annotations loaded")
            st.rerun()

    st.subheader("📤 Export Annotations")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Export as YOLO .txt", use_container_width=True):
            os.makedirs("exports", exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            yolo_path = os.path.join("exports", f"{base_name}.txt")
            class_map = {name: i for i, name in enumerate(class_list)}
            export_yolo(current_boxes, w, h, class_map, yolo_path)
            st.success(f"✅ YOLO saved to `{yolo_path}`")
    with col2:
        if st.button("📦 Export as COCO JSON", use_container_width=True):
            os.makedirs("exports", exist_ok=True)
            base_name = os.path.splitext(filename)[0]
            coco_path = os.path.join("exports", f"{base_name}_coco.json")
            export_coco(current_boxes, filename, w, h, class_list, coco_path)
            st.success(f"✅ COCO JSON saved to `{coco_path}`")
else:
    st.info("👈 Upload an image from the sidebar to start annotating")
