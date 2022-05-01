import pytest


def pytest_addoption(parser):
    parser.addoption("--pdf", action="store_true", default=False, help="run pdf tests")
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "pdf: mark test as pdf to run")
    config.addinivalue_line("markers", "integration: mark test as pdf to run")


def pytest_collection_modifyitems(config, items):
    allowed_extra_options = ["--pdf", "--integration"]
    for option in allowed_extra_options:
        if config.getoption(option):
            continue

        # option flag is not given in cli: mark relevant tests with `skip`
        flag = option.strip("--")
        skip_marker = pytest.mark.skip(reason=f"pass {option} to pytest to run")
        for item in items:
            if flag in item.keywords:
                item.add_marker(skip_marker)
