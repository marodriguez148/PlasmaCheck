from base_page import BasePage
from playwright.sync_api import Page
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
        self.URL = url
        self.username_input = "input[id='email']"
        self.password_input = "input[id='password']"
        self.sign_in_with_google_button = "div[aria-label='Sign in with Google. Opens in new tab']"
        self.join_link_button = "a[href='/join']"
        self.member_reset_password_link = "a[href='/forgot-password']"
        self.provider_reset_password_link = "a[href='/forgot-password/request']"
        self.provider_sign_up_link = "text='Click here to sign up'"
        self.submit_button = "button[class*='submit-btn']"

        if login_required:
            self.go_to_url(self._get_login_url())
            self.verify_login_page_elements()
            self.login()
            self.wait_for_page_load()

    def login(self) -> None:
        self.logger.info(f"Attempting to log in with member: {self.test_credentials}")
        if self.test_credentials:
            self.page.fill(self.username_input, self.test_credentials.get("username"))
            self.page.fill(self.password_input, self.test_credentials.get("password"))
        else:
            raise ValueError("No test credentials provided for login.")
        self.page.click(self.submit_button)

    def verify_login_page_elements(self) -> None:
        assert self.page.is_visible(self.username_input), "Username input is not visible on the login page."
        assert self.page.is_visible(self.password_input), "Password input is not visible on the login page."
        assert self.page.is_visible(self.sign_in_with_google_button), "Sign in with Google button is not visible on the login page."
        if self.URL == MEMBER_FACING_PORTAL_URL:
            assert self.page.is_visible(self.join_link_button), "Join link is not visible on the member login page."
            assert self.page.is_visible(self.member_reset_password_link), "Reset password link is not visible on the member login page."
        elif self.URL == PROVIDER_FACING_PORTAL_URL:
            assert self.page.is_visible(self.provider_reset_password_link), "Reset password link is not visible on the provider login page."
            assert self.page.is_visible(self.provider_sign_up_link), "Sign up link is not visible on the provider login page."

    def verify_invalid_login(self) -> None:
        self.go_to_url(self.URL)
        self.verify_login_page_elements()
        self.login()
        assert self.page.is_visible("text='The Email field is invalid.'"), "Error message for invalid login is not visible."
        assert self.is_disabled(self.submit_button), "Submit button should be disabled for invalid login."

    
    def _get_login_url(self) -> str:
        if MEMBER_FACING_PORTAL_URL in self.URL:
            return MEMBER_FACING_PORTAL_URL
        elif PROVIDER_FACING_PORTAL_URL in self.URL:
            return PROVIDER_FACING_PORTAL_URL
        else:
            raise ValueError(f"Invalid URL provided for login page: {self.URL}")