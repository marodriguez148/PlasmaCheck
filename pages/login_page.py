
from pages.base_page import BasePage
from playwright.sync_api import Page
from constants.constants import MEMBER_FACING_PORTAL_URL, PROVIDER_FACING_PORTAL_URL
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):
    PATH = "sign-in"

    def __init__(
            self,
            page: Page,
            host: str = MEMBER_FACING_PORTAL_URL,
            path: str = PATH,
            test_credentials: dict = None,
            login_required: bool = True
        ) -> None:
        super().__init__(page, host=host, path=path)
        self.test_credentials = test_credentials
        self.username_input = "input[id='email']"
        self.password_input = "input[id='password']"
        # self.sign_in_with_google_button = page.frame_locator(
        #     'iframe[title="Sign in with Google Button"]'
        # ).get_by_role("button", name="Sign in with Google. Opens in") # Can't find the button using this locator - need to investigate further
        self.join_link_button = "a[href='/join']"
        self.member_reset_password_link = "a[href='/forgot-password']"
        self.provider_reset_password_link = "a[href='/forgot-password/request']"
        self.provider_sign_up_link = "text='Click here to sign up'"
        self.submit_button = "button:has-text('Submit')"
        self.email_error_message = "text='The Email field is invalid.'"
        self.anchor_element = self.username_input

        if login_required:
            self.go_to_page()
            self.verify_login_page_elements()
            self.login()
            self.dismiss_cookie_banner()

    def login(self) -> None:
        logger.info(f"Attempting to log in with member: {self.test_credentials}")
        if self.test_credentials:
            self.page.fill(self.username_input, self.test_credentials.get("username"))
            self.page.fill(self.password_input, self.test_credentials.get("password"))
        else:
            raise ValueError("No test credentials provided for login.")
        self.page.click(self.submit_button)

    def verify_login_page_elements(self) -> None:
        logger.info("Verifying login page elements are visible.")
        self.wait_for_elem_visible(self.username_input)
        self.wait_for_elem_visible(self.password_input)
        # assert self.sign_in_with_google_button.is_visible(), "Sign in with Google button is not visible on the login page."
        if self.host == MEMBER_FACING_PORTAL_URL:
            self.wait_for_elem_visible(self.join_link_button)
            self.wait_for_elem_visible(self.member_reset_password_link)
        elif self.host == PROVIDER_FACING_PORTAL_URL:
            self.wait_for_elem_visible(self.provider_reset_password_link)
            self.wait_for_elem_visible(self.provider_sign_up_link)

    def verify_invalid_login(self) -> None:
        logger.info("Verifying behavior for invalid login.")
        self.go_to_page()
        self.verify_login_page_elements()
        self.login()
        self.wait_for_elem_visible(self.email_error_message)
        self.wait_for_elem_to_have_class(self.submit_button, "--appear-disabled", strict=False)
