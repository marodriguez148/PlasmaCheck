from pages.member_dashboard_page import MemberDashboardPage
from pages.booking_pages.select_plan_page import SelectPlanPage
from pages.booking_pages.schedule_scan_page import ScheduleScanPage
from tests.base_test import BaseTest
from constants.constants import TEST_CREDENTIALS
from playwright.sync_api import Page

class TestBookingScan(BaseTest):
    def test_booking_scan(self, page: Page) -> None:
        member_dashboard_page = MemberDashboardPage(
            page, 
            test_credentials=TEST_CREDENTIALS["default_qa_user"]
        )
        member_dashboard_page.verify_url()
        member_dashboard_page.book_a_scan()
        select_plan_page = SelectPlanPage(page)
        select_plan_page.verify_url()
        select_plan_page.verify_page_elements()
        select_plan_page.verify_selecting_plan("MRI Scan")
        schedule_scan_page = ScheduleScanPage(page)
        schedule_scan_page.verify_url()
        schedule_scan_page.verify_page_elements()
        schedule_scan_page.verify_scheduling_scan()