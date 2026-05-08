from pages.member_dashboard_page import MemberDashboardPage
from pages.booking_pages.select_plan_page import SelectPlanPage
from pages.booking_pages.schedule_scan_page import ScheduleScanPage
from pages.booking_pages.scan_confirm_page import ScanConfirmPage
from pages.booking_pages.reserve_appointment_page import ReserveAppointmentPage
from tests.base_test import BaseTest
from constants.constants import TEST_CREDENTIALS
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)

class TestBookingScan(BaseTest):
    def test_booking_scan(self, page: Page, test_card_info: dict) -> None:
        member_dashboard_page = MemberDashboardPage(
            page,
            test_credentials=TEST_CREDENTIALS["default_qa_user"]
        )
        member_dashboard_page.verify_url()
        is_returning = not member_dashboard_page.is_appointments_empty()
        member_dashboard_page.book_a_scan()

        select_plan_page = SelectPlanPage.for_returning_user(page) if is_returning else SelectPlanPage.for_new_user(page)
        select_plan_page.verify_url()
        select_plan_page.verify_page_elements()
        select_plan_page.verify_selecting_plan("MRI Scan")

        schedule_scan_page = ScheduleScanPage.for_returning_user(page) if is_returning else ScheduleScanPage.for_new_user(page)
        schedule_scan_page.verify_url()
        schedule_scan_page.verify_page_elements()
        schedule_scan_page.verify_scheduling_scan()

        reserve_appointment_page = ReserveAppointmentPage.for_returning_user(page) if is_returning else ReserveAppointmentPage.for_new_user(page)
        reserve_appointment_page.verify_url(timeout=20000)
        reserve_appointment_page.verify_page_elements()
        reserve_appointment_page.verify_payment_info_entry(test_card_info)

        scan_confirm_page = ScanConfirmPage.for_returning_user(page) if is_returning else ScanConfirmPage.for_new_user(page)
        scan_confirm_page.verify_url(timeout=20000)
        scan_confirm_page.verify_page_elements()
        scan_confirm_page.click_back_to_dashboard()
        member_dashboard_page.verify_url()