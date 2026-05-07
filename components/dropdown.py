from components.base_component import BaseComponent
from playwright.sync_api import Page, expect

class Dropdown(BaseComponent):
    def __init__(self, page: Page, root_selector: str) -> None:
        super().__init__(page, root_selector)
        self.male_option_selected = "span[class*='selected']:text-is('Male')"
        self.male_option_deselected = "span:not([class*='selected']):text-is('Male')"
        self.female_option_selected = "span[class*='selected']:text-is('Female')"
        self.female_option_deselected = "span:not([class*='selected']):text-is('Female')"

    def select_option(self, option_text: str) -> None:
        selected_option = self._get_selected_option_selector(option_text)
        if option_text == "Male" and selected_option == self.male_option_selected:
            self.logger.info(f"Option '{option_text}' is already selected.")
            return
        
        elif option_text == "Female" and selected_option == self.female_option_selected:
            self.logger.info(f"Option '{option_text}' is already selected.")
            return
        
        elif option_text == "Male" and selected_option == self.female_option_selected:
            self.logger.info(f"Switching selection to '{option_text}'.")
            self.root.click()
            self.page.locator(self.male_option_deselected).click()

        elif option_text == "Female" and selected_option == self.male_option_selected:
            self.logger.info(f"Switching selection to '{option_text}'.")
            self.root.click()
            self.page.locator(self.female_option_deselected).click()

        elif option_text not in ["Male", "Female"]:
            raise ValueError(f"Unexpected option text: {option_text}")


    def _get_selected_option_selector(self, option_text: str) -> str:
        gender_option = self.get_text("span[class='multiselect__single']")
        if gender_option == "Male":
            return self.male_option_selected
        elif gender_option == "Female":
            return self.female_option_selected
        else:
            raise ValueError(f"Unexpected gender option: {gender_option}")