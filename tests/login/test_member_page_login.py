from pages.member_dashboard_page import MemberDashboardPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from constants.constants import TEST_CREDENTIALS
from playwright.sync_api import Page


class TestMemberPageLogin(BaseTest):
    def test_member_page_login(self, page: Page) -> None:
        member_dashboard_page = MemberDashboardPage(
            page, 
            test_credentials=TEST_CREDENTIALS["default_qa_user"]
        )
        member_dashboard_page.verify_url()
        member_dashboard_page.verify_dashboard_elements()

    def test_invalid_member_page_login(self, page: Page) -> None:
        login_page = LoginPage(
            page, 
            test_credentials={"username": "invalid_user", "password": "invalid_pass"},
            login_required=False
        )
        login_page.verify_invalid_login()