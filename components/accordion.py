from components.base_component import BaseComponent
from playwright.sync_api import Page, expect
from utils.logger import get_logger

logger = get_logger(__name__)

STRIPE_FRAME_SELECTOR = "iframe[title='Secure payment input frame'][role='presentation']:not([aria-hidden='true'])"


class Accordion(BaseComponent):
    def __init__(self, page: Page, root_selector: str):
        super().__init__(page, root_selector=root_selector)
        self.accordion_elements = {}
        self.frame = self.page.frame_locator(STRIPE_FRAME_SELECTOR)

    def _button(self, accordion_item: str):
        return self.frame.locator(
            f"[role='button'][data-value='{accordion_item.lower()}']"
        )

    def verify_elem_visible(self, timeout: int = 5000) -> None:
        logger.info(f"Verifying accordion is visible: {self.selector_text}")
        expect(self.page.locator(STRIPE_FRAME_SELECTOR)).to_be_visible()

    def is_expanded(self, accordion_item: str) -> bool:
        expect(self.page.locator(STRIPE_FRAME_SELECTOR)).to_be_visible()
        return self._button(accordion_item).get_attribute("aria-expanded") == "true"

    def expand_accordion_item(self, accordion_item: str) -> None:
        logger.info(f"Expanding accordion item: {accordion_item}")
        if self.is_expanded(accordion_item):
            logger.info(f"Accordion item '{accordion_item}' is already expanded.")
            return
        self.page.locator(STRIPE_FRAME_SELECTOR).evaluate(
            "el => el.scrollIntoView({block: 'center'})"
        )
        self._button(accordion_item).click(force=True)

    def verify_expanded_accordion_elements(self, accordion_item: str) -> None:
        if accordion_item not in self.accordion_elements:
            raise ValueError(
                f"Accordion item '{accordion_item}' does not have defined elements to verify."
            )

        self.expand_accordion_item(accordion_item)
        for key, element_selector in self.accordion_elements[accordion_item].items():
            if key == "optional_fields":
                continue  # Optional fields are only visable when the card info has been filled out
            expect(self.frame.locator(element_selector)).to_be_visible()
