import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def page(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    with sync_playwright() as p:
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=headless)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        

        context = browser.new_context()
        page = context.new_page() 
        yield page
        context.close()
        browser.close()
