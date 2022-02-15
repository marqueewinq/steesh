from typing import List, Text

import fire
import jinja2
import openpyxl

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
    return list(map(lambda row: dict(zip(keys, [cell.value for cell in row])), ws))


def generate_card_html(
    data_dict: dict, template_file: str = "templates/test_card_template.html"
) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(**data_dict)


def generate_table_html(
    cards: List, template_file: str = "templates/table_template.html"
) -> Text:
    template = templateEnv.get_template(template_file)
    return template.render(cards)


def get_sliced_lst(lst: List) -> List:  # For 'generate_table_html' function
    sliced_lst = []
    i = -1
    for i in range(len(lst) // 3):
        print(lst[3 * i : 3 * i + 3])
        sliced_lst.append(lst[3 * i : 3 * i + 3])
    print(i)
    last = lst[3 * i + 3 :]
    if last != []:
        sliced_lst.append(last)
    return sliced_lst


# with open("my_new_file.html", "w") as fh: # output in future
card_lst = card_data_list()
print(card_lst)
# fh.write(generate_table_html(map(lambda i: card_lst[3*i,3*i+3], range(len(card_lst)//3 - 1))]))
