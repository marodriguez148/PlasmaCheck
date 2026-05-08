import re

from playwright.sync_api import Page, expect
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseComponent:
    def __init__(self, page: Page, root_selector: str) -> None:
        self.page = page
        self.root = page.locator(root_selector)
        self.selector_text = root_selector

    def verify_elem_visible(self, timeout: int = 5000) -> None:
        logger.info(f"Verifying element is visible: {self.selector_text}")
        expect(self.root).to_be_visible(timeout=timeout)

    def verify_elem_hidden(self, timeout: int = 5000) -> None:
        logger.info(f"Verifying element is hidden: {self.selector_text}")
        expect(self.root).to_be_hidden(timeout=timeout)

    def is_visible(self) -> bool:
        logger.info("Checking if component is visible.")
        return self.root.is_visible()

    def click_on_element(self) -> None:
        logger.info(f"Clicking element: {self.selector_text}")
        self.root.click()

    def scroll_to_component(self, selector: str = None) -> None:
        logger.info(f"Scrolling to component: {self.selector_text}")
        if selector:
            self.page.locator(selector).scroll_into_view_if_needed()
        else:
            self.root.scroll_into_view_if_needed()

    def fill(self, value: str) -> None:
        logger.info(f"Filling element {self.selector_text} with: {value}")
        self.root.fill(value)

    def get_text(self, selector: str = None) -> str:
        logger.info(f"Getting text from element: {self.selector_text}")
        if selector:
            return self.root.locator(selector).inner_text()
        return self.root.inner_text()

    def verify_text(self, expected_text: str, timeout: int = 5000) -> None:
        logger.info(f"Verifying element {self.selector_text} has text: {expected_text}")
        expect(self.root).to_have_text(expected_text, timeout=timeout)

    def verify_has_class(self, expected_class: str, selector: str = None, strict: bool = True, timeout: int = 5000) -> None:
        if selector:
            class_selector = selector
        else:
            class_selector = self.selector_text
            
        logger.info(f"Verifying element {class_selector} has class: {expected_class}")
        locator = self.root.locator(class_selector)
        if strict:
            expect(locator).to_have_class(expected_class, timeout=timeout)
        else:
            expect(locator).to_have_class(re.compile(expected_class), timeout=timeout)

