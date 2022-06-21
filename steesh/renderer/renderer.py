import csv
import os
import re
import string
import tempfile
from typing import Callable, List, Tuple

import fire
import openpyxl
import weasyprint
from jinja2 import Template
from PyPDF2 import PdfFileMerger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_TABLE_PATH = os.path.join(BASE_DIR, "templates/table_template.html")


def get_template(template_path: str) -> Template:
    with open(template_path, "r") as f:
        template = Template(f.read())
    return template


def check_if_file(path: str) -> None:
    if not os.path.isfile(path):
        if os.path.isdir(path):
            raise IsADirectoryError(f'"{path}" is a directory, not file')
        raise FileNotFoundError(f'File "{path}" not found')


def read_library(path: str) -> dict:
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


def read_deck_from_str(deck: list[str], path: str = "") -> list:
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


def read_deck(path: str) -> list:
    check_if_file(path)
    with open(path, "r") as deck:
        return read_deck_from_str(deck.readlines(), path)


def getApproximateArialStringWidth(st: str) -> float:
    size = 0  # in milinches
    for s in st:
        if s in "lij|' ":
            size += 37
        elif s in "![]fI.,:;/\\t":
            size += 50
        elif s in '`-(){}r"':
            size += 60
        elif s in "*^zcsJkvxy":
            size += 85
        elif s in "aebdhnopqug#$L+<>=?_~FZT" + string.digits:
            size += 95
        elif s in "BSPEAKVXY&UwNRCHD":
            size += 112
        elif s in "QGOMm%W@":
            size += 135
        else:
            size += 50
    return size * 25.4 / 1000.0


def setup_dynamic_fontsize(library_dict: dict) -> None:
    needs_dynamic_fonts: List[Tuple[str, Callable, int, int]] = [
        ("name_font_size", (lambda Name, **kwargs: Name), 42, 9),
        ("module_font_size", (lambda Module, **kwargs: Module), 27, 9),
        (
            "n_v_font_size",
            (lambda ID, Version_Tag, **kwargs: f"N{ID}V{Version_Tag}"),
            15,
            9,
        ),
        ("power_font_size", (lambda Power, **kwargs: Power), 11, 11),
        ("type_font_size", (lambda Type, **kwargs: Type), 49, 11),
        ("text_font_size", (lambda Text, **kwargs: Text), 60, 37),
    ]

    for name, f, width, height in needs_dynamic_fonts:
        lens = list(map(getApproximateArialStringWidth, f(**library_dict).split("\n")))
        max_len = max(lens)
        sum_len = sum(lens) / 2
        try:
            # library_dict[name]=f'{min((width/(0.29*(max_len))), 11)}mm'
            c = 0
            k = min(
                -c / 2 + (width * height / sum_len + c * c / 4) ** (1 / 2)
                if name == "text_font_size"
                else (width / (0.29 * (max_len))),
                9,
            )
            library_dict[name] = f"{k}mm"
        except ZeroDivisionError:
            library_dict[name] = "9mm"


def render_card_html(library_dict: dict, template_file: str) -> str:
    setup_dynamic_fontsize(library_dict)
    template = get_template(template_file)
    return template.render(**library_dict)


def render_table_html(
    cards_table: list, template_file: str = TEMPLATE_TABLE_PATH
) -> str:
    template = get_template(template_file)
    return template.render(cards=cards_table)


def get_sliced_lst(lst: list) -> list[list]:
    sliced_lst = []
    i = -1
    for i in range(len(lst) // 3):
        sliced_lst.append(lst[3 * i : 3 * i + 3])
    last = lst[3 * i + 3 :]
    if last != []:
        sliced_lst.append(last)
    return sliced_lst


def generate_tables_of_cards(
    library_dict: dict, deck: list, template_path: str
) -> list[list]:
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


def render_pdf_from_html_tables(html_tables_list: list, output: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        pdfs = []
        for ind, table in enumerate(html_tables_list):
            open(os.path.join(td, f"{ind}out.pdf"), "wb").write(
                weasyprint.HTML(string=table).write_pdf()
            )
            pdfs.append(os.path.join(td, f"{ind}out.pdf"))
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf, import_bookmarks=False)
        merger.write(output)
        merger.close()


def render_page_cli(
    library_path: str = "examples/dataframes/test_dataframe.csv",
    deck_path: str = "examples/decks/test_deck.txt",
    template_path: str = "examples/templates/test_card_template_dynamic_fontsize.html",
    output: str = "out.pdf",
) -> None:
    library_dict = read_library(library_path)
    deck = read_deck(deck_path)
    render_pdf_from_inputs(library_dict, deck, template_path, output)


def render_pdf_from_inputs(
    library_dict: dict, deck: list, template_path: str, output: str
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
