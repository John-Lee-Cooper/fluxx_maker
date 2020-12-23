#!/usr/bin/env python

""" TODO """

from pathlib import Path
from typing import Optional

from PIL import Image
from PIL.Image import Image as PIL_Image


def get_image(image_dir: Path, image_stem: str) -> Optional[PIL_Image]:
    """ Read image file from image_dir into a PIL image and return it """

    filename = next(image_dir.glob(f"{image_stem}.*"), None)
    if filename:
        return Image.open(filename)
    return None


def resize(image: PIL_Image, height: int, width: int) -> PIL_Image:
    """ Resize image to no larger than height x width keeping aspect ratio """

    image_height, image_width = image.size
    scale = min(height / image_height, width / image_width)
    return image.resize((int(image_height * scale), int(image_width * scale)))

