import os
import re

import pytest

playwright = pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright


def render_response(library_path, deck):
    pass


def format_deck(deck: str) -> list[str]:
    deck = deck.replace("\r\n", "\n")  # replace win linens
    lines = deck.split("\n")
    retval: list[str] = []
    regex = re.compile(r"\d+ .*")
    for line in lines:
        line = line.strip()
        if not regex.match(line):
            continue
        retval.append(line)
    return retval


def get_content(library_path, deck):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000/")
        page.fill("#deck", deck)
        with page.expect_file_chooser() as fc_info:
            page.click("[type=file]")
            file_chooser = fc_info.value
            file_chooser.set_files(library_path)
        # page.on(
        #     "response",
        #     lambda response: response.status == 200
        #     or pytest.fail(f"response status is: {response.status}"),
        # )
        page.locator("button").click()
        return page.content()


@pytest.mark.integration
def test_happy():
    library_path = os.path.join(
        os.path.abspath(os.getcwd()), "unit_test/dataframes/happy/df_1.xlsx"
    )
    deck = open("unit_test/decks/happy/deck_1.txt", "r").read()[:-1]
    expected = render_response(library_path, format_deck(deck))  # noqa: F841
    actual = get_content(library_path, deck)  # noqa: F841
    # assert expected == actual


@pytest.mark.integration
def test_error_flash():
    library_path = os.path.join(
        os.path.abspath(os.getcwd()), "unit_test/dataframes/happy/df_1.xlsx"
    )
    deck = open("unit_test/decks/happy/deck_1.txt", "r").read()
    expected = render_response(library_path, format_deck(deck))  # noqa: F841
    actual = get_content(library_path, deck)  # noqa: F841
    # assert expected == actual
