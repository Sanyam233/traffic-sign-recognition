import io
import json
from typing import Any, Dict

import numpy as np
from flask import jsonify
from PIL import Image

from constants import IMG_HEIGHT, IMG_WIDTH


def send_response(status: str, data : Dict[str, Any]) -> str:
    return jsonify({"status" : status, "rows" : [data]})

def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        data = json.load(f)
    return data


def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    image_arr = np.array(image) / 255
    image_arr = np.expand_dims(image_arr, axis=0)
    return image_arr
