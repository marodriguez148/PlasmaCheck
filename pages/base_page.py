import re

from playwright.sync_api import Page, expect
from utils.logger import get_logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.URL = ""
        self.sign_out = "button:has-text('Sign Out')"
        self.anchor_element = ""
        self.logger = get_logger(self.__class__.__name__)

    @property
    def current_url(self) -> str:
        return self.page.url
    
    def go_to_page(self) -> None:
        self.logger.info(f"Navigating to page: {self.URL}")
        self.page.goto(self.URL)

    def go_to_url(self, url: str) -> None:
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        self.wait_for_page_load()

    def refresh(self) -> None:
        self.logger.info("Refreshing page.")
        self.page.reload()

    def hover(self, selector: str) -> None:
        self.logger.info(f"Hovering over element: {selector}")
        self.page.locator(selector).hover()
    
    def scroll_to_element(self, selector: str) -> None:
        self.logger.info(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def wait_for_elem_visible(self, selector: str, timeout: int = 5000) -> None:
        self.logger.info(f"Waiting for element to be visible: {selector}")
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def wait_for_elem_invisible(self, selector: str, timeout: int = 5000) -> None:
        self.logger.info(f"Waiting for element to be invisible: {selector}")
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def wait_for_elem_to_have_class(self, selector: str, expected_class: str, strict: bool = True, timeout: int = 5000) -> None:
        self.logger.info(f"Waiting for element to have class: {selector}")
        if strict:
            expect(self.page.locator(selector)).to_have_class(expected_class, timeout=timeout)
        else:
            expect(self.page.locator(selector)).to_have_class(re.compile(expected_class), timeout=timeout)

    def wait_for_page_load(self) -> None:
        self.logger.info("Waiting for page to load.")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.locator(self.anchor_element).wait_for()

    def is_visible(self, selector: str) -> bool:
        self.logger.info(f"Checking if element is visible: {selector}")
        return self.page.locator(selector).is_visible()

    def is_hidden(self, selector: str) -> bool:
        self.logger.info(f"Checking if element is hidden: {selector}")
        return self.page.locator(selector).is_hidden()

    def is_enabled(self, selector: str) -> bool:
        self.logger.info(f"Checking if element is enabled: {selector}")
        return self.page.locator(selector).is_enabled()
    
    def is_disabled(self, selector: str) -> bool:
        self.logger.info(f"Checking if element is disabled: {selector}")
        return self.page.locator(selector).is_disabled()

    def verify_url_contains(self, expected_substring: str) -> None:
        self.logger.info(f"Verifying URL contains substring: {expected_substring}")
        assert expected_substring in self.current_url(), f"Expected URL to contain '{expected_substring}', but got '{self.current_url()}'"

    def verify_url(self) -> None:
        self.logger.info(f"Verifying URL is correct: {self.URL}")
        assert self.current_url == self.URL, f"Expected URL to be '{self.URL}', but got '{self.current_url}'"

    def sign_out(self) -> None:
        self.logger.info("Attempting to sign out.")
        self.page.click(self.sign_out)
        assert self.page.is_visible("button[class*='desktop-logout']") == False, "Sign out failed, logout button still visible."
        assert "/sign_in" in self.current_url(), f"Expected to be redirected to login page after sign out, but current URL is '{self.current_url()}'"
