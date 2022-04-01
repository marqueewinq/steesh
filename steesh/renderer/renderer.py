import csv
import os
import re
import tempfile
from typing import Dict, List, Text

import fire
import jinja2
import openpyxl
import pdfkit
from PyPDF2 import PdfFileMerger

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)


def check_if_file(path: str) -> None:
    if not os.path.isfile(path):
        if os.path.isdir(path):
            raise IsADirectoryError(f'"{path}" is a directory, not file')
        raise FileNotFoundError(f'File "{path}" not found')


def read_library(path: str) -> Dict:
    list_of_cards_dicts = []
    check_if_file(path)
    if path.endswith(".xlsx"):
        rows = openpyxl.load_workbook(path).worksheets[0].rows
        keys = [
            cell.value.replace(" ", "_") if cell.value else cell.value
            for cell in next(rows)
        ]
        list_of_cards_dicts = list(
            map(
                lambda row: dict(
                    zip(
                        keys,
                        [
                            cell.value
                            if (cell.value != "-" or cell.value is None)
                            else ""
                            for cell in row
                        ],
                    )
                ),
                rows,
            )
        )
        list_of_cards_dicts = list(
            filter(lambda dic: dic.get("Name"), list_of_cards_dicts)
        )
    elif path.endswith(".csv"):
        rows = csv.reader(open(path))
        try:
            keys = [cell.replace(" ", "_") for cell in next(rows)]
        except StopIteration:
            raise ValueError("Library is empty")
        list_of_cards_dicts = list(
            map(
                lambda row: dict(
                    zip(keys, [cell if cell != "-" else "" for cell in row])
                ),
                rows,
            )
        )
    else:
        raise ValueError("Can't read from file of this format for now")

    if not keys or not list_of_cards_dicts:
        raise ValueError("Library is empty")
    if None in keys or "" in keys:
        raise ValueError("Column name can't be empty")
    dd = dict(map(lambda dic: (dic["Name"], dic), list_of_cards_dicts))

    return dd


def read_deck_from_str(deck: List[str], path: str = "") -> List:
    ret_lst = []
    for ind, line in enumerate(deck):

        mtch = re.search(r"(\d+) (.*)$", line)
        if mtch:
            ret_lst.append(mtch.groups())

        else:
            raise ValueError(f'Wrong input format in file "{path}" in line {ind}')
    if not ret_lst:
        raise ValueError("Deck is empty")
    return ret_lst


def read_deck(path: str) -> List:
    check_if_file(path)
    with open(path, "r") as deck:
        return read_deck_from_str(deck.readlines(), path)


def render_card_html(library_dict: dict, template_file: str) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(**library_dict)


def render_table_html(
    cards_table: List, template_file: str = "steesh/templates/table_template.html"
) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(cards=cards_table)


def get_sliced_lst(lst: List) -> List[List]:
    sliced_lst = []
    i = -1
    for i in range(len(lst) // 3):
        sliced_lst.append(lst[3 * i : 3 * i + 3])
    last = lst[3 * i + 3 :]
    if last != []:
        sliced_lst.append(last)
    return sliced_lst


def generate_tables_of_cards(
    library_dict: dict, deck: List, template_path: Text
) -> List[List]:
    cards_jinja_dicts = []
    for card in deck:
        try:
            cards_jinja_dicts += [library_dict[card[1]]] * int(card[0])
        except KeyError:
            raise ValueError(f'Card "{card}" is not in the library')
    cards_list = list(
        map(lambda card: render_card_html(card, template_path), cards_jinja_dicts)
    )
    cards_list += [""] * ((9 - len(cards_list) % 9) % 9)
    cards_table = get_sliced_lst(get_sliced_lst(cards_list))
    return cards_table


def api_render_html(
    library_path: str,
    deck: List[str],
    template_path: str = "examples/templates/test_card_template.html",
) -> Text:
    return (
        "<ul>\n<li>"
        + "</li>\n<li>".join(
            list(
                map(
                    render_table_html,
                    generate_tables_of_cards(
                        read_library(library_path),
                        read_deck_from_str(deck),
                        template_path,
                    ),
                )
            )
        )
        + "</li>\n</ul>"
    )


def render_pdf_from_html_tables(html_tables_list: List, output: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        pdfs = []
        for ind, table in enumerate(html_tables_list):
            pdfkit.from_string(
                table,
                os.path.join(td, f"{ind}out.pdf"),
                options={
                    "--margin-bottom": "0mm",
                    "--margin-left": "0mm",
                    "--margin-right": "0mm",
                    "--margin-top": "0mm",
                },
            )
            pdfs.append(os.path.join(td, f"{ind}out.pdf"))

        merger = PdfFileMerger()

        for pdf in pdfs:
            merger.append(pdf)

        merger.write(output)
        merger.close()


def render_page_cli(
    library_path: str = "examples/dataframes/test_dataframe.csv",
    deck_path: str = "examples/decks/test_deck.txt",
    template_path: str = "examples/templates/test_card_template.html",
    output: str = "out.pdf",
) -> None:
    library_dict = read_library(library_path)
    deck = read_deck(deck_path)
    render_pdf_from_inputs(library_dict, deck, template_path, output)


def render_pdf_from_inputs(
    library_dict: dict, deck: List, template_path: str, output: str
) -> None:
    render_pdf_from_html_tables(
        list(
            map(
                render_table_html,
                generate_tables_of_cards(library_dict, deck, template_path),
            )
        ),
        output,
    )


if __name__ == "__main__":
    fire.Fire(render_page_cli)
