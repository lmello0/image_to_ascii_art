import base64
from random import randint
from time import sleep
from typing import Dict, List
import sys
from io import BytesIO
from bitmap_utils import get_chars_grayness, extract_font_bitmap, get_chars_joined_by_white_pixels
from image_utils import get_image_data_array, open_image_grayscale


def find_best_ascii_value(bitmap_chars: Dict[float, List[str]], value: float):
    closest_key = min(bitmap_chars, key=lambda x: abs(x - value))
    possible_values = bitmap_chars[closest_key]

    return possible_values[randint(0, len(possible_values) - 1)]


if __name__ == '__main__':
    image_path = sys.argv[1]

    # getting bitmap
    font = BytesIO(base64.b64decode(open('resources/DONT_DELETE').read()))

    bitmap_chars = get_chars_joined_by_white_pixels(
        get_chars_grayness(extract_font_bitmap(font)))

    # opening image
    image = get_image_data_array(open_image_grayscale(image_path))

    for row in image:
        for pixel in row:
            value = find_best_ascii_value(bitmap_chars, pixel)
            print(value, end='')

        sleep(0.02)
        print()
