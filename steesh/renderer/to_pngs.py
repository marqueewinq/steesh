import os
import shutil
import tempfile

import fire
import imgkit

from steesh.renderer.utils import (
    read_deck,
    read_library,
    read_template,
    render_template,
)


def generate_pngs(
    library_dict: dict, deck: list, template_path: str, output: str
) -> None:
    cards_jinja_dicts = []
    for card_count, card_name in deck:
        try:
            cards_jinja_dicts += [library_dict[card_name]] * int(card_count)
        except KeyError:
            raise ValueError(f'Card "{card_name}" is not in the library')
    template = read_template(template_path)
    cards_list = list(
        map(lambda card: render_template(template, card), cards_jinja_dicts)
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        for index, html in enumerate(cards_list):
            html_path = os.path.join(tmpdir, f"./{index:08d}.html")
            png_path = html_path.replace(".html", ".png")
            with open(html_path, "w") as fd:
                fd.write(html)
            imgkit.from_file(
                html_path,
                png_path,
                options={
                    "enable-local-file-access": "",
                    "allow": "/",
                    "crop-w": "256",
                },
            )
            basename = os.path.basename(png_path)
            shutil.move(png_path, os.path.join(output, basename))


def generate_pngs_from_file(
    library_path: str = "examples/dataframes/test_dataframe.csv",
    deck_path: str = "examples/decks/test_deck.txt",
    template_path: str = "examples/templates/test_card_template.html",
    output: str = "out",
    name_column: str = "Name",
    xlsx_sheet_index: int = 0,
) -> None:
    library_dict = read_library(
        library_path,
        name_column=name_column,
        xlsx_sheet_index=xlsx_sheet_index,
    )
    deck = read_deck(deck_path)
    os.makedirs(output, exist_ok=True)
    generate_pngs(library_dict, deck, template_path, output)


if __name__ == "__main__":
    fire.Fire(generate_pngs_from_file)
