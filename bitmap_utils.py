from io import BytesIO
from typing import Dict, List, Tuple
from PIL import ImageFont, ImageDraw, Image
import string


def get_ascii_alphabet() -> List[int]:
    alphabet = [ord(char) for char in string.printable]
    alphabet.sort()

    return alphabet[5:]


def create_bitmap_from_font(font: ImageFont.FreeTypeFont, character: str) -> Image.Image:
    img = Image.new("1", (16, 16), color=0)

    draw = ImageDraw.Draw(img)

    draw.text((0, 0), character, font=font, fill=1)

    return img


def extract_font_bitmap(font_path: BytesIO) -> List[Tuple[str, Image.Image]]:
    font_size = 8
    font = ImageFont.truetype(font_path, font_size)

    characters = [chr(i) for i in get_ascii_alphabet()]

    return [(char, create_bitmap_from_font(font, char)) for char in characters]


def count_white_pixel_from_image(img: Image.Image) -> int:
    white_pixel_count = 0
    for pixel in img.getdata():
        if pixel == 1:
            white_pixel_count += 1

    return white_pixel_count


def get_whitest_pixel_char(bitmap_chars: List[Tuple[str, int]]) -> Tuple[str, int]:
    whitest_pixels_char = bitmap_chars[0]
    for char in bitmap_chars:
        if (char[1] >= whitest_pixels_char[1]):
            whitest_pixels_char = char

    return whitest_pixels_char


def get_chars_grayness(bitmap_chars: List[Tuple[str, Image.Image]]) -> List[Tuple[str, float]]:
    chars = [(char, count_white_pixel_from_image(bitmap_char)) for char, bitmap_char in bitmap_chars]

    maximum_white_value = get_whitest_pixel_char(chars)[1]

    chars = [(char, value/maximum_white_value) for char, value in chars]

    chars.sort(key=lambda char: char[1])

    return chars


def get_chars_joined_by_white_pixels(bitmap_chars: List[Tuple[str, float]]) -> Dict[float, List[str]]:
    chars = {}
    for char, white_pixels in bitmap_chars:
        if (chars.get(white_pixels) == None):
            chars[white_pixels] = [char]
            continue

        chars[white_pixels].append(char)

    return chars
