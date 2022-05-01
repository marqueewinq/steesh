import pytest

from steesh.api.utils import format_deck


@pytest.mark.parametrize(
    "deck,expected",
    [
        (
            "1 Oneword\n2 Two words\nSomething unexpected\n",
            ["1 Oneword", "2 Two words"],
        ),
        (
            "Totally unexpected test \nAnothertotallyunexpectedtest\n\t1 Tabbed text",
            ["1 Tabbed text"],
        ),
    ],
)
def test_format_deck(deck, expected):
    assert format_deck(deck) == expected
