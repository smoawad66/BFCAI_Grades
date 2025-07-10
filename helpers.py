import os
import requests
from io import BytesIO
from PIL import Image

gpa_scale = {
    "A+": {"points": 4.0, "score": 90},
    "A": {"points": 3.7, "score": 85},
    "B+": {"points": 3.3, "score": 80},
    "B": {"points": 3.0, "score": 75},
    "C+": {"points": 2.7, "score": 70},
    "C": {"points": 2.4, "score": 65},
    "D+": {"points": 2.2, "score": 60},
    "D": {"points": 2.0, "score": 50},
    "F": {"points": 0.0, "score": 49}
}

def get_grade(score):
    if score >= 90:return 'A+'
    if score >= 85:return 'A'
    if score >= 80:return 'B+'
    if score >= 75:return 'B'
    if score >= 70:return 'C+'
    if score >= 65:return 'C'
    if score >= 60:return 'D+'
    if score >= 50:return 'D'
    return 'F'

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)

def get_image(img_src):
    img_src = img_src.replace("//", "/").replace("http:/", "http://")
    try:
        response = requests.get(img_src)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            return image
    except Exception:
        return ""