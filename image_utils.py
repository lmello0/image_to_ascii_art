import math
from PIL import Image
import numpy as np

def open_image_grayscale(image_path: str) -> Image.Image:
    image = Image.open(image_path)

    expected_max_height = 120

    if image.height != expected_max_height:
        percent = math.floor((expected_max_height / image.height) * 100)
        image = resize_image_percent(image, percent)

    return image.convert('L')

def resize_image_percent(image: Image.Image, percent: float) -> Image.Image:
    if percent < 0 and percent > 100:
        raise ValueError('Values must be betwenn 0 and 100')

    percent = percent / 100

    width, height = image.size

    new_width = math.ceil(width * percent)
    new_height = math.ceil(height * percent)

    return image.resize((new_width, new_height))

def get_image_data_array(image: Image.Image) -> np.ndarray:
    return np.array(image) / 255.0