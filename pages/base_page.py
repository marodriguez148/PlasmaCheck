from playwright.sync_api import Page
from utils.logger import get_logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.URL = ""
        self.sign_out = "button:has-text('Sign Out')"
        self.logger = get_logger(self.__class__.__name__)

    @property
    def current_url(self) -> str:
        return self.page.url
    
    def go_to_page(self) -> None:
        self.page.goto(self.URL)

    def go_to_url(self, url: str) -> None:
        self.page.goto(url)

    def refresh(self) -> None:
        self.page.reload()

    def hover(self, selector: str) -> None:
        self.page.locator(selector).hover()
    
    def scroll_to_element(self, selector: str) -> None:
        self.page.locator(selector).scroll_into_view_if_needed()

    def wait_for_page_load(self) -> None:
        self.page.wait_for_load_state("DOMContentLoaded")

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def is_hidden(self, selector: str) -> bool:
        return self.page.locator(selector).is_hidden()

    def is_enabled(self, selector: str) -> bool:
        return self.page.locator(selector).is_enabled()
    
    def is_disabled(self, selector: str) -> bool:
        return self.page.locator(selector).is_disabled()

    def verify_url_contains(self, expected_substring: str) -> None:
        assert expected_substring in self.current_url(), f"Expected URL to contain '{expected_substring}', but got '{self.current_url()}'"

    def verify_url(self) -> None:
        assert self.current_url() == self.URL, f"Expected URL to be '{self.URL}', but got '{self.current_url()}'"

    def sign_out(self) -> None:
        self.page.click(self.sign_out)
        assert self.page.is_visible("button[class*='desktop-logout']") == False, "Sign out failed, logout button still visible."
        assert "/sign_in" in self.current_url(), f"Expected to be redirected to login page after sign out, but current URL is '{self.current_url()}'"
