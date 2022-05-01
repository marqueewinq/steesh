import re

from steesh.renderer.renderer import (
    generate_tables_of_cards,
    read_deck_from_str,
    read_library,
    render_table_html,
)


def render_response(
    library_path: str,
    deck: list[str],
    template_path: str = "examples/templates/test_card_template.html",
) -> str:
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


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ["csv", "xlsx"]


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
