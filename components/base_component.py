import re

from playwright.sync_api import Page, expect
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseComponent:
    def __init__(self, page: Page, root_selector: str) -> None:
        self.page = page
        self.root = page.locator(root_selector)
        self.selector_text = root_selector

    def is_visible(self) -> bool:
        logger.info("Checking if component is visible.")
        return self.root.is_visible()

    def wait_for_visible(self, timeout: int = 5000) -> None:
        logger.info("Waiting for component to be visible.")
        expect(self.root).to_be_visible(timeout=timeout)

    def wait_for_hidden(self, timeout: int = 5000) -> None:
        logger.info("Waiting for component to be hidden.")
        expect(self.root).to_be_hidden(timeout=timeout)

    def click(self, selector: str) -> None:
        logger.info(f"Clicking element: {selector}")
        self.root.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        logger.info(f"Filling element {selector} with: {value}")
        self.root.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        logger.info(f"Getting text from element: {selector}")
        return self.root.locator(selector).inner_text()

    def verify_text(self, selector: str, expected_text: str, timeout: int = 5000) -> None:
        logger.info(f"Verifying element {selector} has text: {expected_text}")
        expect(self.root.locator(selector)).to_have_text(expected_text, timeout=timeout)

    def verify_has_class(self, selector: str, expected_class: str, strict: bool = True, timeout: int = 5000) -> None:
        logger.info(f"Verifying element {selector} has class: {expected_class}")
        locator = self.root.locator(selector)
        if strict:
            expect(locator).to_have_class(expected_class, timeout=timeout)
        else:
            expect(locator).to_have_class(re.compile(expected_class), timeout=timeout)

    def verify_elem_visible(self, selector: str, timeout: int = 5000) -> None:
        logger.info(f"Verifying element is visible: {selector}")
        expect(self.root.locator(selector)).to_be_visible(timeout=timeout)

    def verify_elem_hidden(self, selector: str, timeout: int = 5000) -> None:
        logger.info(f"Verifying element is hidden: {selector}")
        expect(self.root.locator(selector)).to_be_hidden(timeout=timeout)
