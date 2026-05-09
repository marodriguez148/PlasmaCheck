import re

from playwright.sync_api import Page, expect
from utils.logger import get_logger
from constants.constants import MEMBER_FACING_PORTAL_URL

logger = get_logger(__name__)


class BasePage:
    def __init__(
        self, page: Page, host: str = MEMBER_FACING_PORTAL_URL, path: str = ""
    ) -> None:
        self.page = page
        self.host = host.rstrip("/")
        self.path = path.lstrip("/")
        self.URL = self._build_url(self.host, self.path)
        self.sign_out = "button:has-text('Sign Out')"
        self.anchor_element = ""
        self.cookie_banner = "div[role='alertdialog']"
        self.accept_cookies_button = "button[data-tid='banner-accept']"

    @property
    def current_url(self) -> str:
        return self.page.url

    @staticmethod
    def _build_url(host: str, path: str = "") -> str:
        clean_host = host.rstrip("/")
        clean_path = path.lstrip("/")
        return f"{clean_host}/{clean_path}"

    def go_to_page(self, path: str | None = None) -> None:
        target_url = self._build_url(self.host, path if path is not None else self.path)
        logger.info(f"Navigating to page: {target_url}")
        self.page.goto(target_url)
        self.wait_for_page_load()

    def go_to_url(self, url: str) -> None:
        logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)
        self.wait_for_page_load()

    def refresh(self) -> None:
        logger.info("Refreshing page.")
        self.page.reload()

    def hover(self, selector: str) -> None:
        logger.info(f"Hovering over element: {selector}")
        self.page.locator(selector).hover()

    def scroll_to_element(self, selector: str) -> None:
        logger.info(f"Scrolling to element: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def wait_for_elem_visible(self, selector: str, timeout: int = 5000) -> None:
        logger.info(f"Waiting for element to be visible: {selector}")
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def wait_for_elem_invisible(self, selector: str, timeout: int = 5000) -> None:
        logger.info(f"Waiting for element to be invisible: {selector}")
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def wait_for_elem_clickable(self, selector: str, timeout: int = 5000) -> None:
        logger.info(f"Waiting for element to be clickable: {selector}")
        expect(self.page.locator(selector)).to_be_enabled(timeout=timeout)

    def wait_for_elem_to_have_text(
        self, selector: str, expected_text: str, timeout: int = 5000
    ) -> None:
        logger.info(f"Waiting for element {selector} to have text: {expected_text}")
        expect(self.page.locator(selector)).to_have_text(expected_text, timeout=timeout)

    def wait_for_elem_to_have_class(
        self,
        selector: str,
        expected_class: str,
        strict: bool = True,
        timeout: int = 5000,
    ) -> None:
        logger.info(f"Waiting for element {selector} to have class: {expected_class}")
        if strict:
            expect(self.page.locator(selector)).to_have_class(
                expected_class, timeout=timeout
            )
        else:
            expect(self.page.locator(selector)).to_have_class(
                re.compile(expected_class), timeout=timeout
            )

    def wait_for_elem_to_not_have_class(
        self, selector: str, unexpected_class: str, timeout: int = 5000
    ) -> None:
        logger.info(
            f"Waiting for element {selector} to not have class: {unexpected_class}"
        )
        class_name = self.page.locator(selector).get_attribute("class") or ""
        assert (
            unexpected_class not in class_name
        ), f"Expected element {selector} to not have class '{unexpected_class}', but it does. Current classes: '{class_name}'"

    def wait_for_page_load(self) -> None:
        logger.info("Waiting for page to load.")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.locator(self.anchor_element).wait_for()

    def is_enabled(self, selector: str) -> bool:
        logger.info(f"Checking if element is enabled: {selector}")
        return self.page.locator(selector).is_enabled()

    def is_disabled(self, selector: str) -> bool:
        logger.info(f"Checking if element is disabled: {selector}")
        return self.page.locator(selector).is_disabled()

    def verify_url_contains(self, expected_substring: str) -> None:
        logger.info(f"Verifying URL contains substring: {expected_substring}")
        assert (
            expected_substring in self.current_url
        ), f"Expected URL to contain '{expected_substring}', but got '{self.current_url}'"

    def verify_url(self, expected_url: str | None = None, timeout: int = 5000) -> None:
        expected_url = expected_url or self.URL
        logger.info(f"Verifying URL is correct: {expected_url}")
        expect(self.page).to_have_url(expected_url, timeout=timeout)

    def dismiss_cookie_banner(self) -> None:
        logger.info("Attempting to dismiss cookie banner if present.")
        if self.page.locator(self.cookie_banner).is_visible():
            self.page.click(self.accept_cookies_button)
            self.wait_for_elem_invisible(self.cookie_banner)

    def sign_out(self) -> None:
        logger.info("Attempting to sign out.")
        self.page.click(self.sign_out)
        self.wait_for_elem_invisible("button[class*='desktop-logout']")
        assert (
            "/sign_in" in self.current_url
        ), f"Expected to be redirected to login page after sign out, but current URL is '{self.current_url}'"
