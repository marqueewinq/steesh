import os
import tempfile

import fire
from jinja2 import Template
from PyPDF2 import PdfFileMerger
from weasyprint import HTML

from steesh.renderer.utils import (
    read_deck,
    read_library,
    read_template,
    render_template,
)

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_TABLE_PATH = os.path.join(BASE_DIR, "templates/table_template.html")


def convert_html_to_pdf(html_str: str, output_path: str) -> None:
    html_obj = HTML(string=html_str)
    html_obj.write_pdf(output_path)


def generate_pdf(
    library: dict,
    deck: list,
    card_template: Template,
    page_template: Template,
    output_path: str,
) -> None:
    card_htmls = []
    for count, card_name in deck:
        card_attributes = library[card_name]
        for _ in range(count):
            card_html = render_template(card_template, card_attributes)
            card_htmls.append(card_html)

    pages = []
    for i in range(0, len(card_htmls), 9):
        cards_3x3 = [card_htmls[i + j : i + j + 3] for j in range(0, 9, 3)]
        page_html = render_template(page_template, {"cards": cards_3x3})
        pages.append(page_html)

    with tempfile.TemporaryDirectory() as td:
        pdfs = []
        for ind, table in enumerate(pages):
            open(os.path.join(td, f"{ind}out.pdf"), "wb").write(
                HTML(string=table).write_pdf()
            )
            pdfs.append(os.path.join(td, f"{ind}out.pdf"))
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append(pdf, import_bookmarks=False)
        merger.write(output_path)
        merger.close()


def generate_pdf_from_file(
    library_path: str = "examples/dataframes/test_dataframe.csv",
    deck_path: str = "examples/decks/test_deck.txt",
    template_path: str = "examples/templates/test_card_template.html",
    output_path: str = "out.pdf",
    name_column: str = "Name",
    xlsx_sheet_index: int = 0,
) -> None:
    library = read_library(
        library_path,
        name_column=name_column,
        xlsx_sheet_index=xlsx_sheet_index,
    )
    deck = read_deck(deck_path)
    template = read_template(template_path)
    page_template = read_template(TEMPLATE_TABLE_PATH)
    generate_pdf(
        library=library,
        deck=deck,
        card_template=template,
        page_template=page_template,
        output_path=output_path,
    )


if __name__ == "__main__":
    fire.Fire(generate_pdf_from_file)
