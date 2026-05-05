from pages.login_page import LoginPage
from playwright.sync_api import Page
from constants.constants import MEMBER_FACING_PORTAL_URL


class MemberDashboardPage(LoginPage):
    def __init__(self, 
            page: Page, 
            url: str = f"{MEMBER_FACING_PORTAL_URL}/", 
            test_credentials: dict = None,
            login_required: bool = True
        ):
        super().__init__(
            page=page, 
            url=url, 
            test_credentials=test_credentials, 
            login_required=login_required
        )
        self.book_a_scan_button = "button[data-testid='book-scan-btn']"

    def verify_dashboard_elements(self) -> None:
        assert self.page.is_visible(self.book_a_scan_button), "Book a Scan button is not visible on the member dashboard page."

