import re

from pages.base_page import BasePage
from playwright.sync_api import Page, expect
from constants.constants import MEMBER_FACING_PORTAL_URL, PROVIDER_FACING_PORTAL_URL

class LoginPage(BasePage):
    def __init__(
            self, 
            page: Page, 
            url: str = MEMBER_FACING_PORTAL_URL, 
            test_credentials: dict = None,
            login_required: bool = True
        ) -> None:
        super().__init__(page)
        self.test_credentials = test_credentials
        self.URL = url + "sign-in"
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
            self.go_to_url(self._get_login_url())
            self.wait_for_page_load()
            self.verify_login_page_elements()
            self.login()

    def login(self) -> None:
        self.logger.info(f"Attempting to log in with member: {self.test_credentials}")
        if self.test_credentials:
            self.page.fill(self.username_input, self.test_credentials.get("username"))
            self.page.fill(self.password_input, self.test_credentials.get("password"))
        else:
            raise ValueError("No test credentials provided for login.")
        self.page.click(self.submit_button)

    def verify_login_page_elements(self) -> None:
        self.logger.info("Verifying login page elements are visible.")
        self.wait_for_elem_visible(self.username_input)
        self.wait_for_elem_visible(self.password_input)
        # assert self.sign_in_with_google_button.is_visible(), "Sign in with Google button is not visible on the login page."
        if self.URL == MEMBER_FACING_PORTAL_URL:
            self.wait_for_elem_visible(self.join_link_button)
            self.wait_for_elem_visible(self.member_reset_password_link)
        elif self.URL == PROVIDER_FACING_PORTAL_URL:
            self.wait_for_elem_visible(self.provider_reset_password_link)
            self.wait_for_elem_visible(self.provider_sign_up_link)

    def verify_invalid_login(self) -> None:
        self.logger.info("Verifying behavior for invalid login.")
        self.go_to_url(self.URL)
        self.verify_login_page_elements()
        self.login()
        self.wait_for_elem_visible(self.email_error_message)
        self.wait_for_elem_to_have_class(self.submit_button, "--appear-disabled", strict=False)

    
    def _get_login_url(self) -> str: 
        # Determine which portal URL to use based on the provided URL
        if MEMBER_FACING_PORTAL_URL in self.URL:
            return MEMBER_FACING_PORTAL_URL
        elif PROVIDER_FACING_PORTAL_URL in self.URL:
            return PROVIDER_FACING_PORTAL_URL
        else:
            raise ValueError(f"Invalid URL provided for login page: {self.URL}")