#!/usr/bin/env python

""" Utility to create a printer ready images of cards for the game Fluxx. """

import csv
import shutil
import textwrap
from pathlib import Path
from typing import List, Union

from PIL import Image, ImageDraw, ImageFont

from lib.cli import run as typer_run
from lib.pil import get_image, resize
from lib.string_util import safe_filename


def csv_reader(path: Path, dialect: csv.Dialect = csv.excel, **kwargs) -> List[str]:
    """ Generator that yields a row from a csv file as a list of strings """

    for row in csv.reader(open(path), dialect=dialect, **kwargs):
        yield [str(cell).strip() for cell in row]


def clear_directory(dir_path: Union[str, Path]) -> Path:
    """ If dir_path exists, delete it.  Then create it """

    dir_path = Path(dir_path)
    if dir_path.exists():
        shutil.rmtree(dir_path)
    dir_path.mkdir()
    return dir_path


def save_raster(deck_dir: Path, rows: int = 3, cols: int = 3) -> None:
    """ Write Fluxx cards onto letter size pages containing rows x cols cards """

    images = list(deck_dir.iterdir())

    image = Image.open(images[0])
    image_width, image_height = image.size
    v_dpi, h_dpi = image.info["dpi"]
    assert v_dpi == h_dpi
    dpi = v_dpi

    page_w = int(8.5 * dpi)
    page_h = int(11.0 * dpi)
    h_space = (page_w - cols * image_width) // (cols + 1)
    v_space = (page_h - rows * image_height) // (rows + 1)

    index = 0
    white = 255, 255, 255

    page_num = 0
    while index < len(images):
        page_num += 1
        page = Image.new("RGB", (page_w, page_h), white)

        y = v_space
        for _ in range(rows):
            x = h_space
            for _ in range(cols):
                if index >= len(images):
                    continue
                image = Image.open(images[index])
                print(images[index], image.size)
                index += 1
                page.paste(image, (x, y))
                x += h_space + image_width
            y += v_space + image_height

        page.save(f"page_{page_num:02d}.png", dpi=(dpi, dpi))


def main(input_dir: Path, template_name: str = "deck.csv") -> None:
    """
    Generate a Fluxx deck from rsrc fonts and images
    and template csv file and images included in input_dir
    """

    rsrc_dir = Path("rsrc")
    title_font = ImageFont.truetype(str(rsrc_dir / "trebucscbd.ttf"), 26)
    font = ImageFont.truetype(str(rsrc_dir / "trebucsc.ttf"), 16)

    templates = {
        "meta_rule": (170, 250),
        "new_rule": (270, 330),
        "creeper": (240, 300),
        "keeper": (240, 300),
        "goal": (230, 300),
        "action": (230, 290),
        "surprise": (230, 290),
    }

    deck_dir = clear_directory("deck")

    deck_csv = input_dir / template_name
    reader = csv_reader(deck_csv)
    for columns in reader:
        type_, name, description = columns[:3]
        safe_name = safe_filename(name)
        if type_ not in templates:
            continue

        # Read the template image
        src = rsrc_dir / f"{type_}.png"
        image = Image.open(src)
        draw = ImageDraw.Draw(image)

        # Get the vertical position of the title and description
        title_v, desc_v = templates[type_]

        # Write the title
        title = textwrap.wrap(name, width=20)
        draw.text(
            (90, title_v - (len(title) - 1) * 35),
            "\n".join(title),
            font=title_font,
            fill="#000",  # black
        )

        if type_ == "goal":
            # Combine Keeper images for Goal card
            icons = [
                get_image(input_dir, safe_filename(keeper))
                for keeper in description.split("\\n")
            ]
            assert icons and all(icons) and len(icons) in (2, 3)
            if len(icons) == 2:
                image.paste(resize(icons[0], 100, 100), (90, desc_v))
                image.paste(resize(icons[1], 100, 100), (100 + 90, 100 + desc_v))
            elif len(icons) == 3:
                image.paste(resize(icons[0], 100, 100), (90, desc_v))
                image.paste(resize(icons[1], 100, 100), (100 + 90, desc_v))
                image.paste(resize(icons[2], 100, 100), (50 + 90, 100 + desc_v))

        else:
            # Write the description
            desc_lines = []
            for desc_line in description.split("\\n"):
                desc_lines += textwrap.wrap(desc_line, width=35)
            draw.text((90, desc_v), "\n".join(desc_lines), font=font, fill="#000")

            # Copy the provided icon
            icon = get_image(input_dir, safe_name)
            if icon:
                image.paste(resize(icon, 200, 200), (90, desc_v))

        # Save the card
        dst = deck_dir / f"{safe_name}.png"
        image.save(dst, dpi=(150, 150))

    save_raster(deck_dir)


if __name__ == "__main__":
    typer_run(main)
