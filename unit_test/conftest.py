import pytest


def pytest_addoption(parser):
    parser.addoption("--pdf", action="store_true", default=False, help="run pdf tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "pdf: mark test as pdf to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--pdf"):
        # --pdf given in cli: do not skip pdf tests
        return
    skip_pdf = pytest.mark.skip(reason="need --pdf option to run")
    for item in items:
        if "pdf" in item.keywords:
            item.add_marker(skip_pdf)
