import logging
import pytest
from playwright.sync_api import sync_playwright
from utils.logger import configure_logging


def pytest_configure(config):
    configure_logging(level="INFO", log_dir="plasma_checker_logs/")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    root = logging.getLogger("plasma_checker")
    root.info("=" * 60)
    root.info("START: %s", request.node.name)
    root.info("=" * 60)
    yield
    rep = getattr(request.node, "rep_call", None)
    outcome = (
        "PASSED"
        if rep and rep.passed
        else "FAILED" if rep and rep.failed else "UNKNOWN"
    )
    root.info("END: %s (%s)", request.node.name, outcome)
    root.info("=" * 60)


@pytest.fixture(scope="session")
def page(request):
    browser_name = request.config.getoption("--browser")[0]
    headless = request.config.getoption("--headed")

    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            screen={"width": 1440, "height": 900},
        )
        page = context.new_page()
        yield page
        context.close()
        browser.close()
