from pages.base_page import BasePage
from components.accordion import Accordion
from playwright.sync_api import Page


class ReserveAppointmentPage(BasePage):
    PATH = "/sign-up/reserve-appointment"
    RETURNING_PATH = "/book-scan/reserve-appointment"

    @classmethod
    def for_new_user(cls, page: Page) -> "ReserveAppointmentPage":
        return cls(page, path=cls.PATH)

    @classmethod
    def for_returning_user(cls, page: Page) -> "ReserveAppointmentPage":
        return cls(page, path=cls.RETURNING_PATH)

    def __init__(self, page, path: str = PATH):
        super().__init__(page, path=path)
        self.page_title = "Reserve your appointment"
        self.payment_info_accordion = PaymentInfoAccordion(page)
        self.pricing_container_selector = "div[class='pricing-container']"
        self.continue_button_selector = "button:has-text('Continue')"
        self.back_button_selector = "button:has-text('Back')"

    def verify_page_elements(self) -> None:
        self.wait_for_elem_visible(self.pricing_container_selector)
        self.payment_info_accordion.verify_elem_visible()
        self.payment_info_accordion.verify_expanded_accordion_elements("Card")
        self.payment_info_accordion.verify_expanded_accordion_elements("link")
        self.payment_info_accordion.verify_expanded_accordion_elements("Affirm")
        self.wait_for_elem_visible(self.continue_button_selector)
        self.wait_for_elem_visible(self.back_button_selector)

    def verify_payment_info_entry(self, card_info: dict) -> None:
        self.payment_info_accordion.expand_accordion_item("Card")
        card_locators = self.payment_info_accordion.accordion_elements["Card"]
        frame = self.payment_info_accordion.frame
        frame.locator(card_locators["card_number"]).fill(card_info["card_number"])
        frame.locator(card_locators["expiration_date"]).fill(card_info["expiration_date"])
        frame.locator(card_locators["cvv"]).fill(card_info["cvv"])
        frame.locator(card_locators["zip_code"]).fill(card_info["zip_code"])
        frame.locator(card_locators["country"]).select_option(card_info["country"])
        optional = card_locators.get("optional_fields", {})
        if optional.get("email") and card_info.get("email"):
            frame.locator(optional["email"]).fill(card_info["email"])
        if optional.get("phone") and card_info.get("phone"):
            frame.locator(optional["phone"]).fill(card_info["phone"])
        self.page.click(self.continue_button_selector)



class PaymentInfoAccordion(Accordion):
    def __init__(self, page: Page):
        super().__init__(page, root_selector="div[class*='payment-info-accordion']")
        self.accordion_elements = {
            "Card": {
                "card_number": "input[id='payment-numberInput']",
                "expiration_date": "input[id='payment-expiryInput']",
                "cvv": "input[id='payment-cvcInput']",
                "zip_code": "input[id='payment-postalCodeInput']",
                "country": "select[id='payment-countryInput']",
                "optional_fields": {
                    "email": "input[id='payment-linkEmailInput']",
                    "phone": "input[id='payment-linkMobilePhoneInput']",
                }
            },
            "link": {
                "bank_name": "input[id='payment-bankInput']",
            },
            "Affirm": {
                "learn_more_button": "button:has-text('Learn More')",
                "description_text": "span[data-testid='next-action-text']"
            }
        }