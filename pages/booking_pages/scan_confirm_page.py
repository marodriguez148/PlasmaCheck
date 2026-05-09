from pages.base_page import BasePage
from playwright.sync_api import Page


class ScanConfirmPage(BasePage):
    PATH = "/sign-up/scan-confirm"
    RETURNING_PATH = "/book-scan/scan-confirm"

    @classmethod
    def for_new_user(cls, page: Page) -> "ScanConfirmPage":
        return cls(page, path=cls.PATH)

    @classmethod
    def for_returning_user(cls, page: Page) -> "ScanConfirmPage":
        return cls(page, path=cls.RETURNING_PATH)

    def __init__(self, page: Page, path: str = PATH):
        super().__init__(page, path=path)
        self.page_title = "Scan Confirmation"
        self.scan_details_selector = "div[class='scan-details']"
        self.begin_medical_questionnaire_button = (
            "button:has-text('Begin Medical Questionnaire')"
        )
        self.back_to_dashboard_button_selector = (
            "a:has(div:has-text('Go to Dashboard'))"
        )

    def verify_page_elements(self) -> None:
        self.wait_for_elem_visible(self.scan_details_selector)
        self.wait_for_elem_visible(self.begin_medical_questionnaire_button)
        self.wait_for_elem_visible(self.back_to_dashboard_button_selector)

    def click_back_to_dashboard(self) -> None:
        self.page.click(self.back_to_dashboard_button_selector)
