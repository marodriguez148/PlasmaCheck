import re

from pages.base_page import BasePage
from components.dropdown import Dropdown
from playwright.sync_api import Page, expect
from constants.constants import MEMBER_FACING_PORTAL_URL
import random
from tests.conftest import page


class SelectPlanPage(BasePage):
    PATH = "/sign-up/select-plan"

    def __init__(self, page: Page, host: str = MEMBER_FACING_PORTAL_URL):
        super().__init__(page, host=host, path=self.PATH)
        self.page_title = "Select Your Plan"
        self.dob_input_selector = "input[id='dob']"
        self.sex_at_birth_dropdown_selector = Dropdown(self.page, "div[class='multiselect']")
        self.plan_encounter_card_selector = "div[class*='encounter-card']"
        self.continue_button_selector = "button:has-text('Continue')"
        self.cancel_button_selector = "button:has-text('Cancel')"

    def verify_page_elements(self) -> None:
        if "/sign-up" in self.current_url:
            self.wait_for_elem_visible(self.dob_input_selector)
            self.sex_at_birth_dropdown_selector.wait_for_visible()
        expect(self.page.locator(self.plan_encounter_card_selector).first).to_be_visible() # Would get data from DB to get exact number of encounter cards
        self.wait_for_elem_visible(self.continue_button_selector)
        self.wait_for_elem_to_have_class(self.continue_button_selector, "--appear-disabled", strict=False)
        self.wait_for_elem_visible(self.cancel_button_selector)


    def verify_selecting_plan(self, plan_name: str) -> None:
        if "/sign-up" in self.current_url:
            self.page.fill(self.dob_input_selector, "01011990")
            self.sex_at_birth_dropdown_selector.select_option(random.choice(["Male", "Female"]))
        self.select_plan_by_name(plan_name)
        button_classes = self.page.locator(self.continue_button_selector).get_attribute("class") or ""
        assert "--appear-disabled" not in button_classes

        self.page.click(self.continue_button_selector)
        

    def select_plan_by_name(self, plan_name: str) -> None:
        plan_card = self.page.locator(f"{self.plan_encounter_card_selector} p:text-is('{plan_name}')")
        expect(plan_card).to_be_visible()
        plan_card.click()


    def verify_addon_card(self, addon_name: str) -> None:
        # Want to automate this but there may be a potenial bug with selection the encounter card and what addon card appears
        pass