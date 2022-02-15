from typing import List, Text

import fire
import jinja2
import openpyxl
import pdfkit

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)

cardlist, output = fire.Fire(
    lambda cardlist, output: (cardlist, output)
)  # Useless for now for easier work


def card_data_list(
    file: str = "dataframes/test_dataframe.xlsx",
) -> List:  # cardlist in future
    ws = openpyxl.load_workbook(file).worksheets[0].rows
    keys = [cell.value.replace(" ", "_") for cell in next(ws)]
    return list(
        map(
            lambda row: dict(
                zip(keys, [cell.value if cell.value != "-" else "" for cell in row])
            ),
            ws,
        )
    )


def generate_card_html(
    data_dict: dict, template_file: str = "templates/test_card_template.html"
) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(**data_dict)


def generate_table_html(
    cards: List, template_file: str = "templates/table_template.html"
) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(cards=cards)


def get_sliced_lst(lst: List) -> List:  # For 'generate_table_html' function
    sliced_lst = []
    i = -1
    for i in range(len(lst) // 3):
        sliced_lst.append(lst[3 * i : 3 * i + 3])
    last = lst[3 * i + 3 :]
    if last != []:
        sliced_lst.append(last)
    return sliced_lst


dtlst = card_data_list()
card_lst = list(map(generate_card_html, dtlst))
card_lst += [""] * ((9 - len(card_lst) % 9) % 9)
sliced_card_lst = get_sliced_lst(get_sliced_lst(card_lst))
i = 0

for card_page in sliced_card_lst:
    with open(f"{i}out.html", "w") as fh:
        fh.write(generate_table_html(card_page))
    i += 1
for j in range(i):
    pdfkit.from_file(str(j) + "out.html", str(j) + output)
