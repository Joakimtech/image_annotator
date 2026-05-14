
#  Image Annotator for Object Detection

A lightweight web tool built with Streamlit that lets you draw bounding boxes on images and export annotations in **YOLO** or **COCO JSON** format.

## Features
- Upload any image (JPG/PNG)
- Draw, delete, adjust bounding boxes via mouse
- Assign class labels from a custom list
- Export per‑image YOLO `.txt` or complete COCO JSON
- Real‑time annotation statistics

## Installation
\```bash
git clone https://github.com/joakimtech/image_annotator.git
cd image_annotator
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
\```

## Usage
[screenshots - coming soon]

## Project Structure
image_annotator/
├── app.py
├── requirements.txt       
├── README.md              
├── .gitignore             
├── utils/
│   ├── __init__.py
│   ├── coco_exporter.py
│   ├── yolo_exporter.py
│   └── canvas_helper.py
└── samples/               (empty folder for demo images)

## Future Extensions
- Support for polygons (segmentation)
- Automatic saving to cloud storage
- Multi‑image project management
