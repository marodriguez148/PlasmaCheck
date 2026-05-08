import random

from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from components.dropdown import Dropdown
from utils.logger import get_logger

logger = get_logger(__name__)

class ScheduleScanPage(BasePage):
    PATH = "/sign-up/schedule-scan"

    def __init__(self, page: Page):
        super().__init__(page, path=self.PATH)
        self.page_title = "Schedule Your Scan"
        self.state_dropdown_options = [
            "Alaska",
            "California",
            "Delaware",
            "Florida",
            "New Jersey",
            "New York",
        ]
        self.state_dropdown_selector = Dropdown(self.page, "div[class='multiselect']", options=self.state_dropdown_options)
        self.locator_card_selector = "p[class*='location-card__name']"
        self.calendar_selector = "div[class*='vuecal--month-view']"
        self.time_selector = "div[class='appointments']"
        self.calendar_open_date_selector = "div[class*='vuecal__cell--day']:not([class*='disabled'])"
        self.time_slot_selector = "div[class*='individual-appointment']:not([style='display: none;'])"
        self.continue_button_selector = "button[data-test='submit']:has-text('Continue')"
        self.go_back_button_selector = "button:has-text('Back')"


    def verify_page_elements(self) -> None:
        self.state_dropdown_selector.verify_elem_visible()
        expect(self.page.locator(self.locator_card_selector).first).to_be_visible() # Would get data from DB to get exact number of locator cards
        self.wait_for_elem_visible(self.continue_button_selector)
        self.wait_for_elem_to_have_class(self.continue_button_selector, "--appear-disabled", strict=False)
        self.wait_for_elem_visible(self.go_back_button_selector)

    def verify_state_selection(self, state: str) -> None:
        # Would need to know which locations are in which states to fully automate this test
        pass

    def select_location(self) -> None:
        self.page.locator(self.locator_card_selector).first.click()

    def verify_scheduling_scan(self) -> None:
        self.select_location()
        self.wait_for_elem_visible(self.calendar_selector, timeout=30000)
        open_dates = self.page.locator(self.calendar_open_date_selector).all()
        logger.info(f"Found {len(open_dates)} open dates on the calendar.")
        random.choice(open_dates).click()
        self.wait_for_elem_visible(self.time_selector)
        available_time_slots = self.page.locator(self.time_slot_selector).all()
        logger.info(f"Found {len(available_time_slots)} available time slots for the selected date.")
        random.choice(available_time_slots).click()
        self.wait_for_elem_to_not_have_class(self.continue_button_selector, "--appear-disabled")
        self.page.click(self.continue_button_selector)