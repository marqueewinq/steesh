from typing import List, Text

from steesh.renderer.renderer import (
    generate_tables_of_cards,
    read_deck_from_str,
    read_library,
    render_table_html,
)


def render_response(
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
