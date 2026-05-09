from components.base_component import BaseComponent
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


class Dropdown(BaseComponent):
    def __init__(self, page: Page, root_selector: str, options: list) -> None:
        super().__init__(page, root_selector)
        self.selected_option = "span[class='multiselect__single']"
        self.deselected_option = "span:not([class*='selected']) span:text-is('{}')"
        self.options = options

    def select_option(self, option_text: str) -> None:
        if option_text not in self.options:
            raise ValueError(
                f"Option '{option_text}' is not a valid option. Valid options are: {self.options}"
            )

        if self._get_selected_option() == option_text:
            logger.info(f"Option '{option_text}' is already selected.")
            return

        deselected_option_selector = self.deselected_option.format(option_text)
        self.root.click()
        self.page.locator(deselected_option_selector).click()

    def _get_selected_option(self) -> str:
        return self.get_text(self.selected_option)

    def verify_select_options(self) -> None:
        self.root.click()  # open the dropdown first
        texts = self.page.locator("span.multiselect__option").all_text_contents()
        for option in self.options:
            assert (
                option in texts
            ), f"Expected option '{option}' not found. Found: {texts}"
