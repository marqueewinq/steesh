import os

import pytest

playwright = pytest.importorskip("playwright")
from playwright.sync_api import sync_playwright

from unit_test.static_text import deck_contains_empty_lines_response, happy_response


def get_content(deck, library_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000/")
        page.fill("#deck", deck)
        with page.expect_file_chooser() as fc_info:
            page.click("[type=file]")
            file_chooser = fc_info.value
            file_chooser.set_files(library_path)
        page.locator("button").click()
        return page.content()


@pytest.mark.integration
def test_happy():
    assert (
        get_content(
            open("unit_test/decks/happy/deck_1.txt", "r").read()[:-1],
            os.path.join(
                os.path.abspath(os.getcwd()), "unit_test/dataframes/happy/df_1.xlsx"
            ),
        )
        == happy_response
    )


@pytest.mark.integration
def test_error_flash():
    assert (
        get_content(
            open("unit_test/decks/happy/deck_1.txt", "r").read(),
            os.path.join(
                os.path.abspath(os.getcwd()), "unit_test/dataframes/happy/df_1.xlsx"
            ),
        )
        == deck_contains_empty_lines_response
    )
