from pages.login_page import LoginPage
from playwright.sync_api import Page
from constants.constants import MEMBER_FACING_PORTAL_URL


class MemberDashboardPage(LoginPage):

    def __init__(self, 
            page: Page,
            test_credentials: dict = None,
            login_required: bool = True
        ):
        super().__init__(
            page=page,
            test_credentials=test_credentials, 
            login_required=login_required
        )
        self.book_a_scan_button = "div[class*='my-appointments'] button[data-testid='book-scan-btn']"
        self.anchor_element = self.book_a_scan_button

    def verify_dashboard_elements(self) -> None:
        self.wait_for_elem_visible(self.book_a_scan_button)

    def book_a_scan(self) -> None:
        self.logger.info("Clicking 'Book a Scan' button on member dashboard.")
        self.page.click(self.book_a_scan_button)
