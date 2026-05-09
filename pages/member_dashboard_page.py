from pages.login_page import LoginPage
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


class MemberDashboardPage(LoginPage):
    DASHBOARD_PATH = ""

    def __init__(
        self, page: Page, test_credentials: dict = None, login_required: bool = True
    ):
        super().__init__(
            page=page, test_credentials=test_credentials, login_required=login_required
        )
        self.URL = self._build_url(self.host, self.DASHBOARD_PATH)
        self.book_a_scan_button = (
            "div[class*='my-appointments'] button[data-testid='book-scan-btn']"
        )
        self.empty_appointments = "div[class='appointments--none']"
        self.anchor_element = self.book_a_scan_button

    def verify_dashboard_elements(self) -> None:
        self.wait_for_elem_visible(self.book_a_scan_button)

    def book_a_scan(self) -> None:
        logger.info("Clicking 'Book a Scan' button on member dashboard.")
        self.page.click(self.book_a_scan_button)

    def is_appointments_empty(self) -> bool:
        self.wait_for_page_load()
        return self.page.locator(self.empty_appointments).is_visible()
