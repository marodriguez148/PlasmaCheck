import pytest

from pages.member_dashboard_page import MemberDashboardPage
from constants.constants import TEST_CREDENTIALS
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="function")
def user_token(page: Page) -> str:
    logger.info("Logging in and retrieving user token.")
    page = MemberDashboardPage(
        page, TEST_CREDENTIALS["default_qa_user"], login_required=True
    )
    page.wait_for_page_load()
    return page.get_bearer_token()
