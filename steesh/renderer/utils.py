import csv
import os
import re
import typing as ty

import openpyxl
from jinja2 import Template


def read_template(template_path: str) -> Template:
    with open(template_path, "r") as f:
        template = Template(f.read())
    return template


def check_if_file(path: str) -> None:
    if not os.path.isfile(path):
        if os.path.isdir(path):
            raise IsADirectoryError(f'"{path}" is a directory, not file')
        raise FileNotFoundError(f'File "{path}" not found')


def std_cell_value(value: ty.Any) -> ty.Any:
    if isinstance(value, str):
        return value.rstrip(" ").replace("\n", "<br />")
    return value


def read_library(
    path: str,
    name_column: str = "Name",
    xlsx_sheet_index: int = 0,
) -> dict:
    list_of_cards_dicts = []
    check_if_file(path)
    if path.endswith(".xlsx"):
        rows = openpyxl.load_workbook(path).worksheets[xlsx_sheet_index].rows
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
                            std_cell_value(cell.value) if cell.value is not None else ""
                            for cell in row
                        ],
                    )
                ),
                rows,
            )
        )
        list_of_cards_dicts = list(
            filter(lambda dic: dic.get(name_column), list_of_cards_dicts)
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
                    zip(
                        keys,
                        [
                            std_cell_value(cell) if cell is not None else ""
                            for cell in row
                        ],
                    )
                ),
                rows,
            )
        )
    else:
        raise ValueError("Can't read from file of this format for now")

    if not keys or not list_of_cards_dicts:
        raise ValueError("Library is empty")
    # if None in keys or "" in keys:
    #     raise ValueError("Column name can't be empty")

    try:
        return dict(map(lambda dic: (dic[name_column], dic), list_of_cards_dicts))
    except KeyError:
        raise


def read_deck_from_str(deck: list[str], path: str = "") -> list:
    ret_lst = []
    for ind, line in enumerate(deck):
        mtch = re.search(r"(\d+)\s*(.+)$", line)
        if mtch:
            card_count, card_name = mtch.groups()
            ret_lst.append((int(card_count), card_name))
        else:
            raise ValueError(f"Line {ind}: couldn't parse: {line}")
    if not ret_lst:
        raise ValueError("Deck is empty")
    return ret_lst


def read_deck(path: str) -> list:
    check_if_file(path)
    with open(path, "r") as deck:
        return read_deck_from_str(deck.readlines(), path)


def render_template(template: Template, card_attributes: dict) -> str:
    rendered_html = template.render(**card_attributes)
    return rendered_html
