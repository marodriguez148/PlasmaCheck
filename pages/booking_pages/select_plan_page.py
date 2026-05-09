import random

from pages.base_page import BasePage
from components.dropdown import Dropdown
from playwright.sync_api import Page, expect
from utils.logger import get_logger

logger = get_logger(__name__)


class SelectPlanPage(BasePage):
    PATH = "/sign-up/select-plan"
    RETURNING_PATH = "/book-scan/select-plan"

    @classmethod
    def for_new_user(cls, page: Page) -> "SelectPlanPage":
        return cls(page, path=cls.PATH)

    @classmethod
    def for_returning_user(cls, page: Page) -> "SelectPlanPage":
        return cls(page, path=cls.RETURNING_PATH)

    def __init__(self, page: Page, path: str = PATH):
        super().__init__(page, path=path)
        self.page_title = "Select Your Plan"
        self.dob_input_selector = "input[id='dob']"
        self.sex_at_birth_dropdown_selector = Dropdown(
            self.page, "div[class='multiselect']", options=["Male", "Female"]
        )
        self.plan_encounter_card_selector = "div[class*='encounter-card']"
        self.continue_button_selector = "button:has-text('Continue')"
        self.cancel_button_selector = "button:has-text('Cancel')"

    def verify_page_elements(self) -> None:
        if "/sign-up" in self.current_url:
            self.wait_for_elem_visible(self.dob_input_selector)
            self.sex_at_birth_dropdown_selector.verify_elem_visible()
        expect(
            self.page.locator(self.plan_encounter_card_selector).first
        ).to_be_visible()  # Would get data from DB to get exact number of encounter cards
        self.wait_for_elem_visible(self.continue_button_selector)
        self.wait_for_elem_to_have_class(
            self.continue_button_selector, "--appear-disabled", strict=False
        )
        self.wait_for_elem_visible(self.cancel_button_selector)

    def verify_selecting_plan(self, plan_name: str) -> None:
        if "/sign-up" in self.current_url:
            self.page.fill(self.dob_input_selector, "01011990")
            self.sex_at_birth_dropdown_selector.select_option(
                random.choice(["Male", "Female"])
            )
        self.select_plan_by_name(plan_name)
        self.wait_for_elem_to_not_have_class(
            self.continue_button_selector, "--appear-disabled"
        )

        self.page.click(self.continue_button_selector)

    def select_plan_by_name(self, plan_name: str) -> None:
        plan_card = self.page.locator(
            f"{self.plan_encounter_card_selector} p:text-is('{plan_name}')"
        )
        expect(plan_card).to_be_visible()
        plan_card.click()

    def verify_addon_card(self, addon_name: str) -> None:
        # Want to automate this but there may be a potenial bug with selection the encounter card and what addon card appears
        pass
