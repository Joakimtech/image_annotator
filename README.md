
#  Image Annotator for Object Detection

A lightweight web tool built with Streamlit that lets you draw bounding boxes on images and export annotations in **YOLO** or **COCO JSON** format.

## Features
- Upload images (JPG/PNG)
- Draw/adjust bounding boxes with mouse
- Custom class labels
- Export to YOLO .txt and COCO JSON
- Annotation statistics and save/load

## Installation
\```bash
- git clone https://github.com/joakimtech/image_annotator.git
- cd image_annotator
- python -m venv venv
- source venv/bin/activate  # or venv\Scripts\activate on Windows
- pip install -r requirements.txt
- streamlit run app.py
\```

## Usage
[screenshots - coming soon]
<img width="1920" height="838" alt="image" src="https://github.com/user-attachments/assets/7104b1ce-2357-419b-9f0a-4352f7685430" />

### 6. Final test

Run `streamlit run app.py` and verify:
- Drawing and class assignment
- Statistics update
- Save/load annotations
- Export buttons create files



## Future Extensions
- Support for polygons (segmentation)
- Automatic saving to cloud storage
- Multi‑image project management
## Visual example of tool in use
<img width="1917" height="880" alt="image" src="https://github.com/user-attachments/assets/249fd592-79da-450b-86b4-6267d5dd08eb" />

##  Support the Project

If you find this tool useful, consider a small donation by clicking the button below to support future development.
**[![Sponsor](https://img.shields.io/badge/Sponsor-PayPal-00457C?style=for-the-badge&logo=paypal)](https://www.paypal.com/donate?business=kiugijoakim%40gmail.com&no_recurring=0&currency_code=USD)**
